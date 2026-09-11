# DeepSeek experiment transport

The authorised model is DeepSeek V4.1 Flash. On 2026-09-11 the authenticated `/v1/models` response listed `deepseek-flash` and `deepseek-v4-pro`. The experiment uses `deepseek-flash` only. The provider's documentation identifies it as V4.1 Flash; the returned model name and fingerprint, when supplied, are recorded on each call. A mutable alias cannot establish an immutable weight identity.

| Arm control | Actual request |
|---|---|
| Thinking disabled | `thinking: {type: disabled}` |
| Native reasoning | `thinking: {type: enabled}`, `reasoning_effort: high` unless a plan states otherwise |
| Completion ceiling | Explicit `max_tokens`; token usage recorded separately |
| Output contract | JSON object, with the same public task contract across comparable arms |
| Sampling | Provider defaults; no claimed deterministic seed |
| Credentials | `DEEPSEEK_API_KEY`, Authorization header only |

The provider says temperature is ignored in thinking mode; top-p also has different effective constraints across modes. Consequently switching thinking compares the provider's modes as delivered, rather than changing only an isolated internal reasoning operation. Equal maximum completion allowances do not make actual prompt tokens, reasoning tokens, latency or compute equal. Native reasoning tokens count toward reported completion usage and ceilings.

Every request is stored before sending. The record retains the final answer content, request settings, usage, finish reason, timestamps and provider identifiers. Native reasoning text is discarded before persistence. Truncation, empty output, missing usage, unexpected thinking behavior, credential echoes and transport failures are loud operational failures. An emergency timeout is not a semantic refutation. No automatic retry is hidden from the record.

Sources checked 2026-09-11: [API quick start](https://api-docs.deepseek.com/), [models](https://api-docs.deepseek.com/quick_start/pricing/), [thinking controls](https://api-docs.deepseek.com/guides/thinking_mode/), [chat completions](https://api-docs.deepseek.com/api/create-chat-completion/).
