---
name: review-asterinas-test
description: Review Asterinas test patches. Use for changes under `test/`, especially C tests under `test/initramfs/`, even when the functionality under test belongs to process, IPC, or another subsystem. This skill is a peer to the subsystem review skills and should trigger on test-file changes.
---

# Review Asterinas Test

Review Asterinas test changes with emphasis on correctness, test isolation, maintainability, and repository-specific style. This skill is for test files and is a peer to the subsystem review skills.

## Priorities

Check these in order:

1. The test asserts real behavior rather than an outdated assumption.
2. The scenario is the right one for the semantic claim being tested.
3. Setup and cleanup do not leak mounts, files, or namespaces across tests.
4. The test proves an observable postcondition rather than only claiming cleanup or isolation in its name or comments.
5. Test code stays simple and readable.
6. Validation uses the narrowest useful build and execution commands.

## What To Flag

- A test claims Linux or Asterinas should return a specific errno, but the scenario does not actually exercise that semantic.
- A weaker scenario is used where a stronger one is needed.
  For example: self-bind of `/proc/self/ns/mnt` when the real claim is about importing an older mount namespace into a newer one.
- A test name or comment claims cleanup or isolation, but the assertions only prove that some other state was unaffected.
- Cleanup depends on later assertions succeeding.
- A test leaves behind mounts, temp files, or namespace state after failure.
- Child-process setup uses ad hoc branching or custom exit-code ladders where `CHECK` or `CHECK_WITH` would do.
- Different semantic claims are packed into one `FN_TEST` instead of being split into focused tests.
- Helper functions contain most of the test logic or assertions, forcing the main `FN_TEST` flow to lose `TEST_*` coverage.
- Helper functions manually inspect success-path return values instead of using `CHECK` or `CHECK_WITH`.
- Syscalls or libc calls in setup/cleanup are left bare instead of being wrapped in the test macros.
- New entries in `run_test.sh` are not kept in alphabetical order within their local block.
- Comments are longer than the code warrants or repeat obvious behavior.

## Preferred Patterns

### Assertions

- Use `TEST_SUCC`, `TEST_ERRNO`, or `TEST_RES` in the main test flow.
- Keep the semantic claim and most assertions in `FN_TEST` so failures are reported by the test framework at the call site.
- In child-process setup or teardown, prefer `CHECK` and `CHECK_WITH`.
- In helper functions, use `CHECK` or `CHECK_WITH` for expected-success operations; leave expected-failure assertions in `FN_TEST` or the immediate child branch.
- Wrap all relevant calls, including `getpid`, `mkdir`, `mount`, `umount`, `close`, `waitpid`, `snprintf`, and `rmdir`, unless there is a strong reason not to.

### Isolation

- Prefer a child process when the test uses `unshare`, destructive mount operations, or fatal `CHECK`-style setup.
- Keep the parent-side assertion simple: usually `waitpid` plus exit-status validation.
- Use unique per-process temp paths when mount state or files may collide across reruns.

### Control Flow

- Prefer one semantic claim per `FN_TEST`; split reads, invalid-input cases, permission checks, and isolation checks when they can fail independently.
- Prefer straight-line setup with `CHECK` over custom `if (...) _exit(n)` trees.
- Keep helpers low-level and mechanical; avoid hiding the core test story behind wrapper functions.
- Keep failure handling minimal.
- If cleanup is required after an expected failure, keep it short and deterministic.

### Comments

- Keep comments short and specific.
- Say what semantic is being tested, not every mechanical step.
- Match the surrounding file style; avoid turning one test into a mini design doc.

## Validation

After changing a test, validate with the narrowest commands first:

```bash
make initramfs ENABLE_BASIC_TEST=true
/root/asterinas/test/initramfs/build/initramfs/test/security/namespace/proc_nsfs
```

If the edited file lives elsewhere, run the closest corresponding binary instead of a broader suite.

When a test fails unexpectedly:

- Reproduce the exact command outside the test if possible.
- Determine whether the expectation is wrong or the implementation is wrong before changing assertions.
- If behavior is claimed to match Linux, verify that the tested scenario really maps to the Linux semantic being cited.

## Output Style

When reviewing, report findings first with file references and concrete reasons.

When editing, prefer small rewrites that:

- remove fragile assumptions,
- reduce custom branching,
- improve cleanup,
- and preserve or improve isolation.
