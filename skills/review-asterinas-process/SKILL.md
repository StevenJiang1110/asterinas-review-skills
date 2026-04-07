---
name: review-asterinas-process
description: Review Asterinas process, namespace, and job-control implementation patches. Use for non-test changes under `kernel/src/process/`, `setns`/`unshare`/`clone` paths, process-group or session logic, terminal control, signals, wait paths, and other process-lifecycle code.
---

# Review Asterinas Process

Review process-related patches with emphasis on Linux semantic fidelity for clone, unshare, setns, process lifecycle, sessions, process groups, terminals, signals, and waits.

## Workflow

1. Read the local `AGENTS.md` instructions first.
2. Inspect the patch and trace the full lifecycle path, not just the edited function.
3. Check flag interactions and implied semantics in clone/unshare/setns paths.
4. Re-read comments and names after refactors; bootstrap-only paths must be named as such.
5. Run the narrowest useful validation, or state the gap explicitly.
6. If the patch also touches process tests under `test/`, apply the peer `review-asterinas-test` lens too: keep `run_test.sh` entries alphabetized within their local block, split distinct claims into focused `FN_TEST`s, keep core assertions in `FN_TEST`, and keep helper success paths on `CHECK`/`CHECK_WITH`.

## Review priorities

### Correctness and Linux semantics

Check process, session, process-group, terminal, signal, and namespace behavior first.

For namespace work, explicitly check Linux implied-flag semantics and entry restrictions. Be suspicious when `clone`, `unshare`, or `setns` paths omit required implication rules or shared-state checks.

### Naming

Prefer names that expose semantic role, especially for bootstrap and compatibility-only paths.

Prefer:
- `new_bootstrap`
- `new_empty`
- `set_control_terminal`

### Single-use private helpers

Keep a private helper only when it enforces an invariant, hides tricky ordering, or is genuinely reused.

### Comments and docs

Comments should explain why a special case exists, especially when Asterinas intentionally diverges from Linux or preserves a bootstrap invariant.

### Asterinas-specific checks

Always verify:
- no `unsafe` appears under `kernel/`
- visibility stays as narrow as possible
- no `.unwrap()` is introduced on fallible paths
- process, session, and process-group relationships stay explicit
- namespace-switching restrictions match Linux expectations
- tests cover observable behavior rather than only internal intent

## Output rules

Report issues in this order:
1. correctness bugs
2. semantic or Linux-compatibility mismatches
3. misleading naming
4. unnecessary abstraction or single-use helpers
5. stale comments or docs
6. missing validation
