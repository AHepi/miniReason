import json

agents = [
    {"id": 1, "team": "Red", "threshold": 5, "enabled": 1},
    {"id": 2, "team": "Red", "threshold": 7, "enabled": 0},
    {"id": 3, "team": "Blue", "threshold": 6, "enabled": 1},
    {"id": 4, "team": "Blue", "threshold": 8, "enabled": 1},
    {"id": 5, "team": "Gold", "threshold": 4, "enabled": 1},
]

events = [
    {"agent_id": 1, "status": "ok", "value": 6},
    {"agent_id": 1, "status": "ok", "value": 4},
    {"agent_id": 2, "status": "ok", "value": 10},
    {"agent_id": 3, "status": "ok", "value": None},
    {"agent_id": 4, "status": "ok", "value": 9},
    {"agent_id": 4, "status": "bad", "value": 12},
    {"agent_id": 6, "status": "ok", "value": 10},
]

joined = []
for agent in agents:
    if agent["enabled"] != 1:
        continue
    matches = []
    for event in events:
        value = event["value"]
        on_is_true = (
            event["agent_id"] == agent["id"]
            and event["status"] == "ok"
            and value is not None
            and value >= agent["threshold"]
        )
        if on_is_true:
            matches.append(event)
    if matches:
        for event in matches:
            joined.append((agent, event["value"]))
    else:
        joined.append((agent, None))

groups = {}
for agent, value in joined:
    row = groups.setdefault(agent["team"], {"rows_seen": 0, "valued": 0, "total": 0})
    row["rows_seen"] += 1
    if value is not None:
        row["valued"] += 1
        row["total"] += value
    else:
        row["total"] += agent["threshold"]

qualified = []
for team, aggregate in groups.items():
    if aggregate["valued"] < aggregate["rows_seen"]:
        qualified.append([team, aggregate["rows_seen"], aggregate["valued"], aggregate["total"]])
qualified.sort(key=lambda row: (-row[3], row[0]))
expected = [["Blue", 2, 1, 15], ["Gold", 1, 0, 4]]
assert qualified == expected

# Corroborate the literal bag interpreter using the exact declared query.
import sqlite3
connection = sqlite3.connect(":memory:")
connection.executescript("""
CREATE TABLE agents(id INTEGER, team TEXT, threshold INTEGER, enabled INTEGER);
INSERT INTO agents VALUES (1,'Red',5,1),(2,'Red',7,0),(3,'Blue',6,1),(4,'Blue',8,1),(5,'Gold',4,1);
CREATE TABLE events(agent_id INTEGER, status TEXT, value INTEGER);
INSERT INTO events VALUES (1,'ok',6),(1,'ok',4),(2,'ok',10),(3,'ok',NULL),(4,'ok',9),(4,'bad',12),(6,'ok',10);
""")
sqlite_rows = [list(row) for row in connection.execute("""
SELECT a.team, COUNT(*) AS rows_seen, COUNT(e.value) AS valued,
       SUM(COALESCE(e.value, a.threshold)) AS total
FROM agents AS a
LEFT JOIN events AS e
  ON e.agent_id = a.id AND e.status = 'ok' AND e.value >= a.threshold
WHERE a.enabled = 1
GROUP BY a.team
HAVING COUNT(e.value) < COUNT(*)
ORDER BY total DESC, a.team ASC
""")]
connection.close()
assert sqlite_rows == qualified

payload = {
    "problem_id": "P04",
    "answer": qualified,
    "diagnostics": {
        "sqlite_query_rows": sqlite_rows,
        "enabled_join_rows": [
            {"agent_id": agent["id"], "team": agent["team"], "event_value": value}
            for agent, value in joined
        ],
        "all_group_aggregates": groups,
    },
}
print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
