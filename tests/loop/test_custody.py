"""Tests for ``minireason.loop.custody`` (wave-plan module ``W0-CUSTODY``).

Each clause of the module's acceptance list has a test named after it:

* ``A one-byte change to any pinned file is detected and named``
* ``a path escaping the run root is refused``
* ``write_new refuses an existing path``
* ``write_new ... refuses credential-bearing content``
* ``verify_pins is pure and order-stable``

Everything is done in a temporary directory: no test here reads, writes or
depends on a tracked file of this repository except the custody module's own
source, which one test scans read-only for the codes it can emit.  No
credential is ever written: the only values put into ``os.environ`` are
obvious fakes, and they are removed again by ``patch.dict``.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from minireason.loop import custody
from minireason.loop.types import LoopError
from minireason.loop.custody import (
    CUSTODY_CODES,
    CredentialInOutput,
    CustodyFinding,
    CustodyMismatch,
    WriteOnceViolation,
    credential_names_in,
    digest,
    encoded,
    fenced,
    pins,
    sha256_bytes,
    sha256_path,
    verify_pins,
    write_new,
)

#: Obvious non-credentials, long enough to clear ``MIN_CREDENTIAL_LENGTH``.
FAKE_SECRET = "FAKE_CUSTODY_TEST_SECRET_0123456789abcdef"
FAKE_SECRET_WITH_QUOTE = 'FAKE"CUSTODY_TEST_SECRET_0123456789abcdef'

CONFIG_FIXTURE = {
    "run_id": "LOOP-01",
    "study": "h005",
    "occurrences": ["experiments/h005/occurrence-01"],
    "runner": "tools/multicycle_commitment_study_multi_v2.py",
    "cycle_budget": 3,
    "max_calls": 240,
    "reading_set": ["p1/mini_fcl/cycle-1/n1#r3"],
    "obligations_path": "experiments/loops/LOOP-01/obligations.json",
    "graph_root": "experiments/loops/LOOP-01/graph",
    "reopen_reasons": ["new-material", "repaired-guard", "appellate-ruling"],
    "audit": {
        "period": 2,
        "judge_err_max": 0.2,
        "judge_err_max_account": "one anchor of the five-anchor calibration set",
        "streak_max": 5,
        "streak_max_account": "longer than any block run the dry run produced",
    },
}

PINNED = {
    "tools/runner.py": b"# runner v2\nprint('one')\n",
    "src/minireason/use_relation_h005.py": b"BANNER = 'the reading is roots'\n",
    "CEILING.md": b"# ceiling\r\nfrozen\r\n",
    "data/endpoints.json": b'{"e": {"family": "f"}}\n',
}


class _Tree(unittest.TestCase):
    """A temporary repository tree carrying the files a loop plan pins."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="loop-custody-")
        self.addCleanup(self._tmp.cleanup)
        self.repo = Path(self._tmp.name) / "repo"
        for name, raw in PINNED.items():
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        self.names = sorted(PINNED)
        self.plan = {"loop_plan_id": "x" * 64, "pins": pins(self.repo, self.names)}


# ------------------------------------------------------- acceptance clauses

class OneByteChangeIsDetectedAndNamed(_Tree):

    def test_a_one_byte_change_to_any_pinned_file_is_detected_and_named(self) -> None:
        self.assertEqual(verify_pins(self.plan, self.repo), [])
        for name, original in PINNED.items():
            with self.subTest(pinned=name):
                path = self.repo / name
                path.write_bytes(original[:-1] + bytes([original[-1] ^ 0x01]))
                findings = verify_pins(self.plan, self.repo)
                self.assertEqual(len(findings), 1, findings)
                finding = findings[0]
                self.assertEqual(finding.code, "SOURCE_PIN_MISMATCH")
                self.assertEqual(finding.path, name)
                self.assertEqual(finding.expected, self.plan["pins"][name])
                self.assertEqual(finding.observed, sha256_path(path))
                self.assertNotEqual(finding.expected, finding.observed)
                self.assertIn(name, str(finding))
                self.assertEqual(finding.as_dict()["path"], name)
                path.write_bytes(original)
        self.assertEqual(verify_pins(self.plan, self.repo), [])

    def test_a_missing_or_replaced_pinned_file_is_detected_and_named(self) -> None:
        (self.repo / "CEILING.md").unlink()
        (self.repo / "data" / "endpoints.json").unlink()
        (self.repo / "data" / "endpoints.json").mkdir()
        findings = {f.path: f.code for f in verify_pins(self.plan, self.repo)}
        self.assertEqual(findings, {"CEILING.md": "SOURCE_PIN_MISSING",
                                    "data/endpoints.json": "SOURCE_PIN_NOT_A_FILE"})

    def test_a_pin_key_that_escapes_the_repository_is_named_not_followed(self) -> None:
        outside = Path(self._tmp.name) / "outside.md"
        outside.write_bytes(b"not the repository\n")
        plan = {"pins": {"../outside.md": sha256_path(outside),
                         "/etc/hostname": "0" * 64}}
        findings = verify_pins(plan, self.repo)
        self.assertEqual([f.code for f in findings],
                         ["SOURCE_PIN_OUTSIDE_REPOSITORY"] * 2)

    def test_a_malformed_pin_value_is_named_rather_than_compared(self) -> None:
        plan = {"pins": dict(self.plan["pins"], **{"CEILING.md": "not-a-sha"})}
        self.assertEqual([(f.code, f.path) for f in verify_pins(plan, self.repo)],
                         [("SOURCE_PIN_MALFORMED", "CEILING.md")])


class PathEscapingTheRunRootIsRefused(_Tree):

    def test_a_path_escaping_the_run_root_is_refused(self) -> None:
        root = Path(self._tmp.name) / "run"
        root.mkdir()
        (root / "link").symlink_to(Path(self._tmp.name), target_is_directory=True)
        for escape in ("..", "../elsewhere", "steps/../../elsewhere",
                       str(Path(self._tmp.name) / "elsewhere"), "/etc/hostname",
                       "link/elsewhere"):
            with self.subTest(path=escape):
                with self.assertRaises(CustodyMismatch) as caught:
                    fenced(root, escape)
                self.assertEqual(caught.exception.code, "PATH_ESCAPES_RUN_ROOT")
                self.assertIn(escape, str(caught.exception))

    def test_fenced_accepts_a_path_inside_the_run_root(self) -> None:
        root = Path(self._tmp.name) / "run"
        (root / "steps").mkdir(parents=True)
        self.assertEqual(fenced(root, "steps/0001-SEND.json"),
                         root.resolve() / "steps" / "0001-SEND.json")
        self.assertEqual(fenced(root, root / "errata" / "e.md"),
                         root.resolve() / "errata" / "e.md")
        self.assertEqual(fenced(root, ""), root.resolve())
        self.assertEqual(fenced(root, "."), root.resolve())


class WriteNewRefusesAnExistingPath(_Tree):

    def test_write_new_refuses_an_existing_path(self) -> None:
        target = Path(self._tmp.name) / "run" / "steps" / "0001-SEND.json"
        write_new(target, {"kind": "SEND", "status": "COMPLETE"})
        first = target.read_bytes()
        with self.assertRaises(CustodyMismatch) as caught:
            write_new(target, {"kind": "SEND", "status": "FAILED"})
        self.assertEqual(caught.exception.code, "WRITE_ONCE_VIOLATION")
        self.assertIsInstance(caught.exception, WriteOnceViolation)
        self.assertIsInstance(caught.exception, FileExistsError)
        self.assertEqual(target.read_bytes(), first)

    def test_write_new_refuses_an_existing_directory_or_symlink(self) -> None:
        root = Path(self._tmp.name) / "run"
        (root / "steps").mkdir(parents=True)
        (root / "dangling").symlink_to(root / "never-created")
        for target in (root / "steps", root / "dangling"):
            with self.subTest(target=target.name):
                with self.assertRaises(WriteOnceViolation):
                    write_new(target, {"k": 1})

    def test_write_new_fsyncs_the_file_and_then_its_parent_directory(self) -> None:
        """N2: the bytes were durable and the NAME was not.

        The docstring's promise is that "a receipt that resolves a spent call must
        survive the process". A crash between the file's ``fsync`` and the
        directory entry reaching disk leaves durable bytes under a name the
        directory never committed - a spent call with no receipt, which is the one
        thing this function exists to prevent.
        """

        target = Path(self._tmp.name) / "run" / "steps" / "0007-SEND.json"
        synced: list[str] = []
        real_fsync, real_open = os.fsync, os.open
        handles: dict[int, str] = {}

        def recording_open(path, flags, *args, **kwargs):
            fileno = real_open(path, flags, *args, **kwargs)
            handles[fileno] = str(path)
            return fileno

        def recording_fsync(fileno):
            synced.append(handles.get(fileno, "<file>"))
            return real_fsync(fileno)

        with patch.object(custody.os, "open", recording_open), \
                patch.object(custody.os, "fsync", recording_fsync):
            write_new(target, {"kind": "SEND"})

        self.assertEqual(target.read_bytes(), encoded({"kind": "SEND"}))
        self.assertEqual(synced[-1], str(target.parent),
                         "the parent directory is fsynced after the file")
        self.assertEqual(len(synced), 2, synced)

    def test_a_directory_fsync_the_platform_refuses_does_not_fail_the_write(self) -> None:
        target = Path(self._tmp.name) / "run" / "steps" / "0008-SEND.json"
        real_open = custody.os.open

        def refuse_a_directory(path, flags, *rest):
            # Only the directory handle is refused: the record's own bytes are
            # written through the same call, and a platform that cannot open a
            # directory can still write a file.
            if Path(path).is_dir():
                raise OSError("no directory fd")
            return real_open(path, flags, *rest)

        with patch.object(custody.os, "open", side_effect=refuse_a_directory):
            write_new(target, {"kind": "SEND"})
        self.assertEqual(target.read_bytes(), encoded({"kind": "SEND"}))

    def test_write_new_writes_bytes_verbatim_and_values_as_canonical_json(self) -> None:
        root = Path(self._tmp.name) / "run"
        write_new(root / "CEILING.md", b"line\r\nkept\r\n")
        self.assertEqual((root / "CEILING.md").read_bytes(), b"line\r\nkept\r\n")
        write_new(root / "cycles" / "decision.json", {"b": 1, "a": [2, 3]})
        raw = (root / "cycles" / "decision.json").read_bytes()
        self.assertEqual(raw, b'{\n  "a": [\n    2,\n    3\n  ],\n  "b": 1\n}\n')
        self.assertEqual(raw, encoded({"b": 1, "a": [2, 3]}))
        self.assertEqual(json.loads(raw), {"a": [2, 3], "b": 1})


class WriteNewRefusesCredentialBearingContent(_Tree):

    def _target(self, name: str = "record.json") -> Path:
        return Path(self._tmp.name) / "run" / "readings" / name

    def test_write_new_refuses_credential_bearing_content(self) -> None:
        target = self._target()
        with patch.dict(os.environ, {"OLLAMA_API_KEY": FAKE_SECRET}, clear=False):
            with self.assertRaises(CustodyMismatch) as caught:
                write_new(target, {"request": {"headers": "Bearer " + FAKE_SECRET}})
            self.assertEqual(caught.exception.code, "CREDENTIAL_IN_OUTPUT")
            self.assertIsInstance(caught.exception, CredentialInOutput)
            self.assertIsInstance(caught.exception, ValueError)
            self.assertIn("OLLAMA_API_KEY", str(caught.exception))
            self.assertNotIn(FAKE_SECRET, str(caught.exception))
            self.assertFalse(target.exists())
            self.assertFalse(target.parent.exists())
            with self.assertRaises(CustodyMismatch):
                write_new(self._target("raw.txt"), FAKE_SECRET.encode("utf-8"))
            self.assertFalse(self._target("raw.txt").exists())

    def test_write_new_refuses_a_credential_in_its_json_escaped_rendering(self) -> None:
        target = self._target()
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": FAKE_SECRET_WITH_QUOTE}, clear=False):
            raw = encoded({"prompt": FAKE_SECRET_WITH_QUOTE})
            self.assertNotIn(FAKE_SECRET_WITH_QUOTE.encode("utf-8"), raw)
            self.assertEqual(credential_names_in(raw), ["DEEPSEEK_API_KEY"])
            with self.assertRaises(CredentialInOutput):
                write_new(target, {"prompt": FAKE_SECRET_WITH_QUOTE})
        self.assertFalse(target.exists())

    def test_write_new_admits_content_carrying_no_credential(self) -> None:
        target = self._target()
        with patch.dict(os.environ, {"OLLAMA_API_KEY": FAKE_SECRET}, clear=False):
            self.assertEqual(credential_names_in(b"no credential here"), [])
            write_new(target, {"seat": "judge", "key_env": "OLLAMA_API_KEY"})
        self.assertEqual(json.loads(target.read_bytes())["key_env"], "OLLAMA_API_KEY")

    def test_a_value_below_the_credential_floor_is_not_treated_as_a_secret(self) -> None:
        target = self._target()
        with patch.dict(os.environ, {"OLLAMA_API_KEY": "x"}, clear=False):
            write_new(target, {"note": "xxxxx"})
        self.assertTrue(target.exists())


class VerifyPinsIsPureAndOrderStable(_Tree):

    def test_verify_pins_is_pure_and_order_stable(self) -> None:
        (self.repo / "CEILING.md").write_bytes(b"# ceiling\r\nedited\r\n")
        (self.repo / "tools" / "runner.py").unlink()
        forward = {"pins": {name: self.plan["pins"][name] for name in self.names}}
        backward = {"pins": {name: self.plan["pins"][name] for name in reversed(self.names)}}
        before = json.dumps(forward, sort_keys=True)
        first = verify_pins(forward, self.repo)
        self.assertEqual(first, verify_pins(forward, self.repo))
        self.assertEqual(first, verify_pins(backward, self.repo))
        self.assertEqual([(f.path, f.code) for f in first],
                         [("CEILING.md", "SOURCE_PIN_MISMATCH"),
                          ("tools/runner.py", "SOURCE_PIN_MISSING")])
        self.assertEqual(first, sorted(first, key=lambda f: (f.path, f.code)))
        self.assertEqual(json.dumps(forward, sort_keys=True), before)
        self.assertEqual(list(forward["pins"]), self.names)

    def test_verify_pins_writes_nothing_into_the_tree_it_checks(self) -> None:
        before = sorted(p.relative_to(self.repo).as_posix() for p in self.repo.rglob("*"))
        verify_pins(self.plan, self.repo)
        after = sorted(p.relative_to(self.repo).as_posix() for p in self.repo.rglob("*"))
        self.assertEqual(before, after)

    def test_verify_pins_normalises_a_pin_key_frozen_with_windows_separators(self) -> None:
        """REC-20260913-I: a verification failed on separator spelling alone."""

        plan = {"pins": {name.replace("/", "\\"): sha for name, sha in self.plan["pins"].items()}}
        self.assertEqual(verify_pins(plan, self.repo), [])

    def test_verify_pins_refuses_a_plan_that_carries_no_pin_map(self) -> None:
        bare = dict(self.plan["pins"])
        for plan in ({"loop_plan_id": "x" * 64}, {"pins": ["a"]}, {}, bare):
            with self.subTest(plan=plan):
                with self.assertRaises(CustodyMismatch) as caught:
                    verify_pins(plan, self.repo)
                self.assertEqual(caught.exception.code, "PIN_MAP_MISSING")


# ------------------------------------------------------ supporting coverage

class PinsAreContentAddressed(_Tree):

    def test_pins_are_sorted_content_addresses_of_the_named_files(self) -> None:
        computed = pins(self.repo, reversed(self.names))
        self.assertEqual(list(computed), self.names)
        self.assertEqual(computed, self.plan["pins"])
        self.assertEqual(encoded(computed), encoded(pins(self.repo, self.names)))
        for name, raw in PINNED.items():
            self.assertEqual(computed[name], sha256_bytes(raw))

    def test_pins_accepts_an_absolute_path_inside_the_repository(self) -> None:
        self.assertEqual(pins(self.repo, [self.repo / "CEILING.md"]),
                         {"CEILING.md": self.plan["pins"]["CEILING.md"]})

    def test_pins_refuses_what_it_cannot_freeze(self) -> None:
        cases = {"../outside.md": "SOURCE_PIN_OUTSIDE_REPOSITORY",
                 "/etc/hostname": "SOURCE_PIN_OUTSIDE_REPOSITORY",
                 "tools": "SOURCE_PIN_NOT_A_FILE",
                 "tools/absent.py": "SOURCE_PIN_MISSING"}
        for name, code in cases.items():
            with self.subTest(path=name):
                with self.assertRaises(CustodyMismatch) as caught:
                    pins(self.repo, [name])
                self.assertEqual(caught.exception.code, code)


#: One fixture for the three digest paths: unsorted keys, nesting, non-ASCII
#: above and below the BMP, an empty container, and every JSON scalar type.
SHARED_FIXTURE = {
    "zeta": ["π\U0001f680", "", None],
    "alpha": {"nested": {"b": True, "a": False}, "empty": {}},
    "middle": 42,
    "float": 0.5,
    "text": "café — dash",
}


class DigestHelpers(unittest.TestCase):

    def test_digest_is_the_transport_modules_identity_digest(self) -> None:
        from minireason import provider_openai_compat as transport
        value = {"b": [1, 2], "a": "é"}
        self.assertEqual(digest(value), transport.digest(value))
        self.assertEqual(custody.MIN_CREDENTIAL_LENGTH, transport._MIN_SECRET_LENGTH)

    def test_encoded_is_the_drivers_record_encoding(self) -> None:
        self.assertEqual(encoded({"a": "é"}), '{\n  "a": "é"\n}\n'.encode("utf-8"))
        self.assertEqual(sha256_bytes(b""), hashlib_empty())

    def test_the_three_digest_paths_are_byte_identical_on_one_shared_fixture(self) -> None:
        """Wave-0 integration decision 7.

        W0-CUSTODY hashes ``json.dumps(sort_keys, compact, ensure_ascii=False)``;
        W0-TYPES hashes ``deepreason_core.canonical.canonical_json``; the
        transport has its own ``digest``. All three must agree, or a digest
        taken by the loop and one taken by runner v2 name different things.
        """

        from deepreason_core.canonical import canonical_json, sha256_hex
        from minireason import provider_openai_compat as transport

        compact = json.dumps(SHARED_FIXTURE, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode("utf-8")
        # (1) The bytes W0-TYPES hashes are the bytes W0-CUSTODY hashes.
        self.assertEqual(canonical_json(SHARED_FIXTURE), compact)
        # (2) The hex the three paths produce is one string.
        self.assertEqual(digest(SHARED_FIXTURE), sha256_bytes(compact))
        self.assertEqual(digest(SHARED_FIXTURE), sha256_hex(canonical_json(SHARED_FIXTURE)))
        self.assertEqual(digest(SHARED_FIXTURE), transport.digest(SHARED_FIXTURE))
        # (3) W0-TYPES' own identities are built on exactly that path, so a
        #     recomputation by hand reproduces loop_plan_id bit for bit.
        from minireason.loop.types import (PINNED_SOURCE_PATHS, PLAN_ID_SCHEMA,
                                           LoopConfig, loop_plan_id)
        config = LoopConfig.from_mapping(CONFIG_FIXTURE)
        # The identity requires every fixed pin (types item 18), so the map a
        # recomputation by hand uses names all six and one run-specific file.
        pins_map = {path: "a" * 64 for path in PINNED_SOURCE_PATHS}
        pins_map["tools/runner.py"] = "b" * 64
        pins_map = dict(sorted(pins_map.items()))
        self.assertEqual(
            loop_plan_id(config, pins_map),
            sha256_hex(canonical_json({"schema": PLAN_ID_SCHEMA,
                                       "config": config.as_dict(),
                                       "pins": pins_map})))
        # (4) Key ORDER is not part of any of the three identities.
        reordered = {k: SHARED_FIXTURE[k] for k in reversed(list(SHARED_FIXTURE))}
        self.assertEqual(digest(reordered), digest(SHARED_FIXTURE))
        self.assertEqual(canonical_json(reordered), canonical_json(SHARED_FIXTURE))

    def test_encoded_is_a_different_encoding_that_addresses_the_same_value(self) -> None:
        # ``encoded`` is the drivers' *record* form (indent=2, trailing newline),
        # deliberately NOT the digest form; it must still round-trip to a value
        # the digest paths agree on, or a written record and its pin disagree.
        raw = encoded(SHARED_FIXTURE)
        self.assertNotEqual(raw, json.dumps(SHARED_FIXTURE, ensure_ascii=False,
                                            sort_keys=True,
                                            separators=(",", ":")).encode("utf-8"))
        self.assertEqual(raw[-1:], b"\n")
        self.assertEqual(json.loads(raw), SHARED_FIXTURE)
        self.assertEqual(digest(json.loads(raw)), digest(SHARED_FIXTURE))
        self.assertEqual(encoded(SHARED_FIXTURE), encoded(dict(SHARED_FIXTURE)))


class DeclaredCodes(unittest.TestCase):

    def test_every_code_the_module_can_emit_is_declared_in_custody_codes(self) -> None:
        source = Path(custody.__file__).read_text(encoding="utf-8")
        emitted = set(re.findall(
            r"(?:CustodyMismatch|CredentialInOutput|WriteOnceViolation|CustodyFinding)"
            r"\(\s*\"([A-Z0-9_]+)\"", source))
        self.assertTrue(emitted)
        self.assertEqual(emitted - set(CUSTODY_CODES), set())
        self.assertEqual(set(CUSTODY_CODES) - emitted, set())
        self.assertEqual(list(CUSTODY_CODES), sorted(set(CUSTODY_CODES)))

    def test_the_public_interface_of_the_wave_plan_entry_is_exported(self) -> None:
        for name in ("pins", "verify_pins", "write_new", "fenced", "CustodyMismatch"):
            self.assertIn(name, custody.__all__)
            self.assertTrue(hasattr(custody, name))
        for name in custody.__all__:
            self.assertTrue(hasattr(custody, name), name)

    def test_a_custody_finding_is_json_ready(self) -> None:
        finding = CustodyFinding("SOURCE_PIN_MISMATCH", "CEILING.md", "a" * 64, "b" * 64)
        self.assertEqual(json.loads(json.dumps(finding.as_dict()))["code"],
                         "SOURCE_PIN_MISMATCH")


def hashlib_empty() -> str:
    import hashlib
    return hashlib.sha256(b"").hexdigest()


class HardeningFindings(_Tree):
    """One test per item of the wave-1 integration decisions, items 33-37."""

    def test_item33_a_planted_symlink_never_receives_a_records_bytes(self):
        """Item 33: ``write_new(fenced(root, rel), value)`` wrote THROUGH a link.

        ``fenced`` returns the resolved path, so ``write_new``'s symlink check
        had nothing left to see: the record landed at the link's target and the
        true owner of that coordinate was later refused as spent.
        """

        run = Path(self._tmp.name) / "run"
        (run / "steps").mkdir(parents=True)
        (run / "cycles" / "1").mkdir(parents=True)
        elsewhere = run / "cycles" / "1" / "decision.json"
        (run / "steps" / "0001-SEND.json").symlink_to(elsewhere)

        coordinate = custody.fenced(run, "steps/0001-SEND.json")
        with self.assertRaises(WriteOnceViolation) as caught:
            write_new(coordinate, {"step": "0001-SEND"})
        self.assertEqual(caught.exception.code, "WRITE_ONCE_VIOLATION")
        self.assertFalse(elsewhere.exists(), "the link's target was written")
        # The true owner of the other coordinate is still free to write it.
        write_new(elsewhere, {"cycle": 1})
        self.assertEqual(json.loads(elsewhere.read_text(encoding="utf-8")),
                         {"cycle": 1})
        # ... and no stray temporary is left behind either way.
        self.assertEqual(sorted(p.name for p in (run / "cycles" / "1").iterdir()),
                         ["decision.json"])

    def test_item34_a_pin_value_with_trailing_whitespace_is_malformed(self):
        """Item 34: ``$`` matched before a trailing newline.

        ``"<64 hex>\\n"`` passed the shape gate and was reported as
        ``SOURCE_PIN_MISMATCH`` - a statement about the tree that was false.
        """

        name = self.names[0]
        good = self.plan["pins"][name]
        for suffix in ("\n", "\r\n", " ", "\t", "\x0b"):
            with self.subTest(suffix=repr(suffix)):
                plan = {"pins": {name: good + suffix}}
                findings = verify_pins(plan, self.repo)
                self.assertEqual([f.code for f in findings], ["SOURCE_PIN_MALFORMED"])
                self.assertIsNone(findings[0].observed)
        # The clean digest still verifies.
        self.assertEqual(verify_pins({"pins": {name: good}}, self.repo), [])

    def test_item34_custody_and_types_agree_on_the_pin_value_shape(self):
        from minireason.loop import types as loop_types

        name = self.names[0]
        good = self.plan["pins"][name]
        pinned = {path: good for path in loop_types.PINNED_SOURCE_PATHS}
        for value in (good + "\n", good + " ", good.upper(), good[:-1], good + "a",
                      "not-a-sha"):
            with self.subTest(value=repr(value)[:24]):
                # types refuses it outright ...
                with self.assertRaises(loop_types.LoopError) as caught:
                    loop_types.loop_plan_id(CONFIG_FIXTURE, dict(pinned, **{name: value}))
                self.assertEqual(caught.exception.code, "PIN_INVALID")
                # ... and custody names it malformed rather than compared.
                findings = verify_pins({"pins": {name: value}}, self.repo)
                self.assertEqual([f.code for f in findings], ["SOURCE_PIN_MALFORMED"])

    def test_item35_every_refusal_is_a_loop_error_with_a_custody_code(self):
        """Item 35: ValueError, OSError, RuntimeError, FileExistsError escaped."""

        root = Path(self._tmp.name) / "escapes"
        root.mkdir()
        (root / "loop-a").symlink_to(root / "loop-b")
        (root / "loop-b").symlink_to(root / "loop-a")
        (root / "file").write_bytes(b"x\n")
        calls = (
            ("fenced NUL", lambda: custody.fenced(root, "a\x00b")),
            ("fenced symlink loop", lambda: custody.fenced(root, "loop-a")),
            ("pins NUL", lambda: pins(root, ["a\x00b"])),
            ("pins symlink loop", lambda: pins(root, ["loop-a"])),
            ("write into a symlink loop",
             lambda: write_new(root / "loop-a", {"a": 1})),
            ("write under a file",
             lambda: write_new(root / "file" / "deeper.json", {"a": 1})),
            ("write a long name", lambda: write_new(root / ("x" * 5000), {"a": 1})),
            ("digest of a non-JSON value", lambda: custody.digest({"a": object()})),
            ("write a non-JSON value", lambda: write_new(root / "n.json", object())),
        )
        for label, call in calls:
            with self.subTest(call=label):
                with self.assertRaises(LoopError) as caught:
                    call()
                self.assertIn(caught.exception.code, CUSTODY_CODES)
        # verify_pins turns the same conditions into findings, not escapes.
        for key in ("loop-a", "a\x00b", "x" * 5000):
            with self.subTest(pin=key[:12]):
                findings = verify_pins({"pins": {key: "a" * 64}}, root)
                self.assertEqual(len(findings), 1)
                self.assertIn(findings[0].code, CUSTODY_CODES)

    def test_item36a_a_narrowed_credential_scan_refuses_instead_of_writing(self):
        """Item 36(a): the scan narrowed to two names in silence."""

        self.assertTrue(custody.credential_scan_is_complete())
        target = Path(self._tmp.name) / "run" / "record.json"
        with patch.object(custody, "_provider_module", return_value=None):
            self.assertFalse(custody.credential_scan_is_complete())
            self.assertEqual(custody.scanned_credential_envs(),
                             tuple(sorted(custody.ALWAYS_SCANNED_ENVS)))
            with self.assertRaises(CustodyMismatch) as caught:
                write_new(target, {"a": 1})
            self.assertEqual(caught.exception.code, "CREDENTIAL_SCAN_INCOMPLETE")
        self.assertFalse(target.exists())
        write_new(target, {"a": 1})
        self.assertTrue(target.exists())

    def test_item36b_a_crash_mid_write_leaves_no_truncated_record(self):
        """Item 36(b): the record was written in place, under its own name."""

        target = Path(self._tmp.name) / "run" / "steps" / "0001-SEND.json"
        target.parent.mkdir(parents=True)
        real_link = custody.os.link

        def die(src, dst):
            raise OSError("the machine stopped")

        with patch.object(custody.os, "link", side_effect=die):
            with self.assertRaises(CustodyMismatch) as caught:
                write_new(target, {"step": "0001-SEND"})
        self.assertEqual(caught.exception.code, "RECORD_WRITE_FAILED")
        self.assertFalse(target.exists(), "a name appeared for a record that failed")
        self.assertEqual(list(target.parent.iterdir()), [],
                         "a temporary was left in the tree")
        self.assertIs(custody.os.link, real_link)
        # The coordinate is still free, which is what write-once must leave.
        write_new(target, {"step": "0001-SEND"})
        self.assertEqual(json.loads(target.read_text(encoding="utf-8")),
                         {"step": "0001-SEND"})

    def test_item36c_a_plan_key_outside_the_plans_key_space_is_named(self):
        """Item 36(c): verify_pins called clean what loop_plan_id refuses."""

        name = self.names[0]
        good = self.plan["pins"][name]
        for key, code in ((f"./{name}", "SOURCE_PIN_MALFORMED"),
                          (f"{name}/", "SOURCE_PIN_MALFORMED"),
                          (f" {name}", "SOURCE_PIN_MALFORMED"),
                          (str(self.repo / name), "SOURCE_PIN_MALFORMED"),
                          (f"../{name}", "SOURCE_PIN_OUTSIDE_REPOSITORY"),
                          ("/etc/hostname", "SOURCE_PIN_OUTSIDE_REPOSITORY")):
            with self.subTest(key=key):
                findings = verify_pins({"pins": {key: good}}, self.repo)
                self.assertEqual([f.code for f in findings], [code])
        # Deviation 2 survives: a backslash-spelled map still verifies.
        self.assertEqual(
            verify_pins({"pins": {n.replace("/", "\\"): s
                                  for n, s in self.plan["pins"].items()}}, self.repo),
            [])

    def test_item37_the_finding_order_is_stable_beyond_the_string_keys(self):
        findings = verify_pins(self.plan, self.repo)
        self.assertEqual(findings, [])
        rows = [
            custody.CustodyFinding("SOURCE_PIN_MISMATCH", "a", "1" * 64, "2" * 64),
            custody.CustodyFinding("SOURCE_PIN_MISMATCH", "a", "1" * 64, "3" * 64),
            custody.CustodyFinding("SOURCE_PIN_MISMATCH", "a", "0" * 64, "9" * 64),
        ]
        key = lambda f: (f.path, f.code, f.expected or "", f.observed or "")
        self.assertEqual([key(f) for f in sorted(rows, key=key)],
                         sorted(key(f) for f in rows))

    def test_item37_a_pin_addresses_bytes_and_not_an_inode(self):
        name = self.names[0]
        real = self.repo / name
        raw = real.read_bytes()
        moved = self.repo / "moved.bin"
        moved.write_bytes(raw)
        real.unlink()
        real.symlink_to(moved)
        self.assertEqual(verify_pins({"pins": {name: self.plan["pins"][name]}},
                                     self.repo), [])


CONFIG_FIXTURE = {
    "run_id": "loop-001",
    "study": "C001",
    "occurrences": ["experiments/occurrences/c001-a"],
    "runner": "tools/multicycle_commitment_study_multi_v2.py",
    "cycle_budget": 3,
    "max_calls": 120,
    "reading_set": ["row-1"],
    "obligations_path": "experiments/loops/loop-001/obligations.json",
    "graph_root": "experiments/loops/loop-001/graph",
    "reopen_reasons": ["new-material"],
    "audit": {
        "period": 2,
        "judge_err_max": 0.2,
        "streak_max": 3,
        "judge_err_max_account": "0.2 is one wrong anchor of five; see design 2.5.",
        "streak_max_account": "Three blocked cycles in a row is an instrument fault.",
    },
}


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
