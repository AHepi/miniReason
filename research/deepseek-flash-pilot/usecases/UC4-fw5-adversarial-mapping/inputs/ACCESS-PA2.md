# Participant access under P-A2

This file prospectively supersedes `ACCESS.md` for the staged P-A2 task. The old file remains an unchanged record of the pre-P-A2 pilot, which had no source-read tool.

The host resolves only task-pinned content-addressed units. `read_source` accepts a pinned unit ID and an exact byte range subject to its per-read limit. It never treats a repository path as authority and cannot list directories, search the checkout, follow an unpinned reference, or open environment files. Every resolved read receives a `source_reads` custody receipt containing the unit SHA256, requested range, returned range, byte count, and any omission.

For UC4, the only semantic source material remains the pinned FW5 excerpts and the pinned offline episode projection. `SOURCE-MANIFEST.json` and this access record provide custody/context; they do not add unread FW5 text or episode events. The full FW5 edition path identifies provenance only. The original episode directory is not participant material. Reader briefs, custody supplements, any derived-properties memorandum, `.env`, arbitrary paths, and repository search remain unavailable. Never infer unread portions.
