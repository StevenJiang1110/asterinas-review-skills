---
name: review-asterinas
description: Top-level review workflow for Asterinas patches. Use for mixed-scope or unclear-scope reviews when a branch touches multiple subsystems or mixes implementation and test changes, then apply the relevant general, process, IPC, namespace, security, and test review lenses based on the changed files.
---

# Review Asterinas

Use this as the fallback review skill when the patch scope is broad or unclear.

## Workflow

1. Read the local `AGENTS.md` instructions first.
2. Inspect the changed files before judging the design.
3. Classify the patch:
- `test/`, especially `test/initramfs/`: apply the test review lens. This is a peer to the subsystem review lenses, not a fallback.
- `kernel/src/process/`, sessions, process groups, terminals, signals, waits, or other non-namespace lifecycle logic: apply the process review lens.
- `kernel/src/ipc/`, `semget`/`semctl`/`semop`, or other System V IPC and semaphore state-management code: apply the IPC review lens.
- `clone`/`unshare`/`setns`, namespace objects, nsfs exposure, namespace lifetime, or namespace-specific visibility rules: apply the namespace review lens.
- credentials, capabilities, permission checks, trust-boundary validation, or other security-sensitive behavior: apply the security review lens.
- Other kernel and `ostd/` implementation changes: apply the general review lens.
4. For mixed patches, combine the relevant specialist lenses and report findings in one review.
5. Present findings first, ordered by severity, with file and line references.

## Baseline checks

Always verify:
- Linux-visible behavior still matches expectations.
- names describe semantics rather than mechanisms.
- private helpers earn their existence.
- comments and doc comments still match behavior.
- no `unsafe` appears under `kernel/`.
- visibility stays as narrow as possible.
- no `.unwrap()` is introduced on fallible paths.
- validation is as narrow and concrete as the environment allows.
