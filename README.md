# miniReason

**Purpose: test whether deliberately configured Mini helps a model construct and repair explanations and technical solutions, against bare-model and native-reasoning comparisons.** Read [PURPOSE.md](PURPOSE.md) before changing the experiment. The experiment must permit Mini to lose and must distinguish broken machinery from a failed candidate idea.

Mini is extracted from [AHepi/h-EPI, claude/mini-experiments](https://github.com/AHepi/h-EPI/tree/b2a33283dc1e05fb83c3357b26e2cc12115f6b6c/src/creib/forge/mini). This project creates its own experimental templates from the supplied ECS 2.0 and harness v1.3 guides. Existing upstream experimental templates and findings are not presented as new work.

The experiment model is DeepSeek V4.1 Flash, using the official `deepseek-flash` identifier. The same model is called with explicit thinking disabled or enabled. See [provider settings](docs/PROVIDER.md) for what those comparisons control and leave uncontrolled.

## Start here

[Current state](docs/STATUS.md) records what ran and what remains open. [The workflow index](docs/workflows/README.md) tells a future operator where to read and write. [The semantic guide](docs/SEMANTIC_GUIDE.md) separates task behavior from claims about creativity. [The experiment method](docs/EXPERIMENT_METHOD.md) states the comparisons and their limits.

| Location | Use |
|---|---|
| `src/creib/forge/mini/` | Extracted Mini engine; existing import namespace retained for provenance |
| `src/minireason/` | Original templates, task interpreters, DeepSeek adapter and experiment driver |
| `experiments/plans/` | Frozen questions and methods, written before their runs |
| `experiments/templates/` | Generated original configurations with their rationale |
| `experiments/records/` | Complete run evidence, including unsuccessful and interrupted work |
| `docs/errata/` | Failures, evidence, causes and corrections |
| `docs/lessons/` | Separate lessons about configuration, method, semantics and operations |
| `docs/workflows/` | Hooks for continuing, testing, diagnosis, publication and review |
| `tests/` | Offline checks for engine integrity and experiment machinery |

## Local setup

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
```

Live calls read `DEEPSEEK_API_KEY` from the process environment. Keep it out of files that are committed. Calls, content, usage and failures are recorded; native hidden reasoning text is discarded. Live commands and the current experiment state are documented in [the continuation workflow](docs/workflows/continue.md).

After every configuration test, preserve the result and its causes, then commit and push to `main` immediately. Do not wait for a successful outcome before publishing. Every finite stopping point must explain the remaining alternatives; reaching a resource ceiling does not mean the search space is exhausted.
