---
name: review-asterinas-security
description: Review security-sensitive Asterinas implementation patches. Use for non-test changes involving credentials, capabilities, permission checks, user-kernel boundary validation, cross-namespace or cross-process authorization, or exposure of kernel objects or state to user space.
---

# Review Asterinas Security

Review security-sensitive patches with emphasis on authorization, privilege transitions, boundary validation, object exposure, and user-visible failure modes.

## Workflow

1. Read the local `AGENTS.md` instructions first.
2. Inspect the patch and trace who can reach the changed path, with what authority.
3. Identify every trust boundary and the checks that must happen there.
4. Trace handle, reference, and state lifetimes across permission checks to catch confused-deputy and TOCTOU risks.
5. Re-read comments and names after refactors; security exceptions and bypasses must stay explicit.
6. Run the narrowest useful validation, or state the gap explicitly.
7. If the patch also changes subsystem-specific semantics or tests, apply the peer `review-asterinas-process`, `review-asterinas-ipc`, `review-asterinas-namespace`, or `review-asterinas-test` lens too.

## Review priorities

### Authorization and privilege transitions

Check capability tests, ownership rules, privilege drops or elevations, and denial paths before style issues.

### Boundary validation

Validate user-controlled inputs and handles at the boundary that introduces risk; trust already-validated internal state afterward.

### Object exposure and information leaks

Check proc, nsfs, syscall, or other user-visible exposure paths for unintended handles, state disclosure, or privilege confusion.

### Lifetime and TOCTOU

Check that lookups and references remain valid across permission checks and concurrent state changes.

### Comments and docs

Comments should explain why a security restriction exists, not just restate the check.

### Asterinas-specific checks

Always verify:
- no `unsafe` appears under `kernel/`
- visibility stays as narrow as possible
- no `.unwrap()` is introduced on fallible security paths
- checks happen at the boundary that introduces the security risk
- failures are observable as Linux-visible denial behavior
- regression tests cover both allowed and denied outcomes when practical

## Output rules

Report issues in this order:
1. correctness bugs
2. semantic or Linux-compatibility mismatches
3. authorization or validation gaps
4. misleading naming
5. stale comments or docs
6. missing validation
