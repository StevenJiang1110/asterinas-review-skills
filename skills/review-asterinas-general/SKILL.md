---
name: review-asterinas-general
description: Review non-test Asterinas kernel or OSTD implementation patches outside the process and IPC subsystems. Use for changes under `kernel/` or `ostd/` that do not primarily touch `kernel/src/process/`, namespace switching, `kernel/src/ipc/`, or test-only files under `test/`.
---

# Review Asterinas General

Review the patch before judging the design. Prioritize correctness, Linux-visible behavior, naming, abstraction quality, comments, and validation.

## Workflow

1. Read the local `AGENTS.md` instructions first.
2. Inspect the patch and nearby code before drawing conclusions.
3. Trace every new helper, rename, and special-case branch with `rg`.
4. Count private-helper call sites before deciding whether the helper should exist.
5. Re-read comments and doc comments after refactors to ensure they still match behavior.
6. Run the narrowest useful validation. If blocked, say so explicitly.

## Review priorities

### Correctness and Linux semantics

Check whether the patch preserves Linux-visible behavior and internal invariants before style issues.

### Naming

Prefer names that expose semantic role rather than mechanism.

### Single-use private helpers

Flag a private helper when it is called only once and does not enforce an invariant, hide tricky synchronization, or materially improve readability.

### Comments and docs

Flag comments that restate code, hide special cases behind generic wording, or become stale after a rename or refactor.

### Asterinas-specific checks

Always verify:
- no `unsafe` appears under `kernel/`
- visibility stays as narrow as possible
- no `.unwrap()` is introduced on fallible paths
- locking assumptions remain clear
- regression tests cover an observable postcondition

## Output rules

Report issues in this order:
1. correctness bugs
2. semantic or Linux-compatibility mismatches
3. misleading naming
4. unnecessary abstraction or single-use helpers
5. stale comments or docs
6. missing validation
