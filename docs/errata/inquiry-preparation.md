# Inquiry preparation errata

These findings concern prototype preparation and integration. No live model call produced them, and none is a semantic failure of C0, WHL, RSS or a criticism.

## INQ-PREP-001 — Queued occurrence identity covered only part of its record

The first prototype signed occurrence fields before merging route metadata into the queued artifact. A later plan could not verify the whole queued object unchanged. Preparation was repaired by signing the complete output occurrence after metadata was included. The queue round-trip test selects that exact object into a successor plan through both direct and Mini routes. No question extraction, endorsement or automatic activation was introduced.

## INQ-PREP-002 — Child route could overwrite enclosing record roles

A flat dictionary update from the Mini adapter could replace the enclosing arm schema and unresolved-state vocabulary. Preparation now preserves the host schema and neutral standing fields, recording the child schema separately as `route_schema`. The original public content remains unchanged. Exposure metadata is not converted into semantic dependence, `about` or `answers` edges.

## INQ-PREP-003 — Signed metadata could disagree with its retained text or activation

Integration review found that recomputing an outer identity could leave an incorrect inner text hash or a wrong issue activation binding undetected. Both would make the record's attributed material differ from what the runner actually used. Occurrence validation now recomputes the UTF-8 text hash; activation preflight checks selected occurrence, successor identity, allocation reason and unresolved standing. Targeted tests verify refusal before provider calls.

## INQ-PREP-004 — Provider settings and resource absence were incompletely checked

The prototype did not reject a provider factory that changed settings other than the completion cap, and it silently defaulted missing resource counters to zero. Integration now checks the complete Settings value, validates public response usage and completion ceilings equally on direct and Mini routes, and records missing or malformed counters as unavailable with an operational alarm. Known reported token totals are distinguished from unknown possible billed cost after failed delivery. Fourteen targeted inquiry tests passed after these changes; the complete regression receipt is under docs/sources/inquiry-integration-check.json.
