# Publish a completed configuration test

The authorised destination is `AHepi/miniReason`, branch `main`. One publisher owns publication, even when up to five tests run concurrently. Do not mutate `AHepi/h-EPI`.

Inspect the staged diff and its explicit path list. Include the plan/template, all requests and public responses, Mini event logs and blobs, task evaluation, interpretation, new errata, relevant lessons and STATUS changes. Keep native hidden reasoning, credentials, environments, unrelated files and generated package caches out of the commit. Never edit a content-addressed reply to remove trailing whitespace; retain its bytes and document that immutable-data exception to whitespace checks.

Use the existing Git author identity. Commit with a message naming the configuration test and its purpose, then push normally to `main` without force or history rewriting. Verify that remote `refs/heads/main` equals the published commit. If Git authentication is unavailable, the independently authenticated GitHub connector may publish the same reviewed blobs/tree with a non-force ref update; verify its resulting tree and commit.

A push failure blocks new successor tests. Record the failure locally and recover publication without modifying completed evidence. Never report a local commit as published.
