# Vendored from AHepi/DeepReason@9607fba src/deepreason/harness.py (MIT, see src/deepreason_core/LICENSE); see docs/sources/deepreason-core-provenance.json
"""Harness core (spec §1–§4): registration, materialized view, replay.

Live registration validates well-formedness (§2), persists records to the
content-addressed object store, then builds an event and applies it via the
SAME code path replay uses — so reopening a harness from its log reproduces
state byte-for-byte (P0 acceptance). Adjudication (§4) recomputes after
every registration; its only inputs are att and dep (§0).
"""

from collections.abc import Callable, Iterable
from datetime import datetime, timezone
import json
from pathlib import Path

from deepreason_core.adjudication.edges import (
    DependenceCycleError,
    build_att,
    build_dep,
    toposort,
)
from deepreason_core.adjudication.grounded import label0 as compute_label0
from deepreason_core.adjudication.support import final_labels
from deepreason_core.canonical import canonical_json
from deepreason_core.log.event_log import EventLog
from deepreason_core.ontology import (
    Artifact,
    Commitment,
    EpistemicState,
    Event,
    Interface,
    LLMCall,
    Problem,
    Provenance,
    Rule,
    StateDiff,
    Warrant,
)
from deepreason_core.ontology.problem import POPPER_BATTERY
from deepreason_core.storage.blobs import (
    BlobStore,
    FencedBlobStore,
    historical_sealed_refs,
)
from deepreason_core.storage.objects import ObjectStore


class WellFormednessError(ValueError):
    """A registration would violate the formation rules (spec §2)."""


class ReadOnlyHarnessError(RuntimeError):
    """A mutation was attempted through a time-travel materialization."""


# --------------------------------------------------------------------- #
# Trial transcript (inlined from informal/trial.py, spec §2/§3 guard)    #
# --------------------------------------------------------------------- #


def conforming_transcript(blobs, trace_ref: str) -> bool:
    """Well-formedness (§2): a rubric-derived warrant's trace_ref must hold
    a conforming trial transcript — re-checkable by program."""
    try:
        data = json.loads(blobs.get(trace_ref))
    except (KeyError, ValueError):
        return False
    if not isinstance(data, dict):
        return False
    ruling = data.get("ruling") or {}
    decisive = ruling.get("decisive_point", "")
    exchange = f"{data.get('case', '')}\n{data.get('answer', '')}"
    return bool(
        data.get("case")
        and data.get("answer")
        and decisive
        and decisive in exchange
        and isinstance(data.get("checks"), dict)
    )


def transcript_blob(harness, *, case: str, answer: str, decisive_point: str,
                    checks: dict | None = None, **meta) -> str:
    """Store a transcript; returns the trace_ref blob hash."""
    data = {"case": case, "answer": answer,
            "ruling": {"verdict": "fail", "decisive_point": decisive_point},
            "checks": checks or {}, **meta}
    return harness.blobs.put(canonical_json(data))


class Harness:
    def __init__(
        self,
        root: Path | str,
        *,
        upto_seq: int | None = None,
        read_only: bool | None = None,
        clock: Callable[[], str] | None = None,
    ) -> None:
        """Open (or create) a harness at ``root``; ``upto_seq`` truncates the
        replay for time-travel views (prefer the ``Harness.at`` spelling).

        Replay applies every event but adjudicates ONCE at the end: the
        grounded-extension fixpoint is a pure function of the final graph,
        so per-event adjudication during replay is discarded work (it made
        reopening an N-event log superlinear)."""
        self.root = Path(root)
        # Optional deterministic event clock: a callable returning the iso8601
        # string stamped on Event.ts. Default None keeps the wall-clock
        # behavior. An offline importer replaying recorded evidence must not
        # fork its log on machine load (spec §0 replay determinism).
        self._clock = clock
        self._read_only = (upto_seq is not None) if read_only is None else read_only
        if self._read_only:
            if not self.root.exists():
                raise FileNotFoundError(f"read-only harness root does not exist: {self.root}")
        else:
            self.root.mkdir(parents=True, exist_ok=True)
        self.blobs = BlobStore(self.root / "blobs", read_only=self._read_only)
        self.objects = ObjectStore(self.root / "objects", read_only=self._read_only)
        self.log = EventLog(self.root / "log.jsonl", read_only=self._read_only)
        self._reset()
        revealed_artifact_ids: set[str] = set()
        for event in self.log.read(upto_seq=upto_seq):
            if event.rule == Rule.REVEAL:
                revealed_artifact_ids.update(event.inputs)
            self._apply_event(event, adjudicate=False)
        self._adjudicate()
        if self._read_only:
            self.blobs = FencedBlobStore(
                self.blobs,
                historical_sealed_refs(
                    self.blobs, self.state.artifacts, revealed_artifact_ids
                ),
            )

    _TAIL_CAP = 512  # bounded in-memory event tail (windows are ~CAPTURE_W)

    def _reset(self) -> None:
        self.state = EpistemicState()
        self.commitments: dict[str, Commitment] = {}
        self.warrants: dict[str, Warrant] = {}
        self._next_seq = 0
        # Derived caches — pure functions of the immutable, append-only
        # history, so they never need invalidation, only extension.
        self._tail: list[Event] = []

    @classmethod
    def at(cls, root: Path | str, seq: int) -> "Harness":
        """Time-travel: the harness as of event ``seq`` (spec §1). Read-only —
        do not register into a truncated view."""
        return cls(root, upto_seq=seq, read_only=True)

    def _ensure_writable(self) -> None:
        if self._read_only:
            raise ReadOnlyHarnessError("time-travel harness is read-only")

    # ------------------------------------------------------------------ #
    # Registration (live path: validate -> persist -> commit event)      #
    # ------------------------------------------------------------------ #

    def register_commitment(self, commitment: Commitment) -> Commitment:
        self._ensure_writable()
        if commitment.id in self.commitments:
            existing = self.commitments[commitment.id]
            if existing != commitment:
                raise WellFormednessError(
                    f"commitment id {commitment.id!r} conflicts with its registered record"
                )
            return existing
        self.objects.put("commitment", commitment)
        self._commit(Rule.REGISTER, inputs=[], outputs=[commitment.id])
        return self.commitments[commitment.id]

    def register_problem(self, problem: Problem) -> Problem:
        self._ensure_writable()
        # Popper battery auto-pinned (spec §1).
        criteria = list(problem.criteria) + [
            b for b in POPPER_BATTERY if b not in problem.criteria
        ]
        payload = problem.model_dump(mode="json", by_alias=True)
        payload["criteria"] = criteria
        problem = Problem.model_validate(payload)
        if problem.id in self.state.problems:
            existing = self.state.problems[problem.id]
            if existing != problem:
                raise WellFormednessError(
                    f"problem id {problem.id!r} conflicts with its registered record"
                )
            return existing
        self.objects.put("problem", problem)
        self._commit(Rule.SPAWN, inputs=list(problem.provenance.from_), outputs=[problem.id])
        return self.state.problems[problem.id]

    def create_artifact(
        self,
        content: bytes | str,
        *,
        codec: str = "utf8",
        interface: Interface | None = None,
        provenance: Provenance | None = None,
        warrants: Iterable[Warrant] = (),
        problem_id: str | None = None,
        rule: Rule = Rule.REGISTER,
        llm: LLMCall | None = None,
    ) -> Artifact:
        """Store content, compute the canonical id, and register."""
        self._ensure_writable()
        interface = interface or Interface()
        if isinstance(content, bytes):
            content_ref = self.blobs.put(content)
        else:
            content_ref = f"inline:{content}"
        warrants = list(warrants)
        artifact = Artifact(
            id=Artifact.compute_id(content_ref, codec, interface),
            content_ref=content_ref,
            codec=codec,
            interface=interface,
            warrants=[w.id for w in warrants],
            provenance=provenance or Provenance(role="user"),
        )
        return self.register_artifact(
            artifact, warrants=warrants, problem_id=problem_id, rule=rule, llm=llm
        )

    def register_artifact(
        self,
        artifact: Artifact,
        *,
        warrants: Iterable[Warrant] = (),
        problem_id: str | None = None,
        rule: Rule = Rule.REGISTER,
        llm: LLMCall | None = None,
    ) -> Artifact:
        self._ensure_writable()
        # register_batch handles both content dedupe and any NEW carriage
        # declared for an existing content artifact.
        self.register_batch(
            [(artifact, list(warrants))], problem_id=problem_id, rule=rule, llm=llm
        )
        return self.state.artifacts[artifact.id]

    def register_batch(
        self,
        entries: list[tuple[Artifact, list[Warrant]]],
        *,
        problem_id: str | None = None,
        rule: Rule = Rule.REGISTER,
        llm: LLMCall | None = None,
    ) -> list[Artifact]:
        """Register artifacts and explicit warrant-carriage relations.

        Content-addressed artifacts dedupe, but a new ``(artifact, warrant)``
        pair still commits. This is what lets identical criticism prose attack
        more than one target without changing the prose artifact's id.
        """
        self._ensure_writable()
        candidate = dict(self.state.artifacts)
        accepted_entries: list[tuple[Artifact, list[Warrant]]] = []
        carry_add: list[tuple[str, str]] = []
        known_carries = set(self.state.carries)
        new_warrants: dict[str, Warrant] = {}
        for artifact, warrants in entries:
            is_new = artifact.id not in candidate
            if not is_new:
                existing_artifact = candidate[artifact.id]
                if (
                    existing_artifact.content_ref != artifact.content_ref
                    or existing_artifact.codec != artifact.codec
                    or existing_artifact.interface != artifact.interface
                ):
                    raise WellFormednessError(
                        f"artifact id {artifact.id} conflicts with its content identity"
                    )
            provided = {w.id: w for w in warrants}
            # Every attack edge carries a registered warrant (§2).
            for wid in artifact.warrants:
                w = provided.get(wid) or new_warrants.get(wid) or self.warrants.get(wid)
                if w is None:
                    raise WellFormednessError(f"carried warrant not provided/registered: {wid}")
                if (
                    wid in provided
                    and wid in self.warrants
                    and provided[wid] != self.warrants[wid]
                ):
                    raise WellFormednessError(
                        f"warrant id {wid} conflicts with the registered record"
                    )
                # A warrant's validity node may be an earlier artifact in this
                # same batch, not only one already in state (one Conj event can
                # carry both the nu and the critic that cites it).
                self._validate_warrant(w, known_artifacts=candidate)
                pair = (artifact.id, wid)
                if pair not in known_carries:
                    carry_add.append(pair)
                    known_carries.add(pair)
                if wid in provided and wid not in self.warrants:
                    existing = new_warrants.get(wid)
                    if existing is not None and existing != provided[wid]:
                        raise WellFormednessError(
                            f"warrant id {wid} has conflicting records in one batch"
                        )
                    new_warrants[wid] = provided[wid]
            if not is_new:
                # The content object already exists, but newly declared
                # carriage above is still a real append-only graph relation.
                continue
            # Interface commitments must be registered (§2).
            for cid in artifact.interface.commitments:
                if cid not in self.commitments:
                    raise WellFormednessError(f"interface commitment not registered: {cid}")
            candidate[artifact.id] = artifact
            accepted_entries.append((artifact, warrants))
        if not accepted_entries and not carry_add:
            return []
        # dep must remain a DAG (§1): check the materialized edge set.
        try:
            toposort(set(candidate), build_dep(candidate))
        except DependenceCycleError as e:
            raise WellFormednessError(str(e)) from e

        outputs: list[str] = []
        for wid, warrant in new_warrants.items():
            self.objects.put("warrant", warrant)
            outputs.append(wid)
        for artifact, _ in accepted_entries:
            self.objects.put("artifact", artifact)
            outputs.append(artifact.id)
        # Existing callers detect content dedupe and record a shared LLM call
        # as a Measure. A carriage-only event therefore leaves llm unset so the
        # same call is not counted twice; a newly registered artifact keeps the
        # original attachment behavior.
        event_llm = llm if accepted_entries else None
        self._commit(
            rule,
            inputs=[*([problem_id] if problem_id else [])],
            outputs=outputs,
            llm=event_llm,
            carry_add=carry_add,
        )
        return [self.state.artifacts[a.id] for a, _ in accepted_entries]

    def carried_warrant_ids(self, artifact_id: str) -> list[str]:
        """Warrants explicitly carried by an artifact, in registration order.

        The materialized relation includes legacy Artifact.warrants entries,
        so callers do not need to distinguish old and new logs.
        """
        return [wid for carrier, wid in self.state.carries if carrier == artifact_id]

    def carrier_ids(self, warrant_id: str) -> list[str]:
        """Every artifact carrying ``warrant_id``, in registration order."""
        return [carrier for carrier, wid in self.state.carries if wid == warrant_id]

    def record_measure(
        self,
        *,
        hv: dict[str, float] | None = None,
        reach: dict[str, float] | None = None,
        addr: list[tuple[str, str]] | None = None,
        inputs: Iterable[str] = (),
        llm: LLMCall | None = None,
    ) -> Event:
        """Measure event (spec §3/§6): estimates steer attention, never
        status — they land in state.hv/state.reach only. ``addr`` carries the
        reach amendment (Def 3.7): full cross-problem survival registers the
        artifact as addressing the foreign problem (structure, not status)."""
        return self._commit(
            Rule.MEASURE,
            inputs=list(inputs),
            outputs=[],
            llm=llm,
            hv_set=hv or {},
            reach_set=reach or {},
            addr_add=addr or [],
        )

    def _validate_warrant(self, warrant: Warrant, known_artifacts=None) -> None:
        known = self.state.artifacts if known_artifacts is None else known_artifacts
        if warrant.validity_node not in known:
            raise WellFormednessError(
                f"warrant {warrant.id}: validity_node {warrant.validity_node} not registered"
            )
        if warrant.commitment and warrant.commitment not in self.commitments:
            raise WellFormednessError(
                f"warrant {warrant.id}: commitment {warrant.commitment} not registered"
            )
        # §2: every rubric-derived demonstrative warrant's trace_ref must
        # contain a conforming trial transcript (§3 guard, unbypassable).
        if warrant.commitment and self.commitments[warrant.commitment].eval.startswith(
            "rubric:"
        ):
            if warrant.trace_ref is None or not conforming_transcript(
                self.blobs, warrant.trace_ref
            ):
                raise WellFormednessError(
                    f"warrant {warrant.id}: rubric-derived but trace_ref lacks a "
                    "conforming trial transcript (§2/§3)"
                )

    # ------------------------------------------------------------------ #
    # Event application (shared by live path and replay)                 #
    # ------------------------------------------------------------------ #

    def _commit(
        self,
        rule: Rule,
        inputs: list[str],
        outputs: list[str],
        llm: LLMCall | None = None,
        hv_set: dict[str, float] | None = None,
        reach_set: dict[str, float] | None = None,
        addr_add: list[tuple[str, str]] | None = None,
        carry_add: list[tuple[str, str]] | None = None,
    ) -> Event:
        self._ensure_writable()
        event = Event(
            seq=self._next_seq,
            ts=(
                self._clock() if self._clock is not None
                else datetime.now(timezone.utc).isoformat()
            ),
            rule=rule,
            inputs=inputs,
            outputs=outputs,
            llm=llm,
            state_diff=StateDiff(hv_set=hv_set or {}, reach_set=reach_set or {},
                                 addr_add=addr_add or [], carry_add=carry_add or []),
        )
        try:
            state_diff = self._apply_event(event)
            event = event.model_copy(update={"state_diff": state_diff})
            self._tail[-1] = event  # _apply_event saw the provisional immutable event
            self.log.append(event)
        except Exception:
            # Object/blob writes are content-addressed and may remain orphaned,
            # but the live materialization must never outrun the durable log.
            self._reset()
            for durable in self.log.read():
                self._apply_event(durable, adjudicate=False)
            self._adjudicate()
            raise
        return event

    def _apply_event(self, event: Event, adjudicate: bool = True) -> StateDiff | None:
        """Apply one event to the materialized view. ``adjudicate=False`` skips
        the grounded-extension recompute and the per-event diff — used by
        replay, which adjudicates once at the end and discards the diffs."""
        pre_att = set(self.state.att)
        pre_dep = set(self.state.dep)
        pre_status = dict(self.state.status)
        a_add: list[str] = []
        pi_add: list[str] = []
        if event.rule == Rule.REVEAL:
            # Reveal (§10.5): move sealed bytes from the holdout namespace
            # into the blob store — idempotent, so replay reproduces it.
            for aid in event.inputs:
                artifact = self.state.artifacts.get(aid)
                if artifact is None:
                    continue
                sealed = self.root / "holdout" / artifact.content_ref
                if sealed.exists() and not self._read_only:
                    self.blobs.put(sealed.read_bytes())
        for oid in event.outputs:
            schema, obj = self.objects.get(oid)
            if schema == "commitment":
                self.commitments[obj.id] = obj
            elif schema == "warrant":
                self.warrants[obj.id] = obj
            elif schema == "problem":
                self.state.problems[obj.id] = obj
                pi_add.append(obj.id)
            elif schema == "artifact":
                self.state.artifacts[obj.id] = obj
                a_add.append(obj.id)
                # Backward compatibility: historical records embedded carriage
                # on the artifact. Materialize those entries into the explicit
                # relation during replay.
                for wid in obj.warrants:
                    pair = (obj.id, wid)
                    if pair not in self.state.carries:
                        self.state.carries.append(pair)
                for pid in event.inputs:
                    if pid in self.state.problems and (obj.id, pid) not in self.state.addr:
                        self.state.addr.append((obj.id, pid))
        for aid, value in event.state_diff.hv_set.items():
            self.state.hv[aid] = value
        for aid, value in event.state_diff.reach_set.items():
            self.state.reach[aid] = value
        for aid, pid in event.state_diff.addr_add:
            if pid in self.state.problems and (aid, pid) not in self.state.addr:
                self.state.addr.append((aid, pid))
        for carrier, wid in event.state_diff.carry_add:
            if (
                carrier in self.state.artifacts
                and wid in self.warrants
                and (carrier, wid) not in self.state.carries
            ):
                self.state.carries.append((carrier, wid))
        self._next_seq = event.seq + 1
        self._tail.append(event)
        if len(self._tail) > self._TAIL_CAP:
            del self._tail[: -self._TAIL_CAP]
        if not adjudicate:
            return None  # replay recomputes status once after the full walk
        self._adjudicate()
        return StateDiff(
            att_add=sorted(set(self.state.att) - pre_att),
            dep_add=sorted(set(self.state.dep) - pre_dep),
            a_add=a_add,
            pi_add=pi_add,
            status_changed=sorted(
                i for i in self.state.artifacts if pre_status.get(i) != self.state.status.get(i)
            ),
            hv_set=event.state_diff.hv_set,
            reach_set=event.state_diff.reach_set,
            addr_add=event.state_diff.addr_add,
            carry_add=event.state_diff.carry_add,
        )

    # ------------------------------------------------------------------ #
    # Adjudication (Adj: after any registration, spec §3/§4)             #
    # ------------------------------------------------------------------ #

    def _adjudicate(self) -> None:
        nodes = set(self.state.artifacts)
        att = build_att(
            self.state.artifacts,
            self.warrants,
            self.commitments,
            self.state.carries,
        )
        dep = build_dep(self.state.artifacts)
        final = final_labels(compute_label0(nodes, att), dep)
        self.state.att = sorted(att)
        self.state.dep = sorted(dep)
        # Insertion (= registration) order keeps serialization deterministic.
        self.state.status = {i: final[i] for i in self.state.artifacts}
        # P0: the isolation/integration driver (§7 L2) is stubbed with knobs
        # (spec §16 P0 row), so conn is the zero map rather than a live
        # conn_map(dep, status). Nothing in P0 reads it, and adjudication
        # never could: its only inputs are att and dep (§0/§4).
        self.state.conn = {aid: 0 for aid in self.state.artifacts}
