"""Offline SQL material preparation; no provider calls or candidate execution.

This is an extensional SQLite oracle, never an incremental reference solution.
Participant construction inputs are allowlisted separately from operator cases.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sqlite3

SCHEMA = """CREATE TABLE L(lid INTEGER PRIMARY KEY, k INTEGER);
CREATE TABLE R(rid INTEGER PRIMARY KEY, k INTEGER, v TEXT);
"""
QUERY = "SELECT ALL L.lid, L.k, R.v FROM L LEFT JOIN R ON L.k = R.k"
TASK = """Construct a reusable account of how to maintain the exact result of the supplied
SQL query after each admitted insertion or deletion, using retained state and the next
event. Choose and explain the retained information and its connection to the output.
The account must cover arbitrary finite tables within the stated value domain and legal
finite event sequences. Identify what initialization needs. After initialization, the
original database and its history are unavailable except insofar as your state retains
information from them. Explain an update by its affected keys and the output changes;
whole-database recomputation may be proposed as an explicit alternative, but is outside
the requested incremental-use contract. State unsupported cases and uncertainty.
Prose, mathematical expressions and optional code are equally admissible proposals.
No supplied list of finished update rules or required state-field vocabulary is given.
A later interpreter, if needed, will be a separately declared contribution and must not
silently repair your account. A finding of insufficiency is an admissible result.
"""
SOURCE_NOTES = """The supplied SQL text defines the target query. SELECT ALL retains duplicate
result rows. LEFT JOIN retains each left row and provides SQL NULL values for the
right columns when the join condition finds no right row. Ordinary equality with
a NULL operand does not evaluate to true. The study uses SQLite's implementation.
These query semantics specify the task; no incremental maintenance rule is supplied.
"""
SOURCES = [
    {"url":"https://www.sqlite.org/lang_select.html", "sections":["2.1", "2.6"],
     "supports":"LEFT JOIN result formation and SELECT ALL multiplicity", "checked_utc_date":"2026-09-12"},
    {"url":"https://www.sqlite.org/lang_expr.html", "sections":["2"],
     "supports":"Ordinary comparison with NULL is not true", "checked_utc_date":"2026-09-12"},
]

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def participant_packet():
    return {"schema":"minireason.sql-construction-material.v1", "schema_sql":SCHEMA,
        "query_sql":QUERY, "task":TASK, "source_notes":SOURCE_NOTES, "sources":SOURCES,
        "value_domain":{"ids":"explicit signed 32-bit integers, unique within each table",
            "keys":"signed 32-bit integers or SQL NULL", "values":"Unicode strings or SQL NULL"},
        "events":{"insert":"Full new row [id,key] for L or [id,key,value] for R; id must be absent",
            "delete":"Full before-image of an existing row; deletion removes that id exactly once",
            "order":"Apply one legal event at a time; updates are a delete followed by an insert",
            "observations":"After each event, the output is the complete bag of [lid,key,value] rows; row order is immaterial"},
        "constraints":{"initial_read":True,"post_initial_database_access":False,
            "state_vocabulary":"chosen by the candidate","prose_admissible":True,
            "incremental_rule_supplied":False}}

def _validate_row(table, row):
    width = {"L":2,"R":3}.get(table)
    if width is None or type(row) is not list or len(row)!=width:
        raise ValueError("ROW_SHAPE")
    if type(row[0]) is not int or not -(2**31)<=row[0]<2**31:
        raise ValueError("ID_DOMAIN")
    if row[1] is not None and (type(row[1]) is not int or not -(2**31)<=row[1]<2**31):
        raise ValueError("KEY_DOMAIN")
    if table=="R" and row[2] is not None and type(row[2]) is not str:
        raise ValueError("VALUE_DOMAIN")

def connect(initial):
    if set(initial)!={"L","R"}:
        raise ValueError("INITIAL_TABLES")
    db=sqlite3.connect(":memory:")
    try:
        db.executescript(SCHEMA)
        for table in ("L","R"):
            for row in initial[table]:
                _validate_row(table,row)
                db.execute("INSERT INTO "+table+" VALUES ("+",".join("?" for _ in row)+")",row)
        return db
    except BaseException:
        db.close()
        raise

def view(db):
    counts=Counter(tuple(row) for row in db.execute(QUERY))
    return [{"row":list(row),"multiplicity":count} for row,count in
        sorted(counts.items(),key=lambda item:canonical(list(item[0])))]

def apply_event(db,event):
    if set(event)!={"op","table","row"} or event["op"] not in {"insert","delete"}:
        raise ValueError("EVENT_CONTRACT")
    table,row=event["table"],event["row"]
    _validate_row(table,row)
    if event["op"]=="insert":
        db.execute("INSERT INTO "+table+" VALUES ("+",".join("?" for _ in row)+")",row)
    else:
        ident="lid" if table=="L" else "rid"
        actual=db.execute("SELECT * FROM "+table+" WHERE "+ident+"=?",(row[0],)).fetchone()
        if actual is None or list(actual)!=row:
            raise ValueError("DELETE_BEFORE_IMAGE")
        db.execute("DELETE FROM "+table+" WHERE "+ident+"=?",(row[0],))

def event(op,table,*row):
    return {"op":op,"table":table,"row":list(row)}

def run_case(case):
    db=connect(case["initial"])
    try:
        snapshots=[view(db)]
        for operation in case["events"]:
            apply_event(db,operation)
            snapshots.append(view(db))
        return {"case_id":case["case_id"],"case_sha256":digest(case),"snapshots":snapshots}
    finally:
        db.close()

def cases():
    return [
        {"case_id":"q01","initial":{"L":[[1,7]],"R":[]},"events":[
            event("insert","R",10,7,"x"),event("insert","R",11,7,"x"),
            event("delete","R",10,7,"x"),event("delete","R",11,7,"x")]},
        {"case_id":"q02","initial":{"L":[[1,7]],"R":[[10,7,None]]},"events":[
            event("insert","R",11,7,"x"),event("delete","R",11,7,"x"),
            event("delete","R",10,7,None),event("insert","R",12,7,None),
            event("insert","R",13,7,None),event("delete","R",12,7,None)]},
        {"case_id":"q03","initial":{"L":[[1,None],[2,7]],"R":[[10,None,"n"],[11,7,"x"]]},"events":[
            event("insert","R",12,None,"z"),event("delete","R",10,None,"n"),
            event("insert","L",3,None),event("delete","R",11,7,"x")]},
        {"case_id":"q04","initial":{"L":[],"R":[[10,7,"x"],[11,7,"x"],[12,7,None]]},"events":[
            event("insert","L",1,7),event("insert","L",2,7),event("delete","L",1,7),
            event("delete","R",10,7,"x"),event("delete","L",2,7)]},
        {"case_id":"q05","initial":{"L":[[1,7],[2,9]],"R":[[10,7,"x"],[11,9,"y"]]},"events":[
            event("insert","R",12,99,"distractor"),event("insert","R",13,7,"z"),
            event("delete","R",10,7,"x"),event("delete","R",12,99,"distractor")]},
        {"case_id":"q06","initial":{"L":[[1,7]],"R":[[10,7,"x"],[11,8,"y"]]},"events":[
            event("delete","R",10,7,"x"),event("insert","R",10,8,"x"),
            event("delete","L",1,7),event("insert","L",1,8),event("delete","R",11,8,"y")]},
    ]

def recode_case(case):
    """Rename the authored finite fixture bank into its declared finite image.

    This arithmetic shift is not a total bijection of the signed32 value domain.
    Reject mapped rows outside that domain; no random search or arm selection.
    """
    def row(table, values):
        renamed = [values[0]+1000, None if values[1] is None else values[1]+10000] + (
            [] if table=="L" else [None if values[2] is None else "r:"+values[2]])
        _validate_row(table, renamed)
        return renamed
    return {"case_id":case["case_id"]+"r", "initial":{table:[row(table,x) for x in case["initial"][table]]
        for table in ("L","R")}, "events":[{"op":x["op"],"table":x["table"],
        "row":row(x["table"],x["row"])} for x in case["events"]]}

def ambiguity_witness():
    ev=event("insert","R",11,7,"x")
    pair=[{"case_id":"hidden0","initial":{"L":[[1,7]],"R":[]},"events":[ev]},
          {"case_id":"hidden1","initial":{"L":[[1,7]],"R":[[10,7,None]]},"events":[ev]}]
    answers=[run_case(x) for x in pair]
    visible=[{"schema_sql":SCHEMA,"query_sql":QUERY,"old_view":a["snapshots"][0],"event":ev}
        for a in answers]
    if visible[0]!=visible[1] or answers[0]["snapshots"][1]==answers[1]["snapshots"][1]:
        raise ValueError("AMBIGUITY_WITNESS_FAILED")
    return {"schema":"minireason.sql-ambiguity-witness.v1", "operator_only":True,
        "histories":pair,"oracle":answers,"common_visible_packet":visible[0],
        "common_visible_sha256":digest(visible[0]),"identical_visible_inputs":True,
        "different_required_successors":True,
        "claim":"No deterministic function of this old visible view and event alone is correct for both admissible histories. An unconstrained guess may match either; this does not establish semantic reason use.",
        "needed_distinction":"The equal visible NULL row can be a left-join extension or a real matched right row whose value is NULL.",
        "limit":"No historical novelty, model limitation or specific candidate active route follows. Additional retained information can resolve this ambiguity in different ways."}

def make_bundle():
    base=cases()
    all_cases=base+[recode_case(case) for case in base]
    return {"participant/construction.json":participant_packet(),
        "operator/cases.json":{"schema":"minireason.sql-case-family.v1","operator_only":True,
            "selection":"Six deliberately chosen source-derived cases and injective renamings into a finite image; arithmetic shifts apply to this finite bank, not the whole signed32 domain; no random generator or seed",
            "case_ids_are_not_model_inputs":True,"cases":all_cases},
        "operator/oracle.json":{"schema":"minireason.sql-oracle.v1","operator_only":True,
            "sqlite_version":sqlite3.sqlite_version,"query_sql":QUERY,
            "results":[run_case(case) for case in all_cases],
            "claim":"Exact finite output-bag obligations only; no incremental candidate has run"},
        "operator/ambiguity.json":ambiguity_witness(),
        "operator/route-status.json":{"schema":"minireason.sql-route-preparation.v1",
            "status":"OFFLINE_MATERIAL_ONLY","provider_calls":0,"candidate_occurrence":None,
            "operative_state":None,"candidate_execution":False,"frozen_live_plan":False,
            "participant_allowlist":["participant/construction.json"],
            "pending":"Actual construction, interpreted initialization, distinct use/return template, treatment-specific wire audit, source and resource freeze"}}

def write_bundle(root):
    root=Path(root)
    if root.exists():
        raise FileExistsError(root)
    content=make_bundle()
    root.mkdir(parents=True)
    entries={}
    for name,value in content.items():
        path=root/name
        path.parent.mkdir(parents=True,exist_ok=True)
        data=(json.dumps(value,indent=2,ensure_ascii=False)+"\n").encode()
        path.write_bytes(data)
        entries[name]={"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)}
    manifest={"schema":"minireason.sql-preparation-manifest.v1","files":entries,
        "sqlite_version":sqlite3.sqlite_version,"network_access_in_generator":False,
        "provider_calls":0,"status":"PREPARATION_ONLY"}
    (root/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    return manifest

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    print(json.dumps(write_bundle(args.output),indent=2))
