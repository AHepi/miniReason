## Orchestration rule (session-wide, user-mandated)

- The top-level Claude Code session is an **orchestrator only**: it assigns work to subagents, interprets their results, and decides what to do next. It does no repository work itself beyond that.
- **Every subagent and every Workflow `agent()` call MUST use Opus 5** (`model: "opus"`). Never spawn Fable 5.1 (or any non-Opus) subagents. Set the model explicitly on every spawn; do not rely on inheritance.
- API keys supplied by the user (Ollama, DeepSeek) are secrets: read them from environment variables or a gitignored local file only. Never write them into a tracked file, a commit, a log, or a report.
