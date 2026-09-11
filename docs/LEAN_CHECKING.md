# Optional Lean compatibility route

Lean checking is a separate material observation. It is never an admission requirement for a language specimen, a prose conjecture, a criticism, or a promoted problem. A compiler receipt concerns particular source bytes, a compiler build and its imported environment. It does not certify the proposed interpretation, expressive adequacy, explanatory bearing or creativity. A rejected or unexecuted Lean proposal remains available for the frozen expression study.

## Current capability, 2026-09-11

The official Linux x86_64 [Lean v4.19.0 archive](https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst) was downloaded and extracted outside this repository. Its locally measured SHA-256 is `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`, and its size is 343842845 bytes. This digest now pins reproducibility; it is not an independently authenticated vendor checksum. The compiler version is inferred from that pinned release, because the executable did not produce a successful version receipt here.

**Compilation is currently unavailable in this managed runtime.** The extracted official `bin/lean --version` exits 1 with `error: failed to locate application`, under both the ordinary environment and a sanitized environment. Supplying the runtime's `LEAN_SYSROOT` did not resolve it. The cause beneath that startup failure is unresolved. A diagnostic trace was unavailable because the operating system denies ptrace. This is an environment limitation, not a Lean syntax result and not a property of a model's proposed language.

An independent synthetic declaration check also stops before compiler execution: the child setup rejects its requested process restrictions or privilege reduction (`Exception occurred in preexec_fn`). That observation does not identify which individual setup operation failed. The wrapper keeps that failure explicit and does not fall back to a less restricted execution path. No model-generated Lean source was executed during provisioning.

The initial archive extraction attempted to preserve the release builder's UID/GID and received unmapped-ownership errors. Re-extraction with `tar --no-same-owner` succeeded. Future bootstrap runs use that flag. This was an extraction failure, not a compiler or semantic result.

Unprivileged namespaces and chroot were already unavailable in this environment. A separate Landlock availability query returned `ENOSYS`. None of those unavailable mechanisms is claimed as active isolation. No escalation or privileged workaround is part of this workflow.

## Reproducible bootstrap

Run the bootstrap with a destination outside the repository:

```sh
python scripts/bootstrap_lean.py /absolute/scratch/path/lean-runtime
```

The script checks platform, download size and the pinned digest before extracting. It saves a receipt next to the compiler, including a failed version probe. The large compiler archive and runtime are reproducible dependencies and must not be committed. Installation alone is not evidence that checks can execute.

The inspected runtime for this session is at `/workspace/scratch/4043a04d6092/lean-runtime/lean-4.19.0-linux/bin/lean`. Scratch paths are session-specific; future runs should use their bootstrap receipt.

The small [runtime receipt](sources/lean-runtime-receipt.json) is preserved in this repository. It records the pinned archive and the failed executable version probe without including the runtime archive.

## Narrow execution policy

`scripts/check_lean_declarations.py` is an optional, deliberately restricted compatibility check. Before using it, review the actual frozen source and record the reviewer's identity and reason. The script separately parses every line before any compiler subprocess can begin. It accepts only ASCII `structure` and `inductive` declarations, fields and constructors, and named type applications, parentheses and arrows. Type names must be a fixed primitive or a declaration in that same specimen. The bounded subset excludes imports, definitions, proofs, tactics, executable commands, metaprogramming, deriving handlers, attributes, comments, strings and external names. Unsupported source is preserved and marked `NOT_EXECUTED_OUTSIDE_SAFE_SUBSET`; it is not rewritten to fit the guard.

For admitted text, the wrapper uses a fresh directory, an environment without inherited API credentials, bounded CPU time, address space, output file sizes, open files and processes, and a wall-clock deadline. When launched as root it also requests an unprivileged UID/GID and empty supplementary groups. Setup failure leaves an operational receipt instead of executing without those requested restrictions. Invoke this script as its own CLI process: its `preexec_fn` is not intended to be imported into a multithreaded experiment worker.

These measures are **not a full operating-system sandbox**. They do not authorize arbitrary generated Lean execution. The restricted parser prevents executable Lean syntax from entering this route; the compiler and its bundled default imports are trusted runtime dependencies. A broader proposed language or a conjecture requiring theorem elaboration needs a separately reviewed execution environment. It can still be studied as text now.

```sh
python scripts/check_lean_declarations.py frozen-specimen.lean \
  --lean /absolute/scratch/path/lean-runtime/lean-4.19.0-linux/bin/lean \
  --reviewed-by 'operator identity' \
  --review-note 'review of these exact declaration bytes' \
  --receipt new-compatibility-receipt.json
```

Receipts use exclusive creation and include the source hash. `COMPILED`, `COMPILER_REJECTED`, `CHECK_TIMEOUT`, `CHECK_OPERATIONAL_FAILURE`, `NOT_EXECUTED_COMPILER_UNAVAILABLE` and `NOT_EXECUTED_OUTSIDE_SAFE_SUBSET` remain distinct. A CLI process ending normally means a receipt was written; consult its status before making a compatibility claim.

## Verification and lessons

`python scripts/test_lean_guard.py` passed three offline tests, including sixteen attempted external or executable syntax forms that were refused before subprocess launch. The tests cover the boundary that matters: arbitrary code must not be silently admitted. They are not evidence that all model-proposed Lean languages fall inside the subset.

The [guard-test receipt](sources/lean-guard-test-receipt.json) preserves the command, exit status, test output and script hashes for this verification.

The transferable operational lesson is to separate download, extraction, executable startup, process containment, syntactic admission and compilation. Each can fail independently. The experimental lesson is to keep a compiler-unavailable flag independent from expression and criticism evidence, so a missing tool cannot silently privilege prose or formal syntax in the comparison.
