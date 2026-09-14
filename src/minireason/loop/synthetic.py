"""Synthetic occurrence and canned offline deliveries for the dry-run gate.

Purpose
-------
`auto_loop dry-run` is the build's acceptance gate: the whole machine walked
offline, every provider an :class:`~minireason.provider_openai_compat.OfflineProvider`,
every git operation against a real bare repository, and each failure the gate
must assert *induced on purpose* rather than waited for. This module is the
material half of that gate. It builds, from a seed and nothing else, one small
H005 occurrence directory whose deliveries import cleanly through
:mod:`minireason.graph_import_h005` and yield a use table carrying at least one
row per published reading-vocabulary value; it serves the scripted role outputs
the loop's five seats would otherwise have to spend a credential to obtain; and
it names, by code, every failure it can induce.

Nothing here reaches a socket, reads a credential or writes one. The two
declared endpoint families are fictions (`synthetic/alpha-family`,
`synthetic/beta-family`) at `.invalid` hosts, and the two declared `key_env`
NAMES (:data:`SYNTHETIC_KEY_ENVS`) are names this repository never sets and
never will; no value of any environment variable is read, recorded or compared
by anything in this module.

Design section
--------------
Design of record `automated-loop-design.md` §4.7 (the dry-run acceptance gate)
and §7, entries `W1-SYNTHETIC` and `W6-DRYRUN`. The guard vocabulary this
module scripts against is §2.3 (the role contracts) and §2.4 (G0-G12); the
contrast leg is §2.4 G8-G10 and PLAN §8a as mirrored by
:mod:`minireason.loop.standard`.

Determinism
-----------
Every byte this module writes is a pure function of ``(seed, induce)`` and of
the frozen text below. There is no wall clock, no ``random``, no ``uuid``, no
directory iteration order and no dictionary-insertion dependence: the one
source of variation is :func:`_draw`, a sha256 over the seed and a caller-named
key. Two generations at one seed are byte-identical; two seeds differ.
:func:`build_occurrence` therefore writes its own ``responses/*.json``
timestamps from :data:`RECORDED_MOMENTS`, which are recorded moments of a run
that is a fiction and are labelled as such in the trace's ``fixture`` line.

Deviations
----------
D1. **Wave-0 imports beyond the declared ``depends_on``.** The wave plan gives
    this module ``depends_on: [W0-TYPES]``, but the build asks for outputs that
    are *schema-valid against contracts*, so :mod:`.contracts` and
    :mod:`.standard` are imported too. Both are wave 0 and integrated; the
    import graph stays acyclic (`types -> standard -> contracts -> synthetic`).

D2. **The plan is frozen here, not by runner v2.** ``verify_custody`` in the
    importer re-checks only the occurrence-local subset of the plan identity
    (``plan_id == digest(plan - plan_id)``, ``material_sha256``, manifest
    pins), and that subset is what :func:`build_occurrence` satisfies by
    itself. Runner v2's ``verify()`` recomputes the whole plan body from a
    repository checkout, which would make this module import
    ``tools/multicycle_commitment_study_multi_v2`` (and, through it, ``creib``
    and every repository path) at build time. The seam is the ``freeze=``
    parameter instead: pass ``freeze=runner_freeze(repo)``-shaped callable and
    runner v2 writes ``plan.json`` and ``manifests/`` in this module's place.
    Without it the manifests are honest stand-ins that say so in their own
    bytes, and the plan says ``"synthetic": {...}`` out loud.

D3. **The canned ``provider/`` call records are shaped like the offline
    provider's, not recomputed from runner v2's ``payload_for``.** The
    importer's custody chain hashes those two files against the receipt and
    never re-derives them, so the chain is genuinely exercised; runner v2's
    ``read_terminal``/``decode_contribution`` comparison is not, and W6 should
    drive ``send_round`` with :func:`provider_factory` when it wants that leg.
    The stand-in records carry ``"synthetic": true`` and ``"url": null``.

D4. **A step timeout is raised, not slept.** ``OfflineProvider`` cannot time
    out and this module owns no clock, so the ``step_timeout`` induction makes
    the scripted provider raise :class:`SyntheticStepTimeout` (``.code ==
    "STEP_TIMEOUT"``) instead of blocking. The driver's handling path and the
    code the closing receipt names are exercised; the wall-clock deadline
    itself is W1-STEPS' own test, not this one's.

D5. **The custody mismatch is induced inside the occurrence, never in the
    repository.** ``induce="custody_mismatch"`` writes ``custody/pins.json``
    with a sha that disagrees with ``custody/pinned_source.txt`` by one byte,
    so ``loop.custody.verify_pins(pins, <occurrence>/custody)`` yields
    ``SOURCE_PIN_MISMATCH`` against a fixture. No pinned repository file is
    touched by anything here.

D6. **``APPELLATE_RULING_APPLIED`` is an outcome, not a failure.** It names an
    induced *outcome* the closing receipt must report - a ruling was ingested
    and pass 1 recomputed under it - rather than anything the loop refused. The
    wave-1 integrator therefore folded it into ``types.OUTCOME_CODES`` and the
    other two members of :data:`NEW_CODES` into ``types.FAILURE_CODES``; the
    two tables are disjoint and a token belongs to exactly one of them, so a
    reader of the closing record can tell a result from a refusal.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, Sequence

from minireason.provider_openai_compat import Endpoint, OfflineProvider

from . import contracts, standard
from .types import LoopError, block_code

__all__ = [
    "SYNTHETIC_SCHEMA",
    "DEFAULT_SEED",
    "PROBLEM_ID",
    "TEMPLATE_ID",
    "NODE_IDS",
    "FCL_ARM",
    "PROSE_ARM",
    "ARM_NAMES",
    "JUDGE_SEATS",
    "SYNTHETIC_FAMILIES",
    "SYNTHETIC_KEY_ENVS",
    "SYNTHETIC_ENDPOINTS",
    "endpoints_registry",
    "INDUCIBLE",
    "INDUCED_CODES",
    "NEW_CODES",
    "READING_PLAN",
    "READING_COORDINATES",
    "REREAD_SUFFIX",
    "PARAPHRASE_SUFFIXES",
    "UNRESOLVABLE_REFS",
    "FAILED_COORDINATE",
    "DUPLICATED_PHRASE",
    "material_document",
    "arms_document",
    "endpoints_document",
    "delivery_content",
    "CONTRAST_CASES",
    "CONTRAST_REPLICATES",
    "BASELINE_KINDS",
    "RECORDED_MOMENTS",
    "SyntheticError",
    "SyntheticStepTimeout",
    "Induced",
    "Occurrence",
    "ScriptedProviders",
    "runner_freeze",
    "build_occurrence",
    "canned_responses",
    "provider_factory",
    "contrast_leg",
    "appellate_ruling",
    "describe",
]


# --------------------------------------------------------------------- #
# codes                                                                  #
# --------------------------------------------------------------------- #

#: Stable codes this module introduced, each with the one-line reason it
#: exists. Everything else it names was already a member of
#: ``types.FAILURE_CODES`` or ``types.BLOCK_CODES``; these three were not, and
#: the wave-1 integrator folded them in (W0-TYPES open question O9) -
#: ``APPELLATE_RULING_APPLIED`` into ``types.OUTCOME_CODES`` because it names
#: what the loop *did*, the other two into ``types.FAILURE_CODES``.
NEW_CODES: Mapping[str, str] = MappingProxyType({
    "APPELLATE_RULING_APPLIED":
        "the dry run's appellate ruling flipped a label through pass 1; an "
        "induced outcome the closing receipt must name, not an operational failure",
    "SYNTHETIC_INDUCTION_UNKNOWN":
        "an induce token outside INDUCIBLE was asked for; refused rather than ignored, "
        "so a misspelt gate cannot pass by inducing nothing",
    "SYNTHETIC_COORDINATE_UNSCRIPTED":
        "a (role, coordinate) the script does not carry was asked for under strict=True; "
        "the loose default synthesises an output instead",
})


class SyntheticError(LoopError):
    """Any refusal this module raises. ``.code`` is a member of :data:`NEW_CODES`."""


class SyntheticStepTimeout(SyntheticError):
    """The induced step timeout (D4). ``.code`` is ``STEP_TIMEOUT``."""

    def __init__(self, detail: str = "") -> None:
        super().__init__("STEP_TIMEOUT", detail)


SYNTHETIC_SCHEMA = "minireason.loop.synthetic.v1"

#: The one seed the gate runs at. A whole number, never a clock reading.
DEFAULT_SEED = 9005


# --------------------------------------------------------------------- #
# the occurrence's shape                                                 #
# --------------------------------------------------------------------- #

PROBLEM_ID = "synth"
TEMPLATE_ID = "probe"
#: Template node ids, in template order. ``account`` takes no input; every
#: later node takes the earlier ones, which is what puts a *cross-document*
#: reference inside reach of the importer's two-hop resolver.
NODE_IDS: tuple[str, ...] = ("account", "objection", "response")

#: The FCL-1 arm. ``graph_import_h005.FCL_SURFACE_ARMS`` is ``("mini_fcl",)``
#: and is the importer's own published constant, so the arm that is meant to
#: carry a parsed commitment surface must be spelled exactly this way.
FCL_ARM = "mini_fcl"
#: The prose arm. Its commitments are deliberately not FCL-1, so it lands in
#: the use table's ``nodes_not_read`` and is the arm the provider failure ends.
PROSE_ARM = "mini_prose"
ARM_NAMES: tuple[str, ...] = (FCL_ARM, PROSE_ARM)

#: The two judge seats G0 requires to carry distinct families.
JUDGE_SEATS: tuple[str, ...] = ("judge-a", "judge-b")

#: Recorded moments, in registration order. Fictions, fixed, and never read
#: from a clock; ``_assign_timestamps`` needs the leading coordinate to carry
#: one, so every coordinate does.
RECORDED_MOMENTS: tuple[str, ...] = (
    "2026-01-01T00:00:01+00:00",
    "2026-01-01T00:00:02+00:00",
    "2026-01-01T00:00:03+00:00",
    "2026-01-01T00:00:04+00:00",
    "2026-01-01T00:00:05+00:00",
    "2026-01-01T00:00:06+00:00",
)


# --------------------------------------------------------------------- #
# the synthetic endpoint registry                                        #
# --------------------------------------------------------------------- #

#: Two fictional families, so G0's cross-family rule has something to hold.
SYNTHETIC_FAMILIES: tuple[str, str] = ("synthetic/alpha-family", "synthetic/beta-family")

#: Two environment variable NAMES that name nothing. They are not
#: ``DEEPSEEK_API_KEY`` or ``OLLAMA_API_KEY`` and are never resolved to a
#: value anywhere in this module: seat assignment needs a name, not a secret.
SYNTHETIC_KEY_ENVS: tuple[str, str] = ("SYNTHETIC_ALPHA_KEY", "SYNTHETIC_BETA_KEY")

_ENDPOINT_ROWS: tuple[Mapping[str, Any], ...] = (
    MappingProxyType({
        "name": "synthetic/alpha",
        "base_url": "https://alpha.synthetic.invalid/v1",
        "model": "synthetic-alpha-1",
        "key_env": SYNTHETIC_KEY_ENVS[0],
        "family": SYNTHETIC_FAMILIES[0],
        "chat_path": "/chat/completions",
        "native": False,
        "max_concurrency": 2,
        "timeout_seconds": 30,
    }),
    MappingProxyType({
        "name": "synthetic/beta",
        "base_url": "https://beta.synthetic.invalid/v1",
        "model": "synthetic-beta-1",
        "key_env": SYNTHETIC_KEY_ENVS[1],
        "family": SYNTHETIC_FAMILIES[1],
        "chat_path": "/chat/completions",
        "native": False,
        "max_concurrency": 2,
        "timeout_seconds": 30,
    }),
)

#: The two declared endpoints, as ``Endpoint`` objects.
SYNTHETIC_ENDPOINTS: tuple[Endpoint, ...] = tuple(
    Endpoint(**dict(row)) for row in _ENDPOINT_ROWS
)

#: Which arm spends which endpoint.
_ARM_ENDPOINT: Mapping[str, str] = MappingProxyType({
    FCL_ARM: SYNTHETIC_ENDPOINTS[0].name,
    PROSE_ARM: SYNTHETIC_ENDPOINTS[1].name,
})

#: Which seat role spends which endpoint. The critic sits on alpha, both
#: defender and the second judge on beta, so G0 (>= 2 judge families, critic
#: family outside the judge families, defender family != critic family) is
#: satisfiable offline without a third fiction.
_SEAT_ENDPOINT: Mapping[str, str] = MappingProxyType({
    "critic": SYNTHETIC_ENDPOINTS[0].name,
    "defender": SYNTHETIC_ENDPOINTS[1].name,
    "judge-a": SYNTHETIC_ENDPOINTS[0].name,
    "judge-b": SYNTHETIC_ENDPOINTS[1].name,
    "marker": SYNTHETIC_ENDPOINTS[0].name,
    "variator": SYNTHETIC_ENDPOINTS[1].name,
    "delivery": SYNTHETIC_ENDPOINTS[0].name,
})


def endpoints_registry() -> dict[str, Endpoint]:
    """The synthetic registry, name -> ``Endpoint``, shaped like the shipped one.

    Hand it to ``tools/multicycle_commitment_study_multi_v2.set_registry`` or to
    W1-SEATS' ``load_registry``; it declares two families and two ``key_env``
    NAMES, which is the least a cross-family seat plan can be built from.
    """

    return {endpoint.name: endpoint for endpoint in SYNTHETIC_ENDPOINTS}


def endpoints_document() -> dict[str, Any]:
    """The registry as an ``endpoints.json``-shaped mapping, for a file fixture."""

    return {
        "schema_version": "minireason.endpoints.v1",
        "endpoints": [dict(row) for row in _ENDPOINT_ROWS],
    }


# --------------------------------------------------------------------- #
# the induction vocabulary                                               #
# --------------------------------------------------------------------- #

#: Every failure this module can induce, in the order §4.7 lists them. A token
#: outside this tuple is refused (``SYNTHETIC_INDUCTION_UNKNOWN``).
INDUCIBLE: tuple[str, ...] = (
    "provider_arm_failure",
    "custody_mismatch",
    "step_timeout",
    "ensemble_split",
    "paraphrase_flip",
    "non_unique_offset",
    "decisive_point_absent",
    "baseline_kind_collision",
    "reread_without_reason",
    "appellate_ruling",
)

#: token -> the code the closing receipt must name for it.
#:
#: Every block code is built with ``types.block_code(reason)`` rather than
#: written out with its prefix (REVIEW-PREREG PR-12: one owner, one spelling).
#: The six literals that used to be here were the package's last retyped
#: ``blocked:`` strings, and ``block_code`` refuses a reason ``BLOCK_CODES``
#: does not carry, so a typo is an ImportError at import rather than a receipt
#: naming a code no register prints.
INDUCED_CODES: Mapping[str, str] = MappingProxyType({
    "provider_arm_failure": "TRANSPORT_OR_RESPONSE_ERROR",
    "custody_mismatch": "SOURCE_PIN_MISMATCH",
    "step_timeout": "STEP_TIMEOUT",
    "ensemble_split": block_code("ensemble-split"),
    "paraphrase_flip": block_code("paraphrase-flip"),
    "non_unique_offset": block_code("referential-integrity"),
    "decisive_point_absent": block_code("referential-integrity"),
    "baseline_kind_collision": block_code("baseline-forced-same"),
    "reread_without_reason": "REOPEN_REFUSED",
    "appellate_ruling": "APPELLATE_RULING_APPLIED",
})

#: token -> the aggregate code the driver reports alongside the per-subject one.
_AGGREGATE_CODES: Mapping[str, str] = MappingProxyType({
    "provider_arm_failure": block_code("provider"),
    "custody_mismatch": "CUSTODY_MISMATCH",
})

#: token -> the step kind (``types.STEP_KINDS``) the induction lands in.
_INDUCED_STEPS: Mapping[str, str] = MappingProxyType({
    "provider_arm_failure": "SEND",
    "custody_mismatch": "PREFLIGHT",
    "step_timeout": "SEND",
    "ensemble_split": "READ",
    "paraphrase_flip": "READ",
    "non_unique_offset": "READ",
    "decisive_point_absent": "READ",
    "baseline_kind_collision": "MARK",
    "reread_without_reason": "READ",
    "appellate_ruling": "ADJUDICATE",
})


def _checked(induce: Iterable[str]) -> frozenset[str]:
    tokens = frozenset(str(token) for token in induce)
    unknown = sorted(tokens - set(INDUCIBLE))
    if unknown:
        raise SyntheticError("SYNTHETIC_INDUCTION_UNKNOWN",
                             f"{unknown} are not members of INDUCIBLE")
    return tokens


# --------------------------------------------------------------------- #
# deterministic draws                                                    #
# --------------------------------------------------------------------- #


def _draw(seed: int, key: str, modulus: int) -> int:
    """A stable whole number in ``[0, modulus)`` from ``(seed, key)``.

    sha256 rather than :mod:`random`, so the value cannot drift with a CPython
    release and no hidden generator state couples two call sites.
    """

    raw = hashlib.sha256(f"{int(seed)}:{key}".encode("utf-8")).digest()
    return int.from_bytes(raw[:8], "big") % int(modulus)


def _variant(seed: int, key: str) -> str:
    """A short stable tag; what makes two seeds produce different bytes."""

    return hashlib.sha256(f"{int(seed)}:{key}".encode("utf-8")).hexdigest()[:8]


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _digest(value: Any) -> str:
    """``provider.digest`` / ``graph_import_h005.study_digest``: compact, sorted."""

    return _sha(json.dumps(value, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")).encode("utf-8"))


def _encoded(value: Any) -> bytes:
    """The record form every occurrence file is written in (runner v2's)."""

    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)
            + "\n").encode("utf-8")


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_encoded(value))


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def _artifact_id(stage_label: str, body_ref: str, commitments_ref: str) -> str:
    """The stored artifact's identity, as ``creib``'s own content id where it can.

    ``creib.forge.mini.runner._store_artifact`` mints it from
    ``content_id(ARTIFACT_DOMAIN, {...})``; the import is lazy and local so a
    checkout without ``creib`` on the path still builds an occurrence, with a
    clearly-labelled fallback identity. Either way the value is a pure function
    of the bytes and the importer only ever compares it with itself.
    """

    payload = {
        "stage_id": stage_label,
        "kind_id": "h005.authored.v1",
        "seq": 0,
        "body_ref": body_ref,
        "commitments_ref": commitments_ref,
        "extra": {},
    }
    try:  # pragma: no cover - exercised whenever creib is importable
        from creib.forge.mini.common import ARTIFACT_DOMAIN, content_id
    except ImportError:  # pragma: no cover - defensive
        return _sha(("synthetic.artifact.v1:" + json.dumps(
            payload, ensure_ascii=False, sort_keys=True,
            separators=(",", ":"))).encode("utf-8"))
    return content_id(ARTIFACT_DOMAIN, payload)


# --------------------------------------------------------------------- #
# the material                                                           #
# --------------------------------------------------------------------- #

_SYSTEM = (
    "Work on the problem using the material actually exposed in this request and your "
    "background knowledge. The problem has no supplied answer key or scoring rule. "
    "Claims, criticisms and methods are fallible. Return a JSON object with exactly two "
    "independently authored string fields: body and commitments."
)

_PROSE_INSTRUCTION = (
    "Write the commitment surface in ordinary free prose. Distinguish a claim from a "
    "proposed application where that is useful, and say what taking your contribution up "
    "would involve. None of these is required to exist."
)

_FORMAL_INSTRUCTION = (
    "Use FCL-1 for the commitment surface, encoded as a JSON document inside the "
    "commitments string: {\"language\":\"FCL-1\",\"records\":[...],\"uptake\":[...]}. Each "
    "record has a unique local id, a type (claim|commitment|objection|use|problem) and "
    "text. References are local IDs or exposed-artifact-label#local-ID; do not invent "
    "hidden IDs."
)

_BARE_INSTRUCTION = (
    "Begin or continue your inquiry into the problem. This single call is one complete "
    "invocation. Use the ordinary prose commitment interface described above."
)

_PROBLEM_PROSE = (
    "Two flatmates keep a chore roster. They agree on who does what, and later disagree "
    "about what the agreement meant. One of them has started avoiding the conversation. "
    "What should they do?"
)

_NODE_INSTRUCTIONS: Mapping[str, str] = MappingProxyType({
    "account": "Issue the account you would now use.",
    "objection": "Develop criticism of the account where you have grounds.",
    "response": "Answer the criticism, or concede it, using only the declared inputs.",
})

_NODE_INPUTS: Mapping[str, tuple[Mapping[str, str], ...]] = MappingProxyType({
    "account": (),
    "objection": (MappingProxyType({"source": "account", "view": "both"}),),
    "response": (MappingProxyType({"source": "account", "view": "both"}),
                 MappingProxyType({"source": "objection", "view": "both"})),
})


def material_document(seed: int = DEFAULT_SEED) -> dict[str, Any]:
    """The occurrence's ``material.json``, valid for runner v2's ``validate_material``."""

    return {
        "schema": "minireason.h005.material.v1",
        "study_id": "W1-SYNTHETIC-dry-run",
        "system": _SYSTEM,
        "prose_instruction": _PROSE_INSTRUCTION,
        "formal_instruction": _FORMAL_INSTRUCTION,
        "bare_instruction": _BARE_INSTRUCTION,
        "templates": {
            TEMPLATE_ID: {
                "nodes": [
                    {
                        "id": node,
                        "instruction": _NODE_INSTRUCTIONS[node],
                        "inputs": [dict(binding) for binding in _NODE_INPUTS[node]],
                    }
                    for node in NODE_IDS
                ]
            }
        },
        "problems": [
            {
                "id": PROBLEM_ID,
                "prose": _PROBLEM_PROSE + f" (synthetic variant {_variant(seed, 'problem')})",
                # Three to five template ids; one template invoked three times.
                "templates": [TEMPLATE_ID, TEMPLATE_ID, TEMPLATE_ID],
            }
        ],
        "source_pins": {},
    }


def arms_document() -> dict[str, Any]:
    """The occurrence's ``arms.json``: two arms, offline, one problem, one cycle."""

    return {
        "schema": "minireason.h005.arms.v1",
        "provider": "offline",
        "arms": {
            FCL_ARM: {
                "surface": "fcl",
                "kind": "mini",
                "endpoint": _ARM_ENDPOINT[FCL_ARM],
                "max_tokens": 4096,
                "seed": 11,
            },
            PROSE_ARM: {
                "surface": "prose",
                "kind": "mini",
                "endpoint": _ARM_ENDPOINT[PROSE_ARM],
                "max_tokens": 4096,
                "seed": 11,
            },
        },
        "scope": {"problems": [PROBLEM_ID], "cycles": [1]},
    }


# --------------------------------------------------------------------- #
# the FCL-1 documents and the prose bodies                               #
# --------------------------------------------------------------------- #

#: One sentence deliberately present in BOTH the account's record ``a3`` and
#: the objection's record ``o3``. A critic quoting it resolves to two offsets
#: on the resolvable surface, which is the ``non_unique_offset`` induction.
DUPLICATED_PHRASE = "The roster is reviewed weekly."

#: Quotes the scripted critic uses, one per reading row. Each occurs exactly
#: once in its row's surface unless the row is the one carrying the
#: non-uniqueness induction.
_ROW_QUOTES: Mapping[str, str] = MappingProxyType({
    "read/retains": "Rotating ownership survives a schedule change.",
    "read/qualifies": "Written confirmation settles what an agreement meant.",
    "read/rejects": DUPLICATED_PHRASE,
    "read/unresolved-a": "It may not be so.",
    "read/repairs": "A shared ledger records completion at the moment of completion.",
    "read/re-deploys": "Rotating ownership is retained here without amendment.",
    "read/unresolved-b": "Rotating ownership survives a schedule change.",
    "read/rejects-2": "Written confirmation holds only where both flatmates read it.",
})


def _account_document() -> dict[str, Any]:
    """The FCL-1 document the other two nodes refer into."""

    return {
        "language": "FCL-1",
        "records": [
            {
                "id": "a1",
                "type": "claim",
                "text": "Rotating ownership survives a schedule change.",
                "scope": "Two flatmates sharing one roster.",
            },
            {
                "id": "a2",
                "type": "commitment",
                "text": "Written confirmation settles what an agreement meant.",
                "action": "Confirm each agreed chore in writing on the day it is agreed.",
                "consequence": "A later disagreement is settled by the written line.",
            },
            {
                "id": "a3",
                "type": "claim",
                "text": DUPLICATED_PHRASE,
                "grounds": "A weekly review is short enough to be kept.",
            },
            {
                "id": "a4",
                "type": "use",
                "text": "A shared ledger records completion at the moment of completion.",
                "consequence": "Nobody has to remember who promised what.",
            },
            {
                "id": "a5",
                "type": "problem",
                "text": "Avoidance is a signal about capacity, not about willingness.",
                "bearing": "Reading it as refusal would misdirect the whole remedy.",
            },
            {
                # Short words and stopwords only: no token of length >= 5 that
                # is not a stopword, so a row targeting this record carries no
                # lexical overlap at all and prints the published note.
                "id": "a6",
                "type": "claim",
                "text": "It may not be so.",
            },
        ],
        "uptake": ["a1", "a2", "a4"],
    }


def _objection_document() -> dict[str, Any]:
    """Cross-document refs into the account, plus two refs that resolve to nothing."""

    return {
        "language": "FCL-1",
        "records": [
            {
                "id": "o1",
                "type": "claim",
                "text": "Rotating ownership is retained here without amendment.",
                "mentions": ["p.objection.0#a1"],
            },
            {
                "id": "o2",
                "type": "claim",
                "text": "Written confirmation holds only where both flatmates read it.",
                "scope": "Qualified to households that share one written surface.",
                "depends": ["p.objection.0#a2"],
            },
            {
                "id": "o3",
                "type": "objection",
                "text": DUPLICATED_PHRASE + " A weekly review is too slow for a rota "
                        "that changes inside the week.",
                "bearing": "If the review cadence is wrong the remedy arrives late.",
                "target": ["p.objection.0#a3"],
            },
            {
                "id": "o4",
                "type": "claim",
                "text": "A record that was never exposed cannot be relied upon.",
                # No local record zz9 in the owning document: unresolved, dropped.
                "mentions": ["p.objection.0#zz9"],
            },
            {
                "id": "o5",
                "type": "claim",
                "text": "A label spelled with its manifest prefix is not in this index.",
                # The label the brief renders is `p.objection.0`; the fully
                # qualified spelling is not a key of the projection index.
                "mentions": ["h005." + TEMPLATE_ID + ".p.objection.0#a1"],
            },
            {
                "id": "o6",
                "type": "use",
                "text": "Taking up the sixth record would need an interpretation this "
                        "document does not supply.",
                "mentions": ["p.objection.0#a6"],
            },
        ],
        "uptake": ["o1", "o3"],
    }


def _response_document() -> dict[str, Any]:
    """Refs into BOTH earlier documents, including one ``#BODY`` extension."""

    return {
        "language": "FCL-1",
        "records": [
            {
                "id": "r1",
                "type": "use",
                "text": "The shared ledger is repaired to record the agreed wording too.",
                "action": "Add an agreed-wording column beside the completion column.",
                "revises": ["p.response.0#a4"],
            },
            {
                "id": "r2",
                "type": "use",
                "text": "Rotating ownership is re-deployed against the avoidance case.",
                "depends": ["p.response.1#o1"],
            },
            {
                "id": "r3",
                "type": "claim",
                "text": "The account as a whole is cited here, not one of its records.",
                "mentions": ["p.response.0#BODY"],
            },
            {
                "id": "r4",
                "type": "objection",
                "text": "Qualifying written confirmation to shared surfaces gives up the "
                        "case it was meant to settle.",
                "bearing": "If the qualification stands the remedy does not reach this household.",
                "target": ["p.response.1#o2"],
            },
        ],
        "uptake": ["r1", "r2"],
    }


_PROSE_COMMITMENTS: Mapping[str, str] = MappingProxyType({
    "account": "Taking this up involves accepting that a rota can be owned rather than "
               "scheduled, and that a written line settles a later disagreement.",
    "objection": "Taking this up involves accepting that a weekly review is too slow, "
                 "which is a claim about cadence and can itself be criticised.",
    "response": "Taking this up involves accepting the ledger repair and the re-deployment "
                "of rotating ownership, neither of which is certified here.",
})


def _body_text(arm: str, node: str, seed: int) -> str:
    """The referring node's public prose; the use table cuts it into sentences."""

    tag = _variant(seed, f"body:{arm}:{node}")
    if node == "account":
        return (
            "Rotating ownership survives a schedule change because the owner, not the "
            "calendar, carries the chore. Written confirmation settles what an agreement "
            "meant, and costs one line. The roster is reviewed weekly. A shared ledger "
            "records completion at the moment of completion. Avoidance is a signal about "
            f"capacity, not about willingness. Synthetic account variant {tag}."
        )
    if node == "objection":
        return (
            "Rotating ownership is retained in this criticism without amendment. Written "
            "confirmation holds only where both flatmates actually read the written "
            "surface. The roster is reviewed weekly, and a weekly cadence is too slow for "
            "a rota that changes inside the week. A record that was never exposed cannot "
            f"be relied upon. Synthetic objection variant {tag}."
        )
    return (
        "The shared ledger is repaired here to record the agreed wording beside the "
        "completion. Rotating ownership is re-deployed against the avoidance case rather "
        "than replaced. The account as a whole is cited, not one of its records. "
        "Qualifying written confirmation to shared surfaces gives up the case it was "
        f"meant to settle. Synthetic response variant {tag}."
    )


def _commitments_text(arm: str, node: str) -> str:
    if arm == FCL_ARM:
        document = {"account": _account_document(),
                    "objection": _objection_document(),
                    "response": _response_document()}[node]
        return json.dumps(document, ensure_ascii=False, sort_keys=False)
    return _PROSE_COMMITMENTS[node]


def delivery_content(arm: str, node: str, seed: int = DEFAULT_SEED) -> str:
    """The provider's raw ``content`` for one coordinate: the two-field envelope.

    This is the single source of the occurrence's delivered bytes. The canned
    occurrence decodes it exactly as runner v2's ``envelope_unwrap`` would, and
    :func:`provider_factory` serves the very same string, so a W6 dry run that
    drives ``send_round`` instead of reading the canned files gets the same
    documents either way.
    """

    return json.dumps(
        {"body": _body_text(arm, node, seed), "commitments": _commitments_text(arm, node)},
        ensure_ascii=False, sort_keys=True)


# --------------------------------------------------------------------- #
# the reading plan                                                       #
# --------------------------------------------------------------------- #

def _coord_key(arm: str, node: str, cycle: int = 1) -> str:
    return f"{PROBLEM_ID}/{arm}/cycle{cycle:02d}/{node}"


#: Short reading coordinate -> the use-table row it names, as
#: ``(referring coordinate key, referring record id, ref field, ref verbatim)``.
#: The row key is exactly what ``use_relation_h005.UseRow`` publishes, so a
#: caller matches on published fields and never on row position.
READING_COORDINATES: Mapping[str, tuple[str, str, str, str]] = MappingProxyType({
    "read/retains": (_coord_key(FCL_ARM, "objection"), "o1", "mentions", "p.objection.0#a1"),
    "read/qualifies": (_coord_key(FCL_ARM, "objection"), "o2", "depends", "p.objection.0#a2"),
    "read/rejects": (_coord_key(FCL_ARM, "objection"), "o3", "target", "p.objection.0#a3"),
    "read/unresolved-a": (_coord_key(FCL_ARM, "objection"), "o6", "mentions", "p.objection.0#a6"),
    "read/repairs": (_coord_key(FCL_ARM, "response"), "r1", "revises", "p.response.0#a4"),
    "read/re-deploys": (_coord_key(FCL_ARM, "response"), "r2", "depends", "p.response.1#o1"),
    "read/unresolved-b": (_coord_key(FCL_ARM, "response"), "r3", "mentions", "p.response.0#BODY"),
    "read/rejects-2": (_coord_key(FCL_ARM, "response"), "r4", "target", "p.response.1#o2"),
})

#: Short reading coordinate -> the reading-vocabulary value the row is built to
#: be read as. Every member of ``standard.READING_VOCABULARY`` appears at least
#: once, ``unresolved`` included, and ``unresolved`` appears twice by two
#: different routes (a critic answering ``none``, and a non-empty
#: ``outside_vocabulary``). **The instrument never fills a reading cell**; this
#: is the gate's own expectation, published so a test can assert coverage.
READING_PLAN: Mapping[str, str] = MappingProxyType({
    "read/retains": "retains",
    "read/qualifies": "qualifies",
    "read/rejects": "rejects-with-reason",
    "read/unresolved-a": "unresolved",
    "read/repairs": "repairs",
    "read/re-deploys": "re-deploys",
    "read/unresolved-b": "unresolved",
    "read/rejects-2": "rejects-with-reason",
})

#: Which reading coordinate carries which induction.
_READING_INDUCTION: Mapping[str, str] = MappingProxyType({
    "read/qualifies": "ensemble_split",
    "read/rejects": "non_unique_offset",
    "read/repairs": "paraphrase_flip",
    "read/re-deploys": "decisive_point_absent",
    "read/unresolved-a": "reread_without_reason",
})

#: The coordinate the ``provider_arm_failure`` induction ends. It is the prose
#: arm's last node, so the FCL arm - which carries every reading row - runs on.
FAILED_COORDINATE = _coord_key(PROSE_ARM, "response")

#: Refs written to resolve to nothing, as ``(coordinate key, record id, field, ref)``.
UNRESOLVABLE_REFS: tuple[tuple[str, str, str, str], ...] = (
    (_coord_key(FCL_ARM, "objection"), "o4", "mentions", "p.objection.0#zz9"),
    (_coord_key(FCL_ARM, "objection"), "o5", "mentions",
     "h005." + TEMPLATE_ID + ".p.objection.0#a1"),
)


# --------------------------------------------------------------------- #
# the contrast leg (C001)                                                #
# --------------------------------------------------------------------- #

CONTRAST_CASES: tuple[str, ...] = ("case-a", "case-b", "case-c", "case-d")
CONTRAST_REPLICATES: tuple[str, ...] = ("rep-1", "rep-2", "rep-3")

#: Case -> the one register that differs and the kind it differs at. Exactly
#: one register differs per case, which is what G9 and the falsifier evaluation
#: are built to read.
_CASE_REGISTER: Mapping[str, tuple[str, str]] = MappingProxyType({
    "case-a": ("T", "target_set_membership"),
    "case-b": ("E", "engagement_form"),
    "case-c": ("D", "disposition_value"),
    "case-d": ("G", "grounds_source"),
})

#: The sealed within-ORIGINAL baseline kind set, per register. ``E`` already
#: carries ``engagement_form``, so ``case-b``'s ``differs`` collides with the
#: baseline and G9 makes the PROGRAM write ``same``.
BASELINE_KINDS: Mapping[str, tuple[str, ...]] = MappingProxyType({
    "T": (),
    "E": ("engagement_form",),
    "D": (),
    "G": (),
})


def _contrast_commitments(case: str, replicate: str, side: str, seed: int) -> str:
    """One replicate's commitment surface, as an FCL-1 document string."""

    register, difference_kind = _CASE_REGISTER[case]
    tag = _variant(seed, f"contrast:{case}:{replicate}")
    differs = side == "CONTROL"
    record: dict[str, Any] = {
        "id": "c1",
        "type": "commitment",
        "text": f"Case {case} replicate {replicate} commitment {tag}.",
        "action": "Apply the agreed remedy once.",
    }
    if register == "T":
        record["target"] = (["p.objection.0#a2"] if differs else ["p.objection.0#a1"])
    elif register == "E":
        record["mentions"] = (["p.objection.0#a1"] if differs else ["a1"])
    elif register == "D":
        record["consequence"] = ("The remedy is withdrawn." if differs
                                 else "The remedy is retained.")
    else:
        record["grounds"] = ("Grounds taken from the objection."
                             if differs else "Grounds taken from the account.")
    document = {"language": "FCL-1", "records": [record], "uptake": ["c1"]}
    return json.dumps(document, ensure_ascii=False, sort_keys=False)


def contrast_leg(seed: int = DEFAULT_SEED) -> dict[str, Any]:
    """Four cases x three replicates, one register differing per case (§4.7).

    ``case-d`` carries one byte-identical ORIGINAL/CONTROL replicate so G10(a)'s
    byte-identity defeater has a subject, and ``case-b``'s difference kind is a
    member of :data:`BASELINE_KINDS` so G9's program downgrade has one.
    """

    cases: dict[str, Any] = {}
    for case in CONTRAST_CASES:
        register, difference_kind = _CASE_REGISTER[case]
        replicates: dict[str, Any] = {}
        for index, replicate in enumerate(CONTRAST_REPLICATES):
            original = _contrast_commitments(case, replicate, "ORIGINAL", seed)
            identical = case == "case-d" and index == 0
            control = (original if identical
                       else _contrast_commitments(case, replicate, "CONTROL", seed))
            replicates[replicate] = {
                "ORIGINAL": original,
                "CONTROL": control,
                "byte_identical": identical,
            }
        cases[case] = {
            "register": register,
            "difference_kind": difference_kind,
            "collides_with_baseline": difference_kind in BASELINE_KINDS[register],
            "replicates": replicates,
        }
    return {
        "schema": SYNTHETIC_SCHEMA + ".contrast",
        "registers": list(standard.REGISTER_IDS),
        "baseline_kinds": {register: list(kinds)
                           for register, kinds in BASELINE_KINDS.items()},
        "cases": cases,
    }


def appellate_ruling(seed: int = DEFAULT_SEED) -> dict[str, Any]:
    """The scripted appellate ruling file (§4.7's last induced item).

    It is an appeal *against a validity node*, so applying it flips a label
    through adjudication pass 1 and rewrites no published record. The target
    spelling is deliberately the reading's own row key rather than a graph id:
    W1-GRAPH mints the ids, and this module may not guess them.
    """

    row = READING_COORDINATES["read/retains"]
    return {
        "schema": SYNTHETIC_SCHEMA + ".appeal",
        "ruling_id": "synthetic-appeal-" + _variant(seed, "appeal"),
        "against": "validity_node",
        "reading_row": {"referring_coordinate_key": row[0], "referring_record_id": row[1],
                        "ref_field": row[2], "ref_verbatim": row[3]},
        "reading_coordinate": "read/retains",
        "sustained": False,
        "reopen_reason": "appellate-ruling",
        "decisive_point": "The quoted passage does not bear the retention it was read as bearing.",
        "note": "Synthetic appellate ruling for the dry-run gate; no published record is rewritten.",
        "expected_code": "APPELLATE_RULING_APPLIED",
    }


# --------------------------------------------------------------------- #
# the scripted role outputs                                              #
# --------------------------------------------------------------------- #

_BINDINGS: Mapping[str, str] = MappingProxyType({
    "target": "the target record named by the ref",
    "defect": "none alleged; the relation is nominated, not the defect",
    "grounds": "the quoted passage of the target record",
    "bearing": "if the relation does not hold the row stays unresolved",
})


#: The suffix a re-read trial's coordinate carries, and the two a paraphrase
#: spot-check carries. A repair, a re-read and a paraphrase are each their own
#: coordinate (§4.4, W2-ROLES' NO_REPLAY), never a second call on the first.
REREAD_SUFFIX = "#reread"
PARAPHRASE_SUFFIXES: tuple[str, ...] = ("#paraphrase-0", "#paraphrase-1")


def _row_of(coordinate: str) -> str:
    """The reading row a derived coordinate belongs to."""

    return coordinate.split("#", 1)[0]


def _critic_output(coordinate: str, seed: int, induce: frozenset[str]) -> dict[str, Any]:
    row = _row_of(coordinate)
    relation = READING_PLAN.get(row, "retains")
    quote = _ROW_QUOTES.get(row, DUPLICATED_PHRASE)
    outside = ""
    if coordinate.endswith(REREAD_SUFFIX):
        # The re-read that would make an unresolved row stick. It is refused at
        # the write for want of a reopen_reason (G11), never here.
        return {"relation": "retains", "passage_quote": quote,
                "role_bindings": dict(_BINDINGS),
                "case": ("On a second reading the quoted passage does bear the relation "
                         f"({_variant(seed, 'reread:' + coordinate)})."),
                contracts.OUTSIDE_VOCABULARY_FIELD: ""}
    if coordinate == "read/unresolved-a":
        # G4/§2.3: a critic answering "none" ends the row at one call and owes
        # neither a case nor a passage.
        return {"relation": "none", "passage_quote": "", "case": "",
                "role_bindings": dict(_BINDINGS), contracts.OUTSIDE_VOCABULARY_FIELD: ""}
    if coordinate == "read/unresolved-b":
        # D6: a non-empty outside_vocabulary forces unresolved, text preserved.
        relation = "retains"
        outside = ("the ref names the contribution rather than a record, which this "
                   "vocabulary has no value for")
    if relation == "unresolved":  # pragma: no cover - defensive
        relation = "retains"
    return {
        "relation": relation,
        "passage_quote": quote,
        "role_bindings": dict(_BINDINGS),
        "case": (f"The referring record takes up the quoted passage as {relation}; "
                 f"the quoted span is the whole of the ground offered "
                 f"({_variant(seed, 'critic:' + coordinate)})."),
        contracts.OUTSIDE_VOCABULARY_FIELD: outside,
    }


def _defender_output(coordinate: str, seed: int) -> dict[str, Any]:
    return {
        "answer": (f"The quoted passage is operative for this row and the nominated "
                   f"relation is the one the record exhibits "
                   f"({_variant(seed, 'defender:' + coordinate)})."),
        "concedes": False,
    }


def _judge_output(coordinate: str, seat: str, seed: int,
                  induce: frozenset[str], *, paraphrased: bool = False) -> dict[str, Any]:
    """One judge seat's ruling.

    ``decisive_point`` must occur exactly once in ``case + "\\n" + answer``
    (G2b), so the default points at a phrase only the defender's answer
    carries. The two induced departures are named in :data:`_READING_INDUCTION`.
    """

    row = _row_of(coordinate)
    sustained = True
    decisive = f"the one the record exhibits ({_variant(seed, 'defender:' + row)})"
    if row == "read/qualifies" and "ensemble_split" in induce and seat == JUDGE_SEATS[1]:
        # G5: the two seats disagree. Never averaged, never majority-voted.
        sustained = False
    if row == "read/re-deploys" and "decisive_point_absent" in induce:
        # G2b: zero occurrences on the exchange surface.
        decisive = "a phrase that appears in neither the case nor the answer"
    if paraphrased and row == "read/repairs" and "paraphrase_flip" in induce:
        # G7: the ruling flips under a paraphrase that held the quoted span.
        sustained = False
    return {
        "sustained": sustained,
        "decisive_point": decisive,
        "reading_note": f"{seat} read the quoted span against the referring record.",
    }


def _variator_output(coordinate: str, seed: int, induce: frozenset[str]) -> dict[str, Any]:
    quote = _ROW_QUOTES.get(_row_of(coordinate), DUPLICATED_PHRASE)
    tag = _variant(seed, "variator:" + coordinate)
    return {
        "paraphrases": [
            f"Restated once, holding the quoted span byte-identical: {quote} [{tag}a]",
            f"Restated again, holding the quoted span byte-identical: {quote} [{tag}b]",
        ]
    }


def _marker_output(coordinate: str, seed: int, induce: frozenset[str]) -> dict[str, Any]:
    """One register mark on one contrast cell.

    The coordinate is ``mark/<case>/<register>/<replicate>``. A cell whose case
    differs at a kind already in the sealed baseline set is still *marked*
    ``differs`` by the seat - G9's downgrade to ``same`` is the PROGRAM's, and
    scripting the seat to pre-empt it would test nothing.
    """

    parts = coordinate.split("/")
    case = parts[1] if len(parts) > 1 else CONTRAST_CASES[0]
    register = parts[2] if len(parts) > 2 else "T"
    case_register, difference_kind = _CASE_REGISTER.get(case, ("T", "target_set_membership"))
    tag = _variant(seed, "marker:" + coordinate)
    if register != case_register:
        # Only one register differs per case; every other register is the same.
        return {"mark": "same", "difference_kind": None, "left_quote": "",
                "right_quote": "", "case": f"No difference in register {register} ({tag})."}
    return {
        "mark": "differs",
        "difference_kind": difference_kind,
        "left_quote": f"ORIGINAL {case} {register}",
        "right_quote": f"CONTROL {case} {register}",
        "case": f"Register {register} differs at {difference_kind} ({tag}).",
    }


def _default_output(role: str, coordinate: str, seat: str, seed: int,
                    induce: frozenset[str]) -> dict[str, Any]:
    if role == "critic":
        return _critic_output(coordinate, seed, induce)
    if role == "defender":
        return _defender_output(coordinate, seed)
    if role == "judge":
        return _judge_output(coordinate, seat or JUDGE_SEATS[0], seed, induce)
    if role == "variator":
        return _variator_output(coordinate, seed, induce)
    if role == "marker":
        return _marker_output(coordinate, seed, induce)
    raise SyntheticError("SYNTHETIC_COORDINATE_UNSCRIPTED",
                         f"no scripted output for role {role!r}")


def _entry(content: str, seed: int, key: str) -> dict[str, Any]:
    """One ``OfflineProvider`` script entry, with plausible stable token counts."""

    prompt_tokens = 200 + _draw(seed, "prompt:" + key, 200)
    completion_tokens = 60 + _draw(seed, "completion:" + key, 120)
    return {
        "content": content,
        "finish_reason": "stop",
        "usage": {"prompt_tokens": prompt_tokens,
                  "completion_tokens": completion_tokens,
                  "total_tokens": prompt_tokens + completion_tokens},
        "reasoning_content_present": False,
    }


def canned_responses(seed: int = DEFAULT_SEED, *,
                     induce: Iterable[str] = ()) -> dict[tuple[str, str], tuple[dict[str, Any], ...]]:
    """Every scripted ``(role, coordinate) -> OfflineProvider script``.

    ``role`` is a seat role (:data:`contracts.ROLE_NAMES`) or ``"delivery"``
    for a runner-v2 occurrence node. A judge coordinate carries **two** entries,
    one per seat of :data:`JUDGE_SEATS`, in seat order; every other coordinate
    carries one. An empty script is how the ``provider_arm_failure`` induction
    is expressed: ``OfflineProvider`` raises ``ProviderFailure`` with its own
    stable ``TRANSPORT_OR_RESPONSE_ERROR`` when the script is exhausted, so no
    transport is patched and no exception is invented.
    """

    tokens = _checked(induce)
    script: dict[tuple[str, str], tuple[dict[str, Any], ...]] = {}

    for arm in ARM_NAMES:
        for node in NODE_IDS:
            key = _coord_key(arm, node)
            if (arm == PROSE_ARM and node == "response"
                    and "provider_arm_failure" in tokens):
                script[("delivery", key)] = ()
                continue
            script[("delivery", key)] = (
                _entry(delivery_content(arm, node, seed), seed, "delivery:" + key),)

    for coordinate in READING_COORDINATES:
        script[("critic", coordinate)] = (
            _entry(json.dumps(_critic_output(coordinate, seed, tokens),
                              ensure_ascii=False, sort_keys=True),
                   seed, "critic:" + coordinate),)
        script[("defender", coordinate)] = (
            _entry(json.dumps(_defender_output(coordinate, seed),
                              ensure_ascii=False, sort_keys=True),
                   seed, "defender:" + coordinate),)
        script[("judge", coordinate)] = tuple(
            _entry(json.dumps(_judge_output(coordinate, seat, seed, tokens),
                              ensure_ascii=False, sort_keys=True),
                   seed, f"judge:{seat}:{coordinate}")
            for seat in JUDGE_SEATS)
        script[("variator", coordinate)] = (
            _entry(json.dumps(_variator_output(coordinate, seed, tokens),
                              ensure_ascii=False, sort_keys=True),
                   seed, "variator:" + coordinate),)
        # G7: each paraphrase is re-ruled at its own coordinate.
        for suffix in PARAPHRASE_SUFFIXES:
            derived = coordinate + suffix
            script[("judge", derived)] = tuple(
                _entry(json.dumps(
                    _judge_output(derived, seat, seed, tokens, paraphrased=True),
                    ensure_ascii=False, sort_keys=True),
                       seed, f"judge:{seat}:{derived}")
                for seat in JUDGE_SEATS)
        # G11: the re-read that would make an unresolved row stick.
        reread = coordinate + REREAD_SUFFIX
        script[("critic", reread)] = (
            _entry(json.dumps(_critic_output(reread, seed, tokens),
                              ensure_ascii=False, sort_keys=True),
                   seed, "critic:" + reread),)

    for case in CONTRAST_CASES:
        for register in standard.REGISTER_IDS:
            for replicate in CONTRAST_REPLICATES:
                coordinate = f"mark/{case}/{register}/{replicate}"
                script[("marker", coordinate)] = (
                    _entry(json.dumps(_marker_output(coordinate, seed, tokens),
                                      ensure_ascii=False, sort_keys=True),
                           seed, "marker:" + coordinate),)
    return script


# --------------------------------------------------------------------- #
# the scripted provider factory                                          #
# --------------------------------------------------------------------- #


class ScriptedProviders:
    """Builds an ``OfflineProvider`` for one ``(seat role, coordinate)``.

    Two call shapes, one script:

    * :meth:`provider` is the loop's: ``provider(role, coordinate, seat=...)``.
    * :meth:`__call__` is runner v2's ``provider_factory(endpoint, records_dir)``.
      The coordinate is read back out of the records directory, whose tail is
      ``provider/<problem>/<arm>/cycle<NN>/<node>``, so ``send_wave`` can drive
      the same script without learning a new argument.

    ``calls`` counts every provider this factory handed out; the dry run reads
    it beside the provider module's own counter to assert that nothing but
    ``OfflineProvider`` ever ran.
    """

    def __init__(self, *, seed: int = DEFAULT_SEED, induce: Iterable[str] = (),
                 strict: bool = False) -> None:
        self.seed = int(seed)
        self.induce = _checked(induce)
        self.strict = bool(strict)
        self.script = canned_responses(self.seed, induce=self.induce)
        self.calls = 0
        self.handed: list[tuple[str, str]] = []

    # -- the script ----------------------------------------------------- #

    def script_for(self, role: str, coordinate: str, *,
                   seat: str | None = None) -> tuple[dict[str, Any], ...]:
        """The ordered script for one key; one entry per call that key will make."""

        entries = self.script.get((role, coordinate))
        if entries is None:
            if self.strict:
                raise SyntheticError(
                    "SYNTHETIC_COORDINATE_UNSCRIPTED",
                    f"({role!r}, {coordinate!r}) is not in the script")
            entries = (_entry(json.dumps(
                _default_output(role, coordinate, seat or "", self.seed, self.induce),
                ensure_ascii=False, sort_keys=True), self.seed, f"{role}:{coordinate}"),)
        if role == "judge" and seat is not None:
            if seat not in JUDGE_SEATS:
                raise SyntheticError("SYNTHETIC_COORDINATE_UNSCRIPTED",
                                     f"{seat!r} is not one of {JUDGE_SEATS}")
            index = JUDGE_SEATS.index(seat)
            return entries[index:index + 1] if index < len(entries) else ()
        return entries

    def endpoint_for(self, role: str, seat: str | None = None) -> Endpoint:
        """The declared endpoint a seat role spends. Never a credential."""

        name = _SEAT_ENDPOINT.get(seat or role)
        if name is None:
            name = _SEAT_ENDPOINT.get(role, SYNTHETIC_ENDPOINTS[0].name)
        return endpoints_registry()[name]

    # -- the providers -------------------------------------------------- #

    def provider(self, role: str, coordinate: str, records_dir: Path | str, *,
                 seat: str | None = None,
                 endpoint: Endpoint | None = None) -> OfflineProvider:
        """One ``OfflineProvider`` scripted for this key. Opens no socket."""

        if self._times_out(role, coordinate):
            raise SyntheticStepTimeout(f"{role}:{coordinate}")
        self.calls += 1
        self.handed.append((role, coordinate))
        return OfflineProvider(endpoint or self.endpoint_for(role, seat),
                               records_dir,
                               self.script_for(role, coordinate, seat=seat))

    def _times_out(self, role: str, coordinate: str) -> bool:
        return ("step_timeout" in self.induce and role == "delivery"
                and coordinate == _coord_key(FCL_ARM, "response"))

    def __call__(self, endpoint: Endpoint, records_dir: Path | str) -> OfflineProvider:
        """Runner v2's ``provider_factory`` shape: ``(endpoint, records_dir)``."""

        coordinate = self.coordinate_of(records_dir)
        if self._times_out("delivery", coordinate):
            raise SyntheticStepTimeout("delivery:" + coordinate)
        self.calls += 1
        self.handed.append(("delivery", coordinate))
        return OfflineProvider(endpoint, records_dir,
                               self.script_for("delivery", coordinate))

    @staticmethod
    def coordinate_of(records_dir: Path | str) -> str:
        """``provider/<problem>/<arm>/cycle<NN>/<node>`` -> the coordinate key."""

        parts = Path(records_dir).parts[-4:]
        if len(parts) != 4:
            raise SyntheticError("SYNTHETIC_COORDINATE_UNSCRIPTED",
                                 f"{records_dir!r} is not a provider records directory")
        return "/".join(parts)


def provider_factory(*, seed: int = DEFAULT_SEED, induce: Iterable[str] = (),
                     strict: bool = False) -> ScriptedProviders:
    """The scripted offline provider factory, keyed by (seat role, coordinate)."""

    return ScriptedProviders(seed=seed, induce=induce, strict=strict)


# --------------------------------------------------------------------- #
# describe()                                                             #
# --------------------------------------------------------------------- #


@dataclass(frozen=True)
class Induced:
    """One induced failure, the code it should produce, and where it lands."""

    token: str
    code: str
    step: str
    subject: str
    aggregate_code: str | None
    note: str

    def as_dict(self) -> dict[str, Any]:
        return {"token": self.token, "code": self.code, "step": self.step,
                "subject": self.subject, "aggregate_code": self.aggregate_code,
                "note": self.note}


_INDUCED_SUBJECTS: Mapping[str, str] = MappingProxyType({
    # The reading-row inductions read their subject off _READING_INDUCTION, so
    # the coordinate that carries a failure and the coordinate describe() names
    # are the same string by construction.
    **{token: coordinate for coordinate, token in _READING_INDUCTION.items()},
    "provider_arm_failure": FAILED_COORDINATE,
    "custody_mismatch": "custody/pinned_source.txt",
    "step_timeout": _coord_key(FCL_ARM, "response"),
    "baseline_kind_collision": "mark/case-b/E/rep-1",
    "appellate_ruling": "appeals/ruling-0001.json",
})

_INDUCED_NOTES: Mapping[str, str] = MappingProxyType({
    "provider_arm_failure":
        "the prose arm's last node has an empty script, so OfflineProvider raises its own "
        "TRANSPORT_OR_RESPONSE_ERROR; the FCL arm keeps running",
    "custody_mismatch":
        "custody/pins.json disagrees with custody/pinned_source.txt by one byte; the halt, "
        "the erratum, the non-zero exit and the stickiness are the driver's",
    "step_timeout":
        "the scripted provider raises SyntheticStepTimeout instead of sleeping (D4)",
    "ensemble_split":
        "judge-b does not sustain what judge-a sustains; the cell is unresolved and is "
        "never voted",
    "paraphrase_flip":
        "the ruling flips on a paraphrase that held the quoted span byte-identical; no "
        "warrant is registered",
    "non_unique_offset":
        "the critic quotes a sentence carried by both the target record and the referring "
        "record, so the quote resolves twice and no warrant is registered",
    "decisive_point_absent":
        "the judge's decisive_point occurs zero times in case + newline + answer",
    "baseline_kind_collision":
        "the seat marks differs at a kind already in the sealed baseline set, and the "
        "PROGRAM writes same",
    "reread_without_reason":
        "the row's prior outcome is unresolved and the re-read call record carries no "
        "reopen_reason from standard.REOPEN_REASONS",
    "appellate_ruling":
        "an appeal against a validity node, applied at the next invocation, flips a label "
        "through adjudication pass 1 and rewrites no published record",
})


def describe(induce: Iterable[str] = INDUCIBLE) -> tuple[Induced, ...]:
    """Every induced failure, by the code it should produce, in :data:`INDUCIBLE` order."""

    tokens = _checked(induce)
    return tuple(
        Induced(token=token, code=INDUCED_CODES[token], step=_INDUCED_STEPS[token],
                subject=_INDUCED_SUBJECTS[token],
                aggregate_code=_AGGREGATE_CODES.get(token), note=_INDUCED_NOTES[token])
        for token in INDUCIBLE if token in tokens
    )


# --------------------------------------------------------------------- #
# the occurrence                                                         #
# --------------------------------------------------------------------- #


@dataclass(frozen=True)
class Occurrence:
    """Where :func:`build_occurrence` put everything, and what it built."""

    root: Path
    material: Path
    arms: Path
    plan: Path
    manifests: Path
    contrast: Path
    appeal: Path
    custody: Path
    endpoints: Path
    seed: int
    induced: tuple[str, ...]
    plan_id: str
    coordinates: tuple[str, ...]
    reading_plan: Mapping[str, str]
    reading_coordinates: Mapping[str, tuple[str, str, str, str]]

    def as_dict(self) -> dict[str, Any]:
        return {
            "root": str(self.root), "seed": self.seed,
            "induced": list(self.induced), "plan_id": self.plan_id,
            "coordinates": list(self.coordinates),
            "reading_plan": dict(self.reading_plan),
        }


def _projection(owner_record: Mapping[str, Any], owner_coord: Mapping[str, Any],
                consumer_node: str, index: int) -> dict[str, Any]:
    """One exposed projection slot, repeating the source record's own hashes."""

    body_ref = owner_record["body_sha256"]
    commitments_ref = owner_record["commitments_sha256"]
    projection_id = f"p.{consumer_node}.{index}"
    artifact_id = _artifact_id(f"projection:{owner_coord['arm']}:{projection_id}",
                               body_ref, commitments_ref)
    return {
        "artifact_id": artifact_id,
        "body_ref": body_ref,
        "commitments_ref": commitments_ref,
        "machine_projection": True,
        "projection_id": projection_id,
        "selected_source": {
            "absent": False,
            "aliases_previous": False,
            "artifact_id": owner_record["artifact_id"],
            "body_sha256": owner_record["body_sha256"],
            "commitments_sha256": owner_record["commitments_sha256"],
            "coordinate": dict(owner_coord),
            "delivery_status": owner_record["delivery_status"],
            "envelope_status": owner_record["envelope_status"],
            "public_text_sha256": owner_record["public_text_sha256"],
            "source": owner_coord["node"],
            "view": "both",
        },
    }


def _brief(node: str, task_artifact_id: str, projections: Sequence[Mapping[str, Any]],
           problem_prose: str) -> str:
    """The rendered brief. Every ``[label] (alias)`` line indexes its own slot."""

    lines = [f"# {node}", "", _NODE_INSTRUCTIONS[node], "",
             "## Original problem (task)",
             f"[{task_artifact_id[:16]}] (h005.task.v1)", problem_prose, ""]
    for projection in projections:
        alias = projection["projection_id"]
        lines += [f"## Selected input {projection['selected_source']['source']} ({alias})",
                  f"[{projection['artifact_id'][:16]}] (h005.{TEMPLATE_ID}.{alias})",
                  "Source account: "
                  + projection["selected_source"]["coordinate"]["problem"]
                  + "/" + projection["selected_source"]["coordinate"]["arm"]
                  + "/cycle-" + str(projection["selected_source"]["coordinate"]["cycle"])
                  + "/" + projection["selected_source"]["source"]
                  + "; selected view: both", ""]
    return "\n".join(lines)


def _artifact_record(arm: str, node: str, seed: int) -> dict[str, Any]:
    """One authored artifact record, decoded exactly as ``envelope_unwrap`` would."""

    content = delivery_content(arm, node, seed)
    envelope = json.loads(content)
    body, commitments = envelope["body"], envelope["commitments"]
    body_sha = _sha(body.encode("utf-8"))
    commitments_sha = _sha(commitments.encode("utf-8"))
    coord = {"problem": PROBLEM_ID, "arm": arm, "cycle": 1, "node": node}
    artifact_id = _artifact_id(
        f"{PROBLEM_ID}/{arm}/cycle-1/{node}", body_sha, commitments_sha)
    return {
        "schema": "minireason.h005.artifact.v1",
        "artifact_id": artifact_id,
        "body": body,
        "body_ref": body_sha,
        "body_sha256": body_sha,
        "commitments": commitments,
        "commitments_ref": commitments_sha,
        "commitments_sha256": commitments_sha,
        "coordinate": coord,
        "delivery_status": "COMPLETE",
        "envelope_status": "AUTHORED",
        "public_text_sha256": _sha(content.encode("utf-8")),
    }


def _task_artifact(seed: int) -> dict[str, Any]:
    prose = material_document(seed)["problems"][0]["prose"]
    body_ref = _sha(prose.encode("utf-8"))
    empty = _sha(b"")
    return {"artifact_id": _artifact_id("task", body_ref, empty),
            "body_ref": body_ref, "commitments_ref": empty}


def _manifest_document(seed: int) -> dict[str, Any]:
    """A stand-in manifest (D2). The importer pins its bytes and never reads them."""

    return {
        "schema_version": "creib.mini.manifest.v1",
        "manifest_id": "h005." + TEMPLATE_ID,
        "problem": "One template invocation in the synthetic dry-run occurrence.",
        "synthetic": (
            "A stand-in written by minireason.loop.synthetic. It is pinned by "
            "plan.json and is never compiled here; pass freeze= to have runner v2 "
            "write the compiled manifest in its place."
        ),
        "nodes": list(NODE_IDS),
        "variant": _variant(seed, "manifest"),
    }


def _plan_document(material_raw: bytes, arms_raw: bytes,
                   manifest_pins: Mapping[str, str], seed: int) -> dict[str, Any]:
    arms = arms_document()["arms"]
    registry = endpoints_registry()
    caps: dict[str, int] = {}
    for arm, spec in arms.items():
        endpoint = registry[spec["endpoint"]]
        caps[endpoint.key_env] = min(caps.get(endpoint.key_env, 5),
                                     endpoint.max_concurrency)
    body = {
        "schema": "minireason.h005.plan.v1",
        "arms": {arm: {"declared_name": arm, "mode": "offline", **dict(spec)}
                 for arm, spec in arms.items()},
        "arms_sha256": _sha(arms_raw),
        "material_sha256": _sha(material_raw),
        "manifests": dict(manifest_pins),
        "providers": {endpoint.name: dict(row)
                      for endpoint, row in zip(SYNTHETIC_ENDPOINTS, _ENDPOINT_ROWS)},
        "provider_mode": "offline",
        "scope": {"problems": [PROBLEM_ID], "cycles": [1]},
        "key_environment_names": sorted(caps),
        "max_concurrent_requests_per_key_env": dict(sorted(caps.items())),
        "max_concurrent_requests_total": sum(caps.values()),
        "automatic_retries": 0,
        "cycle_definition": "one complete template invocation",
        "max_calls": len(ARM_NAMES) * len(NODE_IDS),
        "synthetic": {
            "generator": SYNTHETIC_SCHEMA,
            "seed": int(seed),
            "note": ("Frozen by minireason.loop.synthetic, not by runner v2's plan_body; "
                     "see that module's deviation D2."),
        },
    }
    body["plan_id"] = _digest(body)
    return body


def runner_freeze(repo: Path | str) -> Callable[[Path, Path, Path], Mapping[str, Any]]:
    """A ``freeze=`` callable that lets runner v2 write ``plan.json`` (D2).

    The import of ``tools/multicycle_commitment_study_multi_v2`` is lazy and
    local, because importing it inserts two repository paths into ``sys.path``
    and pulls in ``creib``; nothing at module scope here does that. The returned
    callable installs :func:`endpoints_registry` through the runner's own
    ``set_registry`` seam and **leaves it installed**: ``verify``,
    ``prepare_wave`` and ``send_round`` resolve the registry again, and a plan
    frozen against one registry may not be dispatched against another. Restore
    the shipped registry with ``set_registry(None)`` when the run is over.
    """

    repository = Path(repo).resolve()
    def freeze(occurrence: Path, material: Path, arms: Path) -> Mapping[str, Any]:
        if str(repository) not in sys.path:
            sys.path.insert(0, str(repository))
        runner = __import__("tools.multicycle_commitment_study_multi_v2",
                            fromlist=["initialize"])
        runner.set_registry(endpoints_registry())
        return runner.initialize(repository, occurrence, material, arms)

    return freeze


def build_occurrence(directory: Path | str, *, induce: Iterable[str] = (),
                     seed: int = DEFAULT_SEED,
                     freeze: Callable[[Path, Path, Path], Mapping[str, Any]] | None = None,
                     ) -> Occurrence:
    """Write one complete synthetic occurrence under ``directory``.

    The directory is created if it does not exist and must be empty of
    occurrence files; every byte written is a pure function of ``(seed,
    induce)``. Returns an :class:`Occurrence` naming every path and the
    reading plan a reader is expected to fill the table's four empty cells
    with.

    ``freeze`` is the runner-v2 seam (deviation D2): a callable
    ``(occurrence_dir, material_path, arms_path) -> plan mapping`` that has
    itself written ``plan.json`` and ``manifests/``. Without it this module
    writes both, and the plan says so in its own ``synthetic`` block.
    """

    tokens = _checked(induce)
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)

    # -- material, arms ------------------------------------------------- #
    material = material_document(seed)
    material_raw = _encoded(material)
    (root / "material.json").write_bytes(material_raw)
    arms_raw = _encoded(arms_document())
    (root / "arms.json").write_bytes(arms_raw)

    # -- plan and manifests --------------------------------------------- #
    if freeze is None:
        manifest_raw = _encoded(_manifest_document(seed))
        (root / "manifests").mkdir(parents=True, exist_ok=True)
        (root / "manifests" / (TEMPLATE_ID + ".json")).write_bytes(manifest_raw)
        plan = _plan_document(material_raw, arms_raw,
                              {TEMPLATE_ID: _sha(manifest_raw)}, seed)
        (root / "plan.json").write_bytes(_encoded(plan))
    else:
        plan = dict(freeze(root, root / "material.json", root / "arms.json"))

    # -- deliveries ------------------------------------------------------ #
    records: dict[tuple[str, str], dict[str, Any]] = {}
    for arm in ARM_NAMES:
        for node in NODE_IDS:
            records[(arm, node)] = _artifact_record(arm, node, seed)

    task = _task_artifact(seed)
    problem_prose = material["problems"][0]["prose"]
    coordinates: list[str] = []
    moments = iter(RECORDED_MOMENTS)
    waves: dict[str, dict[str, Any]] = {}

    # Wave order is node order; inside a wave, arm order. `order` in the
    # importer is (wave ordinal, wave index, coordinate), so this fixes it.
    for wave_index, node in enumerate(NODE_IDS, start=1):
        wave_id = f"wave{wave_index:04d}"
        waves[wave_id] = {
            "schema": "minireason.h005.wave.v1",
            "wave_id": wave_id,
            "plan_id": plan["plan_id"],
            "problem": PROBLEM_ID,
            "cycle": 1,
            "coordinates": [],
            "request_hashes": {},
        }
        for arm in ARM_NAMES:
            record = records[(arm, node)]
            coord = record["coordinate"]
            projections = [
                _projection(records[(arm, binding["source"])],
                            records[(arm, binding["source"])]["coordinate"], node, index)
                for index, binding in enumerate(_NODE_INPUTS[node])
            ]
            brief = _brief(node, task["artifact_id"], projections, problem_prose)
            trace = {
                "schema": "minireason.h005.trace.v1",
                "coordinate": dict(coord),
                "template_id": TEMPLATE_ID,
                "paired_template_id": TEMPLATE_ID,
                "fixture": ("Synthetic occurrence; every recorded moment is a fiction and "
                            "no provider was contacted."),
                "origin_aliases_previous": False,
                "barrier_dependencies": [],
                "original_brief": brief,
                "original_brief_sha256": _sha(brief.encode("utf-8")),
                "projection_artifacts": projections,
                "rendering": "synthetic_render",
                "task_artifact": dict(task),
                "visible_sources": [dict(projection["selected_source"])
                                    for projection in projections],
            }
            request = {
                "schema": "minireason.h005.request.v1",
                "coordinate": dict(coord),
                "plan_id": plan["plan_id"],
                "template_id": TEMPLATE_ID,
                "paired_template_id": TEMPLATE_ID,
                "dependencies": [dict(records[(arm, binding["source"])]["coordinate"])
                                 for binding in _NODE_INPUTS[node]],
                "messages": [
                    {"role": "system", "content": _SYSTEM},
                    {"role": "user", "content": brief},
                ],
                "trace_sha256": _digest(trace),
            }
            request["messages_sha256"] = _digest(request["messages"])
            request_sha = _digest(request)

            provider_request = {
                "schema_version": "minireason.call.v2",
                "synthetic": True,
                "call_number": 1,
                "coordinate": {"harness": "H005", **dict(coord)},
                "url": None,
                "not_contacted_url": endpoints_registry()[_ARM_ENDPOINT[arm]].chat_url,
                "method": "POST(offline)",
                "request_header_names": [],
                "request_sha256": request_sha,
            }
            content = delivery_content(arm, node, seed)
            provider_response = {
                "schema_version": "minireason.call.v2",
                "synthetic": True,
                "call_number": 1,
                "status": "COMPLETE",
                "finish_reason": "stop",
                "content": content,
                "usage": _entry(content, seed, f"delivery:{PROBLEM_ID}/{arm}/cycle01/{node}")["usage"],
                "reasoning_content_present": False,
                "reasoning_content_persisted": False,
                "credential_redaction": False,
            }
            provider_dir = (root / "provider" / PROBLEM_ID / arm / "cycle01" / node)
            moment = next(moments)
            ended = ("provider_arm_failure" in tokens
                     and f"{PROBLEM_ID}/{arm}/cycle01/{node}" == FAILED_COORDINATE)

            receipt = {
                "schema": "minireason.h005.receipt.v1",
                "coordinate": dict(coord),
                "artifact_sha256": _sha(_encoded(record)),
                "envelope_repairs": [],
                "envelope_status": record["envelope_status"],
                "failure_code": None,
                "failure_type": None,
                "finish_reason": "stop",
                "finished_utc": moment,
                "provider_request_sha256": _sha(_encoded(provider_request)),
                "provider_response_sha256": _sha(_encoded(provider_response)),
                "reasoning_content_present": False,
                "request_sha256": request_sha,
                "returned_model": endpoints_registry()[_ARM_ENDPOINT[arm]].model,
                "status": record["delivery_status"],
                "strict_parse_would_succeed": True,
                "usage": provider_response["usage"],
            }
            attempt = {
                "schema": "minireason.h005.attempt.v1",
                "automatic_retry": False,
                "coordinate": dict(coord),
                "published_commit": "0" * 40,
                "request_sha256": request_sha,
                "started_utc": receipt["finished_utc"],
                "wave_id": wave_id,
            }

            stem = f"{PROBLEM_ID}/{arm}/cycle01/{node}"
            _write(root / "traces" / f"{stem}.json", trace)
            _write(root / "requests" / f"{stem}.json", request)
            _write(root / "attempts" / f"{stem}.json", attempt)
            if ended:
                # The arm ended here: the provider raised, so there is a FAILED
                # receipt and no artifact, no public text and no provider call
                # bytes. `discover_scope` globs `artifacts/`, so the coordinate
                # is simply not in the import's scope - which is what an ended
                # arm looks like from the outside. Every other arm runs on.
                _write(root / "responses" / f"{stem}.json", {
                    "schema": "minireason.h005.receipt.v1",
                    "coordinate": dict(coord),
                    "status": "FAILED",
                    "envelope_status": "ABSENT",
                    "failure_type": "ProviderFailure",
                    "failure_code": INDUCED_CODES["provider_arm_failure"],
                    "finish_reason": None,
                    "finished_utc": moment,
                    "request_sha256": request_sha,
                    "provider_request_sha256": None,
                    "provider_response_sha256": None,
                    "reasoning_content_present": False,
                    "returned_model": None,
                    "envelope_repairs": [],
                    "strict_parse_would_succeed": False,
                    "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                })
            else:
                _write(provider_dir / "call-0001.request.json", provider_request)
                _write(provider_dir / "call-0001.response.json", provider_response)
                _write(root / "artifacts" / f"{stem}.json", record)
                _write(root / "responses" / f"{stem}.json", receipt)
                _write_text(root / "responses" / f"{stem}.txt", content)

            if not ended:
                coordinates.append(f"{PROBLEM_ID}/{arm}/cycle01/{node}")
            waves[wave_id]["coordinates"].append(dict(coord))
            waves[wave_id]["request_hashes"][
                f"{PROBLEM_ID}/{arm}/cycle-1/{node}"] = request_sha

    for wave_id, wave in waves.items():
        _write(root / "waves" / f"{wave_id}.json", wave)

    # -- the side fixtures ---------------------------------------------- #
    _write(root / "contrast.json", contrast_leg(seed))
    ruling = appellate_ruling(seed)
    ruling["induced"] = "appellate_ruling" in tokens
    _write(root / "appeals" / "ruling-0001.json", ruling)
    _write(root / "endpoints.json", endpoints_document())

    pinned = ("A pinned source file of the synthetic run.\n"
              f"Variant {_variant(seed, 'custody')}.\n")
    _write_text(root / "custody" / "pinned_source.txt", pinned)
    recorded = pinned if "custody_mismatch" not in tokens else pinned.replace(
        "pinned source file", "pinned source FILE", 1)
    _write(root / "custody" / "pins.json", {
        "schema": SYNTHETIC_SCHEMA + ".pins",
        "pins": {"pinned_source.txt": _sha(recorded.encode("utf-8"))},
        "drifted": "custody_mismatch" in tokens,
    })

    _write(root / "SYNTHETIC.json", {
        "schema": SYNTHETIC_SCHEMA,
        "seed": int(seed),
        "induced": sorted(tokens),
        "induced_codes": {token: INDUCED_CODES[token] for token in sorted(tokens)},
        "reading_plan": dict(READING_PLAN),
        "reading_coordinates": {name: list(row)
                                for name, row in READING_COORDINATES.items()},
        "unresolvable_refs": [list(row) for row in UNRESOLVABLE_REFS],
        "new_codes": dict(NEW_CODES),
    })

    return Occurrence(
        root=root,
        material=root / "material.json",
        arms=root / "arms.json",
        plan=root / "plan.json",
        manifests=root / "manifests",
        contrast=root / "contrast.json",
        appeal=root / "appeals" / "ruling-0001.json",
        custody=root / "custody",
        endpoints=root / "endpoints.json",
        seed=int(seed),
        induced=tuple(sorted(tokens)),
        plan_id=str(plan["plan_id"]),
        coordinates=tuple(coordinates),
        reading_plan=READING_PLAN,
        reading_coordinates=READING_COORDINATES,
    )
