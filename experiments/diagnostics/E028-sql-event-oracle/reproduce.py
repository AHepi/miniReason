"""Recheck the operator-only event oracle with SQLite; no provider access."""
import json
from pathlib import Path
import sqlite3

data=json.loads(Path(__file__).with_name("oracle.json").read_text())
con=sqlite3.connect(":memory:")
con.executescript("CREATE TABLE L(lid INTEGER PRIMARY KEY,k INTEGER); CREATE TABLE R(rid INTEGER PRIMARY KEY,k INTEGER,v TEXT);")
con.executemany("INSERT INTO L VALUES (?,?)",data["initial"]["Lrows"])
con.executemany("INSERT INTO R VALUES (?,?,?)",data["initial"]["Rrows"])
def snapshot():
    return {"Lrows":[list(r) for r in con.execute("SELECT * FROM L ORDER BY lid")],
            "Rrows":[list(r) for r in con.execute("SELECT * FROM R ORDER BY rid")],
            "output_bag":sorted([list(r) for r in con.execute("SELECT ALL L.lid,L.k,R.v FROM L LEFT JOIN R ON L.k=R.k")],key=lambda r:json.dumps(r,ensure_ascii=False))}
assert snapshot()==data["initial"]
for event in data["events"]:
    table,row=event["table"],event["row"]
    assert table in {"L","R"}
    identity="lid" if table=="L" else "rid"
    if event["operation"]=="delete":
        assert list(con.execute(f"SELECT * FROM {table} WHERE {identity}=?",(row[0],)).fetchone())==row
        con.execute(f"DELETE FROM {table} WHERE {identity}=?",(row[0],))
    else:
        assert event["operation"]=="insert"
        con.execute(f"INSERT INTO {table} VALUES ({','.join('?' for _ in row)})",row)
    assert snapshot()==event["after"]
    assert [r for r in snapshot()["output_bag"] if r[0]==3]==[[3,9,None]]
print(json.dumps({"status":"PASS","event_count":len(data["events"]),"protected_key9":True,"provider_calls":0}))
