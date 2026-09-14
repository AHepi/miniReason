"""Pins for the operator page, ``docs/workflows/automated-loop.md``.

The page is **generated** from the modules and from the driver's own argument
parser (wave 5); this file is what keeps it true. Every mechanical thing on the
page is pinned against the source it came from - the ceiling block against the
bytes of ``data/ceiling_v1.md``, the failure and block tables against
``types``, the stop vocabulary against ``types.STOP_REASONS``, the argv and the
state table against ``tools/auto_loop.py`` - so a code or a flag added without
regenerating the page fails here.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from minireason.loop import obligations, standard, types  # noqa: E402

if "auto_loop" in sys.modules:
    auto_loop = sys.modules["auto_loop"]
else:
    _spec = importlib.util.spec_from_file_location(
        "auto_loop", REPO / "tools" / "auto_loop.py")
    auto_loop = importlib.util.module_from_spec(_spec)
    # Registered BEFORE exec: ``dataclasses`` resolves a class's own module out
    # of ``sys.modules`` and a module absent from it breaks every @dataclass.
    sys.modules["auto_loop"] = auto_loop
    _spec.loader.exec_module(auto_loop)

PAGE_PATH = REPO / "docs" / "workflows" / "automated-loop.md"


def page() -> str:
    return PAGE_PATH.read_text(encoding="utf-8")


def page_lines() -> list[str]:
    return page().splitlines()


def page_flat() -> str:
    """The page with wrapping folded away, for phrases that may wrap."""
    return " ".join(page().split())


class ThePageExists(unittest.TestCase):

    def test_the_page_is_present_and_non_empty(self):
        self.assertTrue(PAGE_PATH.is_file())
        self.assertGreater(len(page()), 1000, "the operator page is a stub")

    def test_the_sections_are_present(self):
        for heading in (
            "## 1. The command",
            "## 2. The config",
            "## 3. The directory layout",
            "## 4. Failure codes",
            "## 5. Block codes",
            "## 6. The two narrowings",
            "## 7. Concurrency and the gateway wall",
            "## 8. The pre-registration template",
            "## 9. The obligations template",
            "## 10. The claim ceiling, verbatim",
        ):
            self.assertIn(heading, page())


class TheCeilingIsByteIdentical(unittest.TestCase):
    """The page's ceiling block is the file's bytes, no more, no less."""

    def block(self) -> bytes:
        text = page()
        begin = "<!-- CEILING:BEGIN -->\n"
        end = "<!-- CEILING:END -->"
        self.assertEqual(text.count(begin.strip()), 1)
        inner = text.split(begin, 1)[1].split(end, 1)[0]
        if inner.endswith(chr(10)+chr(10)):
            inner = inner[:-1]
        return inner.encode("utf-8")

    def test_the_ceiling_block_is_byte_identical_to_the_shipped_file(self):
        self.assertEqual(
            self.block(), standard.CEILING_PATH.read_bytes(),
            "the page's ceiling block must reproduce data/ceiling_v1.md exactly")

    def test_the_ceiling_block_carries_the_pinned_digest(self):
        self.assertEqual(hashlib.sha256(self.block()).hexdigest(),
                         standard.CEILING_SHA256)

    def test_every_required_ceiling_sentence_is_on_the_page(self):
        for sentence in standard.CEILING_REQUIRED_SENTENCES:
            self.assertIn(sentence, page())


class EveryFailureCodeTheModulesOwnIsOnThePage(unittest.TestCase):

    def test_every_failure_code_is_named_on_the_page(self):
        text = page()
        missing = [code for code in types.FAILURE_CODES if f"`{code}`" not in text]
        self.assertEqual(missing, [],
                         "codes the page must name: " + ", ".join(missing))

    def test_the_failure_table_carries_one_row_per_code(self):
        rows = [line for line in page_lines()
                if line.startswith("| `")
                and ("minireason/loop/" in line or "tools/auto_loop.py" in line)
                and not line.startswith("| `blocked:")]
        seen = set()
        for row in rows:
            code = row.split("`")[1]
            if code in types.FAILURE_CODES:
                seen.add(code)
        self.assertEqual(seen, set(types.FAILURE_CODES))

    def test_every_table_row_names_a_module_that_owns_the_code(self):
        # Every module of the package, read off the tree rather than listed:
        # a wave that adds one must not have to edit this test to be attributed.
        sources = {
            path.stem: path.read_text(encoding="utf-8")
            for path in sorted((REPO / "src/minireason/loop").glob("*.py"))
            if path.stem != "__init__"
        }
        sources["auto_loop"] = (REPO / "tools" / "auto_loop.py").read_text(
            encoding="utf-8")
        for line in page_lines():
            if not line.startswith("| `"):
                continue
            cells = [cell.strip() for cell in line.split("|")]
            if len(cells) < 4:
                continue
            if "minireason/loop/" not in cells[2] and "auto_loop.py" not in cells[2]:
                continue
            code = cells[1].strip("`")
            if code not in types.FAILURE_CODES:
                continue
            owner = cells[2].strip("`").split("/")[-1].removesuffix(".py")
            self.assertIn(code, sources[owner],
                          f"{code} is attributed to {owner} but does not occur there")

    def test_the_parameterised_http_family_is_named(self):
        text = page()
        self.assertIn("`HTTP_<status>`", text)
        self.assertIn("`HTTP_429`", text)

    def test_every_code_the_driver_itself_adds_is_on_the_page(self):
        flat = page_flat()
        for code, reason in auto_loop.NEW_CODES.items():
            with self.subTest(code=code):
                self.assertIn(f"`{code}`", flat)
                # and its one-line reason, as the driver writes it
                self.assertIn(" ".join(reason.split())[:60], flat)
        self.assertIn("Every code the driver itself adds is in this table",
                      flat)


class EveryBlockCodeTheModulesOwnIsOnThePage(unittest.TestCase):

    def test_every_block_code_is_named_on_the_page(self):
        text = page()
        missing = [code for code in types.BLOCK_CODES if f"`{code}`" not in text]
        self.assertEqual(missing, [])

    def test_the_block_table_carries_one_row_per_block_code(self):
        rows = [line for line in page_lines() if line.startswith("| `blocked:")]
        seen = {row.split("`")[1] for row in rows}
        self.assertEqual(seen, set(types.BLOCK_CODES))

    def test_the_nine_ceiling_reasons_are_named(self):
        joined = page()
        for reason in types.CEILING_BLOCK_REASONS:
            self.assertIn(reason, joined, reason)

    def test_constitution_is_named_as_the_one_extra(self):
        self.assertIn("`blocked:constitution`", page())
        self.assertIn("the one extra", page())

    def test_every_stop_reason_and_the_declared_condition_prefix_appear(self):
        text = page()
        for reason in types.STOP_REASONS:
            self.assertIn(f"`{reason}`", text)
        self.assertIn("`preregistered_condition:<id>`", text)

    def test_every_outcome_code_appears(self):
        for code in types.OUTCOME_CODES:
            self.assertIn(f"`{code}`", page())


class TheNarrowingsAndConcurrencyFacts(unittest.TestCase):

    def _design_clause(self) -> str:
        """Design section 6's narrowing clause, read off the FROZEN ceiling.

        The design document is not in this tree and the ceiling is: the clause
        is one of ``CEILING_REQUIRED_SENTENCES``, so quoting it from the bytes
        the plan pins is quoting it from the one owner rather than from a copy.
        """

        flat = " ".join(standard.CEILING_TEXT.split())
        start = flat.index("**Two published instruments were narrowed")
        clause = flat[start:flat.index("**What would reopen this:", start)]
        return " ".join(clause.split())

    def _sentence(self, start_marker: str, end_marker: str) -> str:
        flat = self._design_clause()
        start = flat.index(start_marker)
        return flat[start:flat.index(end_marker, start)]

    def test_the_vocabulary_narrowing_is_quoted_from_design_section_6(self):
        sentence = self._sentence("`ROOT_READING_VOCABULARY`", " And where")
        self.assertIn(sentence, page_flat())

    def test_the_judge_role_narrowing_is_quoted_from_design_section_6(self):
        flat = self._design_clause()
        start = flat.index("And where") + 1  # "where ..." without "And"
        sentence = flat[start:]
        self.assertIn(sentence, page_flat())

    def test_the_two_credential_fact_is_stated(self):
        flat = page_flat()
        self.assertIn("two `key_env` values", flat)
        self.assertIn("5 × 2 = 10", flat)
        self.assertIn("five concurrent calls per credential", flat)

    def test_the_gateway_wall_is_stated(self):
        text = page()
        self.assertIn("300 s gateway wall", text)
        self.assertIn("`PROVIDER_GATEWAY_WALL`", text)
        self.assertIn("roles.GATEWAY_WALL_SECONDS", text)


class TheTemplatesAndMarkers(unittest.TestCase):

    def test_the_preregistration_template_names_every_declared_field(self):
        flat = page_flat()
        for term in ("budget", "Stop conditions", "Reading set", "**O and P**",
                     "**Falsifiers**", "**Would-reopen**", "cycle_budget",
                     "max_calls", "reading_set[]", "reopen_reasons[]",
                     "what would reopen"):
            self.assertIn(term, flat, term)

    def test_the_obligations_template_mirrors_the_module_schema(self):
        text = page()
        self.assertIn(f'"{obligations.OBLIGATIONS_SCHEMA}"', text)
        for key in obligations.OBLIGATION_KEYS:
            self.assertIn(f'"{key}"', text)
        for name in sorted(obligations.PREDICATES):
            self.assertIn(f"`obligations.{name}`", text, name)

    def test_the_layout_block_is_the_design_layout(self):
        for line in (
            "config.json  preregistration.md  obligations.json  CEILING.md  plan.json",
            "steps/NNNN-KIND.json[.open]",
            "cycles/cycle-NN/{import,use-table,readings,contrast,decision.json,CYCLE.md}",
            "readings/<row_key>/{requests,attempts,responses,provider}/...",
            "audits/  appeals/  errata/  CLOSING.md  READING_TABLE.md  COMPARISON.md",
        ):
            self.assertIn(line, page())

    def test_every_subcommand_and_flag_of_the_driver_is_on_the_page(self):
        parser = auto_loop._parser()
        sub = [action for action in parser._actions
               if isinstance(action, argparse._SubParsersAction)][0]
        flat = page_flat()
        for name, entry in sub.choices.items():
            with self.subTest(command=name):
                self.assertIn(name, flat)
                for action in entry._actions:
                    for option in action.option_strings:
                        if option in ("-h", "--help"):
                            continue
                        self.assertIn(option, flat, f"{name} {option}")

    def test_every_state_names_the_function_that_runs_it(self):
        flat = page_flat()
        for label, kind, function in auto_loop.STATE_RESPONSIBILITIES:
            with self.subTest(state=label):
                self.assertIn(f"| {label} | `{kind}` | `auto_loop.{function}` |",
                              " ".join(page().split("\n")))
        self.assertIn("`AUDIT`", flat)

    def test_the_resource_boundary_discipline_is_stated(self):
        text = page()
        self.assertIn("resource boundary", text.lower())
        self.assertIn("`resource_boundary`", text)
        # the one token the loop never claims appears only inside the
        # ceiling's own denial sentence and where the denial is discussed
        hits = standard.CEILING_EXHAUSTION_DENIAL
        for line in page_lines():
            if "exhaust" not in line.casefold():
                continue
            if hits in line:
                continue
            self.assertIn("never claims", line, f"unauthorised use: {line}")


if __name__ == "__main__":
    unittest.main()
