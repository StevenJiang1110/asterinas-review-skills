---
name: review-asterinas-namespace
description: Review Asterinas namespace implementation patches. Use for non-test changes involving `clone`/`unshare`/`setns`, namespace objects or nsfs exposure, namespace lifetime or import and export rules, and mount, IPC, PID, network, UTS, time, or user namespace semantics.
---

# Review Asterinas Namespace

Review namespace-related patches with emphasis on Linux semantic fidelity for namespace creation, switching, exposure, lifetime, and cross-namespace restrictions.

## Workflow

1. Read the local `AGENTS.md` instructions first.
2. Inspect the patch and trace the full namespace transition or exposure path, not just the edited function.
3. Check implied-flag semantics and entry restrictions in `clone`/`unshare`/`setns` paths.
4. Trace namespace object lookup, file-descriptor exposure, lifetime, and cleanup end to end.
5. Re-read comments and names after refactors; ownership, ancestry, and privilege-sensitive rules should stay explicit.
6. Run the narrowest useful validation, or state the gap explicitly.
7. If the patch also changes subsystem-specific semantics inside the namespace path, apply the peer `review-asterinas-process`, `review-asterinas-ipc`, `review-asterinas-security`, or `review-asterinas-test` lens too.

## Review priorities

### Correctness and Linux semantics

Check implied flags, ancestor and ownership rules, switching restrictions, and namespace-scoped visibility before style issues.

Be suspicious when a patch:
- treats namespace membership as only a refcount problem while ignoring permission or ancestry rules
- exposes nsfs or namespace file descriptors without rechecking Linux-visible access rules
- claims cleanup or isolation without an observable postcondition

### Lifetime and cleanup

Ensure namespace objects, references, and scoped resources are released at the right abstraction boundary.

### Abstraction boundaries

Do not expose raw guards, maps, or collections when the namespace object can provide a higher-level operation.

### Comments and docs

Comments should explain why a restriction exists and what Linux semantic it preserves.

### Asterinas-specific checks

Always verify:
- no `unsafe` appears under `kernel/`
- visibility stays as narrow as possible
- no `.unwrap()` is introduced on fallible paths
- implied-flag and entry restrictions match Linux expectations
- namespace lifetime and cleanup behavior are observable in tests

## Output rules

Report issues in this order:
1. correctness bugs
2. semantic or Linux-compatibility mismatches
3. misleading naming
4. unnecessary abstraction or single-use helpers
5. stale comments or docs
6. missing validation
