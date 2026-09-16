"""Offline contribution-pair adapter (v5 contract, WAVE7 extension).

Admission records exact authored reference plus frozen delivery mapping. It is
not a finding of reason use (FW5:601,626-634). No FCL is repaired or interpreted.
Raw UTF-8 file spans and legacy Surface code-point offsets remain separate.
"""
from __future__ import annotations

import hashlib
import json
import ntpath
from pathlib import Path
import re
from typing import Any, Mapping, Sequence

from minireason.loop.surface import Surface, Span

SCHEMA = "minireason.loop.rows_pairs.v1"
BUILDER = "pairs-v1"
POSITIONS = (("objection", "response", "o", "r"),
             ("rival", "response", "v", "r"),
             ("response", "carry", "r", "c"))
DEFAULT_GROUPS = ({"arm": "mini_prose", "code": "p"},
                  {"arm": "mini_fcl", "code": "f"})
RUN_NAME = "L004-loop-read-f001-occ09-2026-09-16"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _read(path: Path, root: Path) -> dict[str, Any]:
    resolved = path.resolve()
    relative = resolved.relative_to(root.resolve()).as_posix()
    raw = resolved.read_bytes()
    raw.decode("utf-8")
    return _span(raw, relative, 0, len(raw))


def _span(raw: bytes, path: str, start: int, end: int) -> dict[str, Any]:
    text = raw[start:end].decode("utf-8")
    return {"path": path, "sha256": _sha(raw), "byte_start": start,
            "byte_end": end, "line_start": raw[:start].count(b"\n") + 1,
            "line_end": raw[:max(start, end - 1)].count(b"\n") + 1,
            "codepoint_start": len(raw[:start].decode("utf-8")),
            "codepoint_end": len(raw[:end].decode("utf-8")), "text": text}


def _sub(source: Mapping[str, Any], start: int, end: int) -> dict[str, Any]:
    raw = source["text"].encode("utf-8")
    return _span(raw, source["path"], start, end)


def _coord(problem: str, arm: str, cycle: int, node: str) -> dict[str, Any]:
    return dict(problem=problem, arm=arm, cycle=cycle, node=node)


def _coord_key(coord: Mapping[str, Any]) -> str:
    return f"{coord['problem']}/{coord['arm']}/cycle-{coord['cycle']}/{coord['node']}"


def _path(occurrence: Path, category: str, coord: Mapping[str, Any], suffix: str) -> Path:
    return (occurrence / category / coord["problem"] / coord["arm"] /
            f"cycle{coord['cycle']:02d}" / (coord["node"] + suffix))


def cell_key_for(key: str) -> str:
    """Pure mirror of the driver's folding; tests check actual agreement."""
    folded = []
    for part in key.split("/"):
        if not part:
            raise ValueError("empty key segment")
        text = re.sub(r"[^A-Za-z0-9_.#-]", "-", part).strip("-") or "x"
        if not text[0].isalnum():
            text = "x" + text
        folded.append(text)
    folded[-1] += "#" + _sha(key.encode("utf-8"))[:12]
    return "/".join(folded)


def provider_paths(key: str, run_name: str = RUN_NAME,
                   root: str = r"C:\Dev\miniReason") -> dict[str, str]:
    prefix = ntpath.join(root, "experiments", "loops", run_name, "readings")
    return {name: ntpath.join(prefix, key.replace("/", "\\"),
            (cell_key_for(key) + suffix).replace("/", "\\"),
            "judge-1", "provider", "call-0001.response.json")
            for name, suffix in (("original", ""), ("swapped", "#order-swapped"),
                                 ("paraphrase", "#paraphrase-1"))}


def validate_keys(rows: Sequence[Mapping[str, Any]], run_name: str = RUN_NAME) -> None:
    keys = [row["row_key"] for row in rows]
    cells = [cell_key_for(key) for key in keys]
    if len(set(keys)) != len(keys) or len(set(cells)) != len(cells):
        raise ValueError("pair key/cell collision")
    source_pairs = [(row["mapping_evidence"][0]["path"],
                     json.dumps(row["earlier_coordinate"], sort_keys=True),
                     json.dumps(row["later_coordinate"], sort_keys=True)) for row in rows]
    if len(set(source_pairs)) != len(source_pairs):
        raise ValueError("duplicate source pair under distinct adapter aliases")
    for key in keys:
        if not re.fullmatch(r"h005-row/[A-Za-z0-9]{2,12}#u/ref/[ovr]", key):
            raise ValueError("pair key outside declared grammar")
        coordinate, _record, field, earlier = key[len("h005-row/"):].replace("#", "/").split("/")
        row = next(row for row in rows if row["row_key"] == key)
        if tuple(row["key_components"]) != (coordinate, _record, field, earlier):
            raise ValueError("pair key/component mismatch")
        if max(map(len, provider_paths(key, run_name).values())) >= 240:
            raise ValueError("pair provider path reaches Windows 240-character bound")


def adapter_index(rows: Sequence[Mapping[str, Any]]) -> dict[tuple[str, ...], Mapping[str, Any]]:
    validate_keys(rows)
    result = {tuple(row["key_components"]): row for row in rows}
    if len(result) != len(rows):
        raise ValueError("pair adapter identity collision")
    return result


def _passage(source: Mapping[str, Any], start: int, end: int) -> dict[str, Any]:
    raw = source["text"].encode("utf-8")
    # Exact raw-file paragraph/sentence, retaining JSON escaping and CRLF.
    left = max(raw.rfind(b"\n", 0, start), raw.rfind(b"\\n", 0, start),
               raw.rfind(b". ", 0, start))
    left = 0 if left < 0 else left + (1 if raw[left:left + 1] == b"\n" else 2)
    ends = [p for sep in (b"\n", b"\\n", b". ")
            if (p := raw.find(sep, end)) >= 0]
    right = min(ends) + 1 if ends else len(raw)
    return _sub(source, left, max(right, end))


def _references(later: Mapping[str, Any], trace: Mapping[str, Any],
                selected: Mapping[str, Any], earlier_role: str, target: Mapping[str, Any],
                projection_id: str = ""
                ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    # Whole-contribution tokens have declared grain, not invented record IDs.
    nouns = {"objection": ("objection", "criticism"), "rival": ("rival",),
             "response": ("response", "synthesis response")}[earlier_role]
    patterns = [rb"(?i)\b(?:the |selected )" + re.escape(n.encode()) + rb"\b"
                for n in nouns]
    token_left, token_right = rb"(?<![A-Za-z0-9_.#:/\x80-\xff-])", rb"(?![A-Za-z0-9_.#:/\x80-\xff-])"
    port_prefixes = []
    if re.fullmatch(r"[0-9a-f]{64}", projection_id):
        patterns.append(token_left + rb"(?:" + re.escape(projection_id.encode()) +
                        rb"|" + re.escape(projection_id[:16].encode()) + rb")" + token_right)
    # Port labels come only from the trace's exact selected-input header.
    brief = trace.get("original_brief", "")
    for match in re.finditer(r"## Selected input ([^ \n]+) \(([^)]+)\)", brief):
        if match.group(1) == selected.get("source"):
            port = match.group(2)
            prefix = "h005." + str(trace.get("template_id", "")) + "." + port
            port_prefixes.append(prefix.encode())
            # Consume the complete token before checking it; never backtrack
            # a malformed record suffix into a shorter authored identifier.
            patterns.append(token_left + re.escape(prefix.encode()) +
                            rb"[A-Za-z0-9_.#:/\x80-\xff-]*" + token_right)
    raw = later["text"].encode("utf-8")
    found, unresolved = {}, {}
    for pattern in patterns:
        for match in re.finditer(pattern, raw):
            entry = {"reference": _sub(later, match.start(), match.end()),
                     "passage": _passage(later, match.start(), match.end()),
                     "target_grain": "whole-contribution"}
            token = match.group()
            if any(token.startswith(prefix) for prefix in port_prefixes) and not any(
                    re.fullmatch(re.escape(prefix) +
                                 rb"(?:#[A-Za-z0-9][A-Za-z0-9_.-]*)?", token)
                    for prefix in port_prefixes):
                entry["reason"] = "UNRESOLVED: malformed or extended source reference token"
                unresolved[(match.start(), match.end())] = entry
                continue
            if b"#" in token:
                record_id = token.rsplit(b"#", 1)[1]
                # A lexical authored id anchor, not a repaired/validated FCL record.
                pattern_id = rb'\\?"id\\?"\s*:\s*\\?"' + re.escape(record_id) + rb'\\?"'
                anchors = list(re.finditer(pattern_id, target["text"].encode("utf-8")))
                if len(anchors) != 1:
                    entry["reason"] = "UNRESOLVED: target record not identified uniquely"
                    unresolved[(match.start(), match.end())] = entry
                    continue
                anchor = anchors[0]
                entry["target_grain"] = "authored-record-id-anchor; whole contribution available"
                entry["target_record_id"] = record_id.decode("utf-8")
                entry["target_anchor"] = _sub(target, anchor.start(), anchor.end())
            found[(match.start(), match.end())] = entry
    return ([found[key] for key in sorted(found)],
            [unresolved[key] for key in sorted(unresolved)])


def source_paths(occurrence: Path) -> tuple[Path, ...]:
    """Evidence paths S0 must pin for this adapter, excluding provider records."""
    occurrence = Path(occurrence)
    paths = [occurrence / n for n in ("material.json", "arms.json", "plan.json")
             if (occurrence / n).is_file()]
    for category, suffix in (("responses", "*.txt"), ("traces", "*.json"),
                             ("artifacts", "*.json")):
        paths.extend(sorted((occurrence / category).rglob(suffix)))
    return tuple(paths)


def build_rows(occurrence: Path, *, repo_root: Path) -> list[dict[str, Any]]:
    """Enumerate every declared slot without writing files or minting identities.

    Defaults implement F09's six slots. A prospective material.pair_rows map
    declares branched runner-native F003 treatments; it does not supply evidence.
    """
    occurrence, root = Path(occurrence), Path(repo_root)
    if not occurrence.is_absolute():
        occurrence = root / occurrence
    material_source = _read(occurrence / "material.json", root)
    material = json.loads(material_source["text"])
    declaration = material.get("pair_rows", {})
    groups = declaration.get("groups", DEFAULT_GROUPS)
    tag = declaration.get("source_tag", "")
    problem, cycle = declaration.get("problem", "daily"), declaration.get("cycle", 1)
    if not isinstance(cycle, int) or cycle < 1:
        raise ValueError("pair cycle must be a positive integer")
    if not isinstance(problem, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", problem):
        raise ValueError("unsafe pair problem component")
    if not isinstance(tag, str) or not re.fullmatch(r"[A-Za-z0-9]*", tag):
        raise ValueError("unsafe pair source tag")
    for group in groups:
        for field in ("arm", "code", "objection_node", "rival_node", "response_node", "carry_node"):
            value = group.get(field, "default")
            if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value):
                raise ValueError("unsafe pair coordinate component: " + field)
        if group.get("route", "returned") not in ("returned", "archive-context"):
            raise ValueError("unknown pair route")
    rows = []
    for group in groups:
        arm, code = group["arm"], group["code"]
        for earlier_role, later_role, earlier_code, later_code in POSITIONS:
            earlier = _coord(problem, arm, cycle, group.get(earlier_role + "_node", earlier_role))
            later = _coord(problem, arm, cycle, group.get(later_role + "_node", later_role))
            key_coord = tag + code + later_code
            key = f"h005-row/{key_coord}#u/ref/{earlier_code}"
            archived = group.get("route") == "archive-context" and earlier_role == "objection"
            row = {"schema": SCHEMA, "row_key": key,
                   "key_components": [key_coord, "u", "ref", earlier_code],
                   "pair_position": earlier_role + "->" + later_role,
                   "comparison_position": earlier_code + later_code,
                   "treatment": group.get("treatment", "prior-exposed"),
                   "route": "archive-context" if archived else "declared-input",
                   "earlier_coordinate": earlier, "later_coordinate": later,
                   "admission": "UNRESOLVED", "reason": "source not available",
                   "target": None, "referring": None, "referring_passages": [], "unresolved_references": [],
                   "context": [], "mapping_evidence": [material_source],
                   "uptake_note": "not declared at this whole-contribution grain; authored wording retained verbatim"}
            rows.append(row)
            try:
                target = _read(_path(occurrence, "responses", earlier, ".txt"), root)
                referring = _read(_path(occurrence, "responses", later, ".txt"), root)
                row.update(target=target, referring=referring)
                trace_source = _read(_path(occurrence, "traces", later, ".json"), root)
                artifact_source = _read(_path(occurrence, "artifacts", earlier, ".json"), root)
                later_artifact_source = _read(_path(occurrence, "artifacts", later, ".json"), root)
                trace, artifact = json.loads(trace_source["text"]), json.loads(artifact_source["text"])
                later_artifact = json.loads(later_artifact_source["text"])
                row["mapping_evidence"].extend([trace_source, artifact_source, later_artifact_source])
                account = _path(occurrence, "responses", _coord(problem, arm, cycle, "account"), ".txt")
                if account.is_file() and account != _path(occurrence, "responses", earlier, ".txt"):
                    row["context"].append(_read(account, root))
            except (FileNotFoundError, UnicodeError, json.JSONDecodeError) as exc:
                row["reason"] = "UNRESOLVED: source custody unavailable (" + type(exc).__name__ + ")"
                continue
            if (trace.get("coordinate") != later or artifact.get("coordinate") != earlier
                    or later_artifact.get("coordinate") != later
                    or later_artifact.get("public_text_sha256") != referring["sha256"]
                    or artifact.get("public_text_sha256") != target["sha256"]):
                row["reason"] = "UNRESOLVED: source coordinate or raw-byte hash mismatch"
                continue
            direct = trace.get("rendering") == "direct_explicit_views"
            if direct:
                # Native matched calls have visible_sources, no Mini projections.
                mappings = [(s, s.get("artifact_id", ""))
                            for s in trace.get("visible_sources", [])
                            if s.get("coordinate") == earlier and not s.get("absent", False)]
            else:
                mappings = [(p["selected_source"], p.get("artifact_id", ""))
                            for p in trace.get("projection_artifacts", [])
                            if p.get("selected_source", {}).get("coordinate") == earlier
                            and not p["selected_source"].get("absent", False)]
            if archived:
                # Barrier metadata is not an input port; this candidate can be
                # displayed but is never promoted just because a route was declared.
                row["reason"] = ("UNRESOLVED: declared withheld objection is archive context only"
                                 if not mappings else
                                 "UNRESOLVED: archive declaration conflicts with delivered input")
                continue
            if len(mappings) != 1:
                row["reason"] = "UNRESOLVED: target contribution not uniquely mapped by frozen trace"
                continue
            selected, reference_id = mappings[0]
            if (selected.get("public_text_sha256") != target["sha256"] or
                    selected.get("artifact_id") != artifact.get("artifact_id")):
                row["reason"] = "UNRESOLVED: projection/source custody mismatch"
                continue
            if selected.get("view") != "both":
                row["reason"] = "UNRESOLVED: selected view does not expose both contribution fields"
                continue
            if direct:
                brief = trace.get("original_brief", "")
                header = ("## Selected input " + str(selected.get("source", "")) +
                          "\n\nSource " + str(selected.get("source", "")) + ": " +
                          _coord_key(earlier) + "; selected view: both\nArtifact: " +
                          str(selected.get("artifact_id", "")) + "\n")
                if (trace.get("projection_artifacts") or not isinstance(brief, str) or
                        trace.get("original_brief_sha256") != _sha(brief.encode("utf-8")) or
                        brief.count(header) != 1):
                    row["reason"] = "UNRESOLVED: direct selected-source header or brief custody mismatch"
                    continue
            references, unresolved = _references(referring, trace, selected, earlier_role,
                                                 target, reference_id)
            row["referring_passages"] = references
            row["unresolved_references"] = unresolved
            if not references:
                row["reason"] = "UNRESOLVED: exact referring passage not identified"
                continue
            row["admission"] = "ADMITTED"
            row["reason"] = "Exact whole-contribution reference mapped by frozen source correspondence; use remains unresolved"
    validate_keys(rows)
    return rows


def build_surface(row: Mapping[str, Any]) -> Surface:
    """Quote each whole raw source once; archive/account context stays outside G3.

    A Surface span uses code-point offsets into the named response.txt, with
    source_field='raw_utf8_text'. Adapter spans separately carry raw byte offsets.
    Legacy Offset.source_field is None for these new sides, never 'commitments'.
    """
    if row.get("referring") is None or row.get("target") is None:
        raise ValueError("pair surface requires both authored contributions")
    later_key = _coord_key(row["later_coordinate"])
    earlier_key = _coord_key(row["earlier_coordinate"])
    pieces, spans, cursor = [], [], 0
    regions = [("pair-referring", row["referring"], later_key,
                "Later whole contribution; authored uptake remains as written", True),
               ("pair-target", row["target"], earlier_key,
                "ARCHIVE CONTEXT ONLY: withheld objection; not an operative target"
                if row["route"] == "archive-context" else "Earlier whole contribution",
                row["route"] != "archive-context")]
    for context in row.get("context", []):
        regions.append(("pair-context", context, "context",
                        "Earlier account context only; not an additional pair", False))
    for side, source, coord, title, operative in regions:
        header = ("\n\n[" + title + "; " + source["path"] + "; sha256=" + source["sha256"] +
                  f"; bytes={source['byte_start']}:{source['byte_end']}; " +
                  f"lines={source['line_start']}:{source['line_end']}]\n").encode("utf-8")
        pieces.append(header)
        cursor += len(header)
        content = source["text"].encode("utf-8")
        if _sha(content) != source["sha256"] or source["byte_start"] != 0:
            raise ValueError("pair whole-source hash/span mismatch")
        if operative:
            spans.append(Span(side, cursor, cursor + len(content), source["path"],
                              "raw_utf8_text", source["codepoint_start"],
                              source["codepoint_end"], coord))
        pieces.append(content)
        cursor += len(content)
    return Surface(b"".join(pieces), tuple(spans), later_key, earlier_key,
                   None, None, "pair-position", row["pair_position"],
                   "whole-contribution; " + row["route"])


def raw_offset(row: Mapping[str, Any], offset: Any) -> dict[str, Any]:
    """Prove a resolved guard offset's code-point/raw-byte correspondence."""
    candidates = [row.get("referring"), row.get("target"), *row.get("context", [])]
    source = next((s for s in candidates if s and s["path"] == offset.occurrence_path), None)
    if source is None or offset.file_start is None or offset.file_end is None:
        raise ValueError("offset does not resolve to a declared raw source")
    text = source["text"]
    start = len(text[:offset.file_start].encode("utf-8"))
    end = len(text[:offset.file_end].encode("utf-8"))
    result = _sub(source, start, end)
    material = build_surface(row).text[offset.start:offset.end]
    if material != result["text"].encode("utf-8"):
        raise ValueError("guard/raw offset correspondence failed")
    return result


def juxtapose(rows: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], ...]:
    """Group identical pair positions across declared treatments, in source order.

    Each source keeps its own Surface and unresolved disposition. This is an
    operator/reader comparison interface, not a driver mark or a causal verdict.
    Missing source material has surface=None rather than fabricated text.
    """
    validate_keys(rows)
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (row["later_coordinate"]["arm"], row["pair_position"])
        group = groups.setdefault(key, {"runner_arm": key[0], "pair_position": key[1],
                                        "candidates": []})
        group["candidates"].append({"row_key": row["row_key"],
            "treatment": row["treatment"], "admission": row["admission"],
            "reason": row["reason"],
            "surface": build_surface(row) if row.get("referring") and row.get("target") else None})
    return tuple(groups.values())
