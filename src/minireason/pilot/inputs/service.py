# Local bridge provenance: miniReason P-A2 integration; not copied from an upstream module.
# DeepReason reference: https://github.com/AHepi/DeepReason @ 9607fba6f0a3066fbcab282c9ae0fad823e52e0c; original path: none (local bridge); upstream license: MIT, Copyright (c) 2026 Aaron Hepi; see LICENSE.
"""Pilot adaptation of DeepReason admission: pinned units and exact scoped reads.
No path is accepted from a model. Reads use the in-memory bytes pinned at seal.
The filesystem loader is an operator-only allowlist reader, never a model tool.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import os
import stat
from types import MappingProxyType

from .canonical import canonical_json, sha256_hex
from .models import AttachedSourceProvenanceV1
from .parse import AdmissionInput, admit_sources
from .preflight import InputError
from ..util import strict_loads

_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_MUTABLE = frozenset({"task", "premises", "candidate", "objections"})
INPUT_REF_SCHEMA = {
    "type":"object", "additionalProperties":False,
    "required":["unit_id","start","end","encoding"],
    "properties":{
        "unit_id":{"type":"string","pattern":"^[0-9a-f]{64}$"},
        "start":{"type":"integer","minimum":0},
        "end":{"type":"integer","minimum":1},
        "encoding":{"type":"string","enum":["json"]},
        "overrides":{"type":"object","additionalProperties":False,"properties":{
            "task":{"type":"string"}, "candidate":{"type":"string"},
            "premises":{"type":"array","items":{"type":"string"}},
            "objections":{"type":"array","items":{"type":"string"}}}}
    }}

def _denied_path(path):
    name = str(path).replace("\\", "/").casefold()
    parts = PurePosixPath(name).parts
    return (any(p.startswith(".env") for p in parts) or
            any(word in name for word in ("reader-brief", "reader_brief", "briefs/", "sealed-brief",
                                         "derived-properties", "derived_properties")))

def _safe_read(root, relative):
    if not isinstance(relative,str) or not relative or _denied_path(relative):
        raise InputError("INPUT_PATH_REFUSED", "source path is excluded")
    p = PurePosixPath(relative.replace("\\", "/"))
    if p.is_absolute() or ".." in p.parts or any(":" in part for part in p.parts):
        raise InputError("INPUT_PATH_REFUSED", "source must be a repository-relative pinned path")
    path = root.resolve() / Path(*p.parts)
    if not path.resolve().is_relative_to(root.resolve()) or _denied_path(path.resolve()) or not path.is_file():
        raise InputError("INPUT_PATH_REFUSED", "source escapes root or is unavailable")
    # Positive authority is the explicit task descriptor, never a model path.
    # Reject linked/reparse components and check the opened handle before read.
    relative_parts = path.relative_to(root.resolve()).parts
    cursor = root.resolve()
    for component in relative_parts:
        cursor = cursor/component
        observed = cursor.lstat()
        if stat.S_ISLNK(observed.st_mode) or (getattr(observed,"st_file_attributes",0) & 0x400):
            raise InputError("INPUT_PATH_REFUSED", "linked/reparse sources are excluded")
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size > 16*1024*1024:
        raise InputError("INPUT_PATH_REFUSED", "source must be a bounded regular single-link file")
    flags = os.O_RDONLY | getattr(os,"O_BINARY",0) | getattr(os,"O_NOFOLLOW",0)
    descriptor = os.open(path,flags)
    try:
        opened = os.fstat(descriptor)
        identity = lambda info: (info.st_dev,info.st_ino,info.st_size,info.st_mtime_ns)
        if identity(opened) != identity(before):
            raise InputError("INPUT_PATH_REFUSED", "source changed before opening")
        with os.fdopen(descriptor,"rb",closefd=False) as handle:
            raw = handle.read(16*1024*1024+1)
        if identity(os.fstat(descriptor)) != identity(opened) or identity(path.lstat()) != identity(opened):
            raise InputError("INPUT_PATH_REFUSED", "source changed while reading")
        return raw
    finally:
        os.close(descriptor)

class TaskInputs:
    def __init__(self):
        self._units = {}
        self._cards = {}
        self.receipts = []
        self.resolved_inputs = {}
        self.input_ref = None
        self.dossier = None

    @classmethod
    def from_task(cls, task, repo_root):
        self = cls()
        cards = task.get("input_units", [])
        if not isinstance(cards,list):
            raise InputError("INPUT_MANIFEST_INVALID", "input_units must be a list")
        for card in cards:
            if not isinstance(card,dict) or set(card) != {"unit_id","sha256","byte_count","path","media_type","role"}:
                raise InputError("INPUT_MANIFEST_INVALID", "unit descriptor has an invalid shape")
            if card["role"] not in {"task_input","public_source"}:
                raise InputError("INPUT_ROLE_REFUSED", "only task inputs and pinned public sources are admitted")
            if not isinstance(card["unit_id"],str) or not _DIGEST.fullmatch(card["unit_id"]):
                raise InputError("INPUT_MANIFEST_INVALID", "invalid content id")
            if type(card["byte_count"]) is not int or not 0 < card["byte_count"] <= 16*1024*1024:
                raise InputError("INPUT_MANIFEST_INVALID", "invalid byte count")
            if card["unit_id"] in self._cards:
                raise InputError("INPUT_MANIFEST_INVALID", "duplicate unit descriptor")
            raw = _safe_read(Path(repo_root), card["path"])
            if len(raw) != card["byte_count"] or sha256_hex(raw) != card["sha256"] or card["sha256"] != card["unit_id"]:
                raise InputError("INPUT_PIN_MISMATCH", "source bytes differ from task pin")
            try:
                raw.decode("utf-8",errors="strict")
            except UnicodeDecodeError as error:
                raise InputError("INPUT_ENCODING_REFUSED", "pinned source is not strict UTF-8") from error
            self._register(raw,card)
        value = task.get("inputs",{})
        if isinstance(value,dict) and "unit_id" in value:
            self.input_ref = deepcopy(value)
            self.resolved_inputs = self.expand_inputs(value,call_id="seal")
        elif cards:
            raise InputError("INPUT_MANIFEST_INVALID", "P-A2 task inputs must name their pinned JSON unit")
        else:
            if not isinstance(value,dict):
                raise InputError("INPUT_MANIFEST_INVALID", "legacy inputs must be an object")
            self.resolved_inputs = deepcopy(value)
            self.input_ref = self.compact_inputs(value)
        if self._units:
            source_inputs = [AdmissionInput(locator=c["path"],data=self._units[uid])
                             for uid,c in sorted(self._cards.items()) if c["role"] != "task_derived"]
            if source_inputs:
                self.dossier, report = admit_sources(source_inputs,problem_ref="pilot-task",
                    provenance=AttachedSourceProvenanceV1(supplied_by="task pin manifest",
                                                         acquisition_method="verified exact bytes"))
                if report.refusals:
                    raise InputError("INPUT_ADMISSION_REFUSED", "source admission reported omissions",
                                     {"refusals":report.refusals})
        return self

    def _register(self,raw,card):
        uid = sha256_hex(raw)
        if uid in self._units and self._units[uid] != raw:
            raise InputError("INPUT_ID_COLLISION", "known input id changed")
        if (uid in self._cards and card["role"] == "task_derived"
                and self._cards[uid]["role"] not in {"task_input", "task_derived"}):
            raise InputError("INPUT_ROLE_COLLISION", "derived task JSON conflicts with a pinned public-source binding")
        if uid not in self._units:
            self._units[uid] = bytes(raw)
            self._cards[uid] = MappingProxyType(deepcopy(card))
        return uid

    def catalog(self):
        cards = []
        for uid in sorted(self._cards):
            card = dict(self._cards[uid])
            # Canonical parser spans are usable byte locators, not pasted text.
            # CSV projection/extracted blocks are not raw-byte quote locators.
            card["span_blocks"] = [] if self.dossier is None else [
                {"block_id":b.id,"kind":b.kind,"start":b.span_start,"end":b.span_end,
                 "text_sha256":b.text_sha256,"title":b.title}
                for b in sorted(self.dossier.blocks,key=lambda b:(b.span_start,b.id))
                if b.source_sha256 == uid and b.text is None]
            cards.append(card)
        return cards

    def compact_inputs(self,inputs):
        if not isinstance(inputs,dict):
            raise InputError("INPUT_REFERENCE_INVALID", "inputs must be an object")
        raw = canonical_json(inputs)
        uid = sha256_hex(raw)
        self._register(raw,{"unit_id":uid,"sha256":uid,"byte_count":len(raw),
            "path":"host-derived/"+uid+".json","media_type":"application/json","role":"task_derived"})
        return {"unit_id":uid,"start":0,"end":len(raw),"encoding":"json"}

    def expand_inputs(self,value,call_id):
        if not isinstance(value,dict):
            raise InputError("INPUT_REFERENCE_INVALID", "inputs must be an object")
        if "unit_id" not in value:
            return deepcopy(value)  # legacy compatibility; caller still validates scope
        if set(value)-{"unit_id","start","end","encoding","overrides"} or value.get("encoding") != "json":
            raise InputError("INPUT_REFERENCE_INVALID", "invalid input reference shape")
        uid = value["unit_id"]
        if uid not in self._cards or self._cards[uid]["role"] not in {"task_input","task_derived"}:
            raise InputError("INPUT_REFERENCE_INVALID", "input reference is not a pinned task JSON unit")
        if value.get("start") != 0 or value.get("end") != len(self._units[uid]):
            raise InputError("INPUT_REFERENCE_INVALID", "task JSON must resolve its complete pinned unit")
        result = self.read_source(uid,start=0,end=len(self._units[uid]),limit=len(self._units[uid]),call_id=call_id)
        try:
            parsed = strict_loads(result["content"])
            # Reject numeric overflow too: JSON 1e999 otherwise becomes infinity.
            json.dumps(parsed, allow_nan=False)
        except (TypeError, ValueError) as error:
            raise InputError("INPUT_REFERENCE_INVALID", "task JSON must have unique keys and finite values") from error
        if not isinstance(parsed,dict):
            raise InputError("INPUT_REFERENCE_INVALID", "task unit is not an object")
        overrides = value.get("overrides",{})
        if not isinstance(overrides,dict) or set(overrides)-_MUTABLE:
            raise InputError("INPUT_OVERRIDE_REFUSED", "overrides cannot replace sealed source or scope")
        parsed.update(deepcopy(overrides))
        return parsed

    def read_source(self,unit_id,start=0,end=None,limit=65536,call_id="host-read"):
        if not isinstance(unit_id,str) or unit_id not in self._units:
            raise InputError("INPUT_UNPINNED", "read_source accepts only task-pinned unit ids, never paths")
        body = self._units[unit_id]
        end = len(body) if end is None else end
        if any(type(x) is not int for x in (start,end,limit)) or not 0 <= start < end <= len(body) or not 1 <= limit <= 262144:
            raise InputError("INPUT_RANGE_INVALID", "read range/limit must be finite and within the pinned unit")
        # Requested bounds must be UTF-8 boundaries; a limiting cap backs up
        # deterministically and receipts the exact unreturned remainder.
        try:
            body[start:end].decode("utf-8")
        except UnicodeDecodeError as exc:
            raise InputError("INPUT_RANGE_INVALID", "requested bounds split UTF-8 text") from exc
        returned_end = min(end,start+limit)
        while returned_end > start:
            try:
                text = body[start:returned_end].decode("utf-8")
                break
            except UnicodeDecodeError as exc:
                returned_end = start+exc.start
        if returned_end <= start:
            raise InputError("INPUT_LIMIT_TOO_SMALL", "limit cannot contain the next complete UTF-8 character")
        excerpt = body[start:returned_end]
        omitted = []
        if start: omitted.append({"start":0,"end":start,"reason":"outside_requested_range"})
        if returned_end < end: omitted.append({"start":returned_end,"end":end,"reason":"read_limit"})
        if end < len(body): omitted.append({"start":end,"end":len(body),"reason":"outside_requested_range"})
        receipt = {"schema":"pilot.source-read.pa2.v1", "call_id":str(call_id),
            "unit_id":unit_id,"unit_sha256":sha256_hex(body),"unit_bytes":len(body),
            "requested_start":start,"requested_end":end,"limit":limit,
            "start":start,"end":returned_end,"byte_count":len(excerpt),
            "source_ref":"unit:"+unit_id+"@"+str(start)+":"+str(returned_end),
            "excerpt_sha256":sha256_hex(excerpt),"omitted_ranges":omitted,
            "role":self._cards[unit_id]["role"]}
        self.receipts.append(deepcopy(receipt))
        return {"content":text,"receipt":receipt}

    def resolve_ref(self,ref,call_id,limit=None):
        return self.read_source(ref["unit_id"],start=ref["start"],end=ref["end"],
                                limit=limit or ref["end"]-ref["start"],call_id=call_id)

    def exposure_receipts(self,messages,call_id):
        """Distinguish exact text delivery from canonical JSON object delivery.
        Neither receipt claims the participant read or used its content.
        Paths/catalog entries alone never count as exposure. JSON equality is
        not byte equality: prepared wire custody records actual serialization.
        """
        strings = []
        objects = []
        def visit(value, *, field=None, root=False):
            if isinstance(value,str): strings.append(value)
            elif isinstance(value,list):
                for item in value: visit(item)
            elif isinstance(value,dict):
                if root or field == "inputs":
                    objects.append(canonical_json(value))
                for key,item in value.items(): visit(item, field=key)
        for message in messages:
            content = message.get("content","")
            if not isinstance(content,str): continue
            strings.append(content)
            try: visit(json.loads(content), root=True)
            except (TypeError,ValueError): pass
        receipts = []
        for uid,body in sorted(self._units.items()):
            text = body.decode("utf-8")
            if text in strings:
                receipt = {"schema":"pilot.source-exposure.pa2.v1","call_id":str(call_id),
                    "delivery":"exact UTF-8 text in decoded message field",
                    "unit_id":uid,"unit_sha256":uid,"unit_bytes":len(body),
                    "start":0,"end":len(body),"byte_count":len(body),
                    "excerpt_sha256":uid,"omitted_ranges":[],"role":self._cards[uid]["role"]}
                receipts.append(receipt)
            elif body in objects:
                receipts.append({"schema":"pilot.json-delivery.pa2.v1","call_id":str(call_id),
                    "unit_id":uid,"unit_sha256":uid,"canonical_json_sha256":uid,
                    "delivery":"decoded JSON object equality under canonical_json; not literal byte exposure",
                    "role":self._cards[uid]["role"]})
        # Tool reads carry exact range receipts alongside their delivered bytes.
        for message in messages:
            try: packet = json.loads(message.get("content",""))
            except (TypeError,ValueError): continue
            def read_results(value):
                if isinstance(value,dict):
                    receipt = value.get("receipt")
                    if isinstance(receipt,dict) and receipt.get("schema") == "pilot.source-read.pa2.v1":
                        uid = receipt.get("unit_id")
                        if (receipt in self.receipts and uid in self._units and
                            isinstance(value.get("content"),str) and
                            value["content"].encode("utf-8") == self._units[uid][receipt["start"]:receipt["end"]]):
                            receipts.append({**receipt,"call_id":str(call_id),"delivery":"outgoing tool-result data"})
                    for item in value.values(): read_results(item)
                elif isinstance(value,list):
                    for item in value: read_results(item)
            read_results(packet)
        return receipts

    def freeze(self,root):
        directory = Path(root)/"input-units"
        directory.mkdir(parents=True,exist_ok=True)
        for uid,raw in sorted(self._units.items()):
            path = directory/(uid+".txt")
            if path.exists():
                if path.read_bytes() != raw:
                    raise InputError("INPUT_FROZEN_CONFLICT", "frozen source bytes changed")
            else:
                with path.open("x",encoding="utf-8",newline="") as f:f.write(raw.decode("utf-8"))
        manifest = {"schema":"pilot.input-units.pa2.v1","units":self.catalog(),
                    "dossier":None if self.dossier is None else self.dossier.model_dump(mode="json",by_alias=True)}
        raw = canonical_json(manifest)
        path = directory/(sha256_hex(raw)+".manifest.json")
        if path.exists():
            if path.read_bytes() != raw:
                raise InputError("INPUT_FROZEN_CONFLICT", "frozen manifest bytes changed")
        else:
            with path.open("x",encoding="utf-8",newline="") as f:f.write(raw.decode("utf-8"))
        return {"manifest_sha256":sha256_hex(raw),"manifest_path":str(path)}
