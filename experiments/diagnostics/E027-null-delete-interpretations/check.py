"""Operator-authored two-reading witness; no provider and no candidate code execution."""
import hashlib
import json
import sqlite3
from pathlib import Path

def witness():
    con = sqlite3.connect(":memory:")
    con.executescript("CREATE TABLE L(lid INTEGER PRIMARY KEY,k INTEGER); CREATE TABLE R(rid INTEGER PRIMARY KEY,k INTEGER,v TEXT);")
    con.execute("INSERT INTO L VALUES (?,?)", (1, None))
    query = "SELECT ALL L.lid,L.k,R.v FROM L LEFT JOIN R ON L.k=R.k"
    initial = [list(row) for row in con.execute(query)]
    con.execute("DELETE FROM L WHERE lid=?", (1,))
    expected = [list(row) for row in con.execute(query)]
    actual_left = [list(row) for row in con.execute("SELECT lid,k FROM L")]
    # Section4.2 explicitly removes the NULL branch's output triple only.
    literal = {"Lrows": [[1,None]], "Rrows": [], "LkeyIndex": [], "RkeyIndex": [], "cached_output": []}
    # Section2.1 defines Lrows as live rows; applying that invariant adds deletion.
    uniform = {"Lrows": [], "Rrows": [], "LkeyIndex": [], "RkeyIndex": [], "cached_output": []}
    literal_reconstructed = [[lid,key,None] for lid,key in literal["Lrows"]]
    uniform_reconstructed = [[lid,key,None] for lid,key in uniform["Lrows"]]
    assert initial == [[1,None,None]] and expected == [] and actual_left == []
    assert literal["cached_output"] == uniform["cached_output"] == expected
    assert literal["Lrows"] != actual_left and uniform["Lrows"] == actual_left
    assert literal_reconstructed != expected and uniform_reconstructed == expected
    return {"schema":"minireason.selected-account-interpretation-witness.v1", "provider_calls":0,
      "candidate_answer_sha256":"b5fb115264eaff0a0466ea19012b58624a2669f95c4b6e47aab545c2074268c0",
      "candidate_sections":["2.1","4.2","5"],"initial_L":[[1,None]],"initial_R":[],
      "event":{"table":"L","operation":"delete","row":[1,None]},"initial_output":initial,
      "sqlite_version":sqlite3.sqlite_version,"sqlite_after_output":expected,"sqlite_after_L":actual_left,
      "literal_branch_reading":literal,"invariant_guided_uniform_removal":uniform,
      "reconstructed_literal_output":literal_reconstructed,"reconstructed_uniform_output":uniform_reconstructed,
      "finding":"Both cached deltas satisfy immediate query output; literal retained Lrows violates live-row meaning and its later reconstructed output diverges.",
      "interpretation_limit":"Literal branch reading is not the only reasonable reading. Uniform deletion is supported by wider prose intent but is an explicitly attributed extra branch operation. No claim of wrong model use or a unique mandatory reading.",
      "scope":"Operator-authored deterministic diagnostic of two readings; no model-generated execution or B result."}

if __name__ == "__main__":
    print(json.dumps(witness(),ensure_ascii=False,indent=2))
