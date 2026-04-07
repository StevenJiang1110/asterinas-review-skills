---
name: review-asterinas-ipc
description: Review Asterinas IPC and System V semaphore implementation patches. Use for non-test changes under `kernel/src/ipc/`, `semget`/`semctl`/`semop` syscall paths, IPC namespaces, and related nsfs or setns exposure.
---

# Review Asterinas IPC

Review IPC patches with emphasis on Linux semantic fidelity for System V IPC, IPC namespaces, semaphore key and ID handling, synchronization, and namespace-scoped cleanup.

## Workflow

1. Read the local `AGENTS.md` instructions first.
2. Inspect the patch and nearby IPC paths before drawing conclusions.
3. Trace key allocation, lookup, removal, drop, and wait paths end to end.
4. Count private-helper call sites before keeping an abstraction.
5. Re-read comments, lock-order docs, and test names after refactors.
6. Run the narrowest useful validation, or state the gap explicitly.

## Review priorities

### Correctness and Linux semantics

Check key-versus-ID semantics, permission checks, namespace scoping, cleanup behavior, and blocking semantics before style issues.

For namespace work, explicitly check Linux implied-flag semantics. In particular, `unshare(CLONE_NEWIPC)` should imply `CLONE_SYSVSEM`, just as `CLONE_NEWNS` implies `CLONE_FS`.

### Abstraction boundaries

Do not expose namespace-internal lock guards, map types, or raw collections in public APIs when the namespace object can provide a higher-level operation instead.

### Single-use private helpers

Flag a private helper when it is called only once and does not enforce an invariant, hide tricky synchronization, or materially improve readability.

### Comments and docs

When reviewing lock-order comments, distinguish true nested lock ordering from mere temporal sequencing. Do not accept docs that claim an order between locks that are not held concurrently.

### Asterinas-specific checks

Always verify:
- no `unsafe` appears under `kernel/`
- visibility stays as narrow as possible
- no `.unwrap()` is introduced on fallible paths
- locking assumptions remain clear
- semaphore key allocation and freeing paths are race-free and documented at the right abstraction level
- regression tests prove an observable postcondition instead of only claiming cleanup or isolation in comments or names

## Output rules

Report issues in this order:
1. correctness bugs
2. semantic or Linux-compatibility mismatches
3. misleading naming
4. unnecessary abstraction or single-use helpers
5. stale comments or docs
6. missing validation
