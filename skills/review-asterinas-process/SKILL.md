---
name: review-asterinas-process
description: Review Asterinas process and job-control implementation patches. Use for non-test changes under `kernel/src/process/` that primarily affect process lifecycle, fork or exit behavior, process-group or session logic, terminal control, signals, wait paths, and other non-namespace process semantics.
---

# Review Asterinas Process

Review process-related patches with emphasis on Linux semantic fidelity for process lifecycle, fork and exit behavior, sessions, process groups, terminals, signals, and waits.

## Workflow

1. Read the local `AGENTS.md` instructions first.
2. Inspect the patch and trace the full lifecycle path, not just the edited function.
3. Check fork, exit, wait, signal, and job-control interactions across the full path.
4. Re-read comments and names after refactors; bootstrap-only paths must be named as such.
5. Run the narrowest useful validation, or state the gap explicitly.
6. If the patch also touches namespace mechanics, apply the peer `review-asterinas-namespace` lens too. If it also touches process tests under `test/`, apply the peer `review-asterinas-test` lens too.

## Review priorities

### Correctness and Linux semantics

Check process, session, process-group, terminal, signal, wait, fork, and exit behavior first.

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
- job-control and wait-related transitions match Linux expectations
- tests cover observable behavior rather than only internal intent

## Output rules

Report issues in this order:
1. correctness bugs
2. semantic or Linux-compatibility mismatches
3. misleading naming
4. unnecessary abstraction or single-use helpers
5. stale comments or docs
6. missing validation
