# Why miniReason exists

This project tests whether deliberately configured Mini machinery changes what a language model can construct, criticise and repair. The required comparison is a bare model, candidate Mini configurations, and the same model's native reasoning. Mini must be allowed to lose. A run that fails to execute cannot decide whether its proposed reasoning method is useful.

The semantic guide is the supplied Explanatory Construction Semantics 2.0. The supplied Conjecture–Criticism Harness v1.3 guides mechanism design. Neither source is silently replaced by Mini's implementation. Mini uses kind records and does not implement all v1.3 epistemic graph semantics; these are explicit differences to analyse, not claims of conformance.

Configurations are arguments about a failure mechanism. Before trying one, explain what it makes visible, what it changes, what it preserves, and which comparison could defeat its rationale. After a failure, inspect the actual prompts, wiring, outputs and checker before revising. Do not randomly mutate configurations, run an evolutionary search, invent a scalar progress target, or call an arbitrary budget cutoff exhaustion.

Record every experiment, including operational failure. Keep causes in [the errata](docs/errata/README.md), and transferable learning in separate [lesson files](docs/lessons/README.md). Publish each completed configuration test to `main` immediately before beginning a successor test. Up to five configurations may run concurrently, with publication serialised. A publication failure blocks successor tests until the record is durable.

Finite observations can defeat scoped behavioural claims. They do not establish creativity across all tasks, establish the model's pretraining repertoire, or refute ECS merely because an implementation failed. Any claimed semantic counterexample needs an independently defended interpretation and a fixed system boundary.

Start or resume at [README](README.md), then [the continuation workflow](docs/workflows/continue.md). A future operator should be able to recover the question, evidence and open alternatives without a chat transcript.
