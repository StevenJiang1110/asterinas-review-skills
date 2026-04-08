---
name: review-asterinas-test
description: Review Asterinas test patches. Use for changes under `test/`, especially `test/initramfs/`, regardless of the functionality under test. This skill is a peer to the subsystem review skills and should trigger on test-file changes.
---

# Review Asterinas Test

Review Asterinas test changes with emphasis on correctness, isolation, maintainability, and repository-specific style. This skill is for test code quality; pair it with a subsystem or security lens when the semantic claim itself is domain-specific.

## Priorities

Check these in order:

1. The test asserts real behavior rather than an outdated assumption.
2. The scenario actually exercises the semantic claim being tested.
3. Setup and cleanup do not leak state across tests.
4. The test proves an observable postcondition rather than only claiming one in its name or comments.
5. Test code stays simple and readable.
6. Validation uses the narrowest useful build and execution commands.

## What To Flag

- A test claims Linux or Asterinas should return a specific errno, but the scenario does not actually exercise that semantic.
- A weaker scenario is used where a stronger one is needed for the claim.
- A test name or comment claims cleanup or isolation, but the assertions only prove that some other state was unaffected.
- Cleanup depends on later assertions succeeding.
- A test leaves behind temp state after failure.
- Child-process setup uses ad hoc branching or custom exit-code ladders where `CHECK` or `CHECK_WITH` would do.
- Different semantic claims are packed into one `FN_TEST` instead of being split into focused tests.
- Helper functions contain most of the test logic or assertions, forcing the main `FN_TEST` flow to lose `TEST_*` coverage.
- Helper functions manually inspect success-path return values instead of using `CHECK` or `CHECK_WITH`.
- Helper functions parse fixed-format text in two stages when one direct parse would be clearer, such as matching a fixed `/proc` prefix first and then parsing the suffix separately.
- Setup or cleanup calls are left bare instead of being wrapped in the test macros without a good reason.
- New entries in `run_test.sh` are not kept in alphabetical order within their local block.
- Comments are longer than the code warrants or repeat obvious behavior.
- A temporary like `expected_*` is introduced only to hold a simple expression for the next assertion, making the assertion flow harder to read.
- State-changing calls and their immediate postcondition checks are split apart by avoidable temporaries or layout noise.
- Blank lines in child-process branches do not separate clear phases such as setup, mutation, verification, and exit.

## Preferred Patterns

### Assertions

- Use `TEST_SUCC`, `TEST_ERRNO`, or `TEST_RES` in the main test flow.
- Keep the semantic claim and most assertions in `FN_TEST` so failures are reported by the test framework at the call site.
- In child-process setup or teardown, prefer `CHECK` and `CHECK_WITH`.
- In helper functions, use `CHECK` or `CHECK_WITH` for expected-success operations; leave expected-failure assertions in `FN_TEST` or the immediate child branch.
- Wrap setup and cleanup calls in the test macros unless there is a strong reason not to.
- Keep a state-changing operation and the checks that prove its result adjacent when they form one verification step.
- Inline simple expected expressions in `CHECK_WITH` or `TEST_RES` instead of storing them in one-use `expected_*` temporaries.

### Isolation

- Prefer a child process when the test mutates shared state or uses fatal `CHECK`-style setup.
- Keep the parent-side assertion simple: usually child completion plus exit-status validation.
- Use unique temp paths when files or other shared state may collide across reruns.

### Control Flow

- Prefer one semantic claim per `FN_TEST`; split reads, invalid-input cases, permission checks, and isolation checks when they can fail independently.
- Prefer straight-line setup with `CHECK` over custom `if (...) _exit(n)` trees.
- Keep helpers low-level and mechanical; avoid hiding the core test story behind wrapper functions.
- When scanning fixed-format output in a helper, prefer one direct parse that both identifies and extracts the target field if the format is static.
- Keep failure handling minimal.
- If cleanup is required after an expected failure, keep it short and deterministic.
- In child branches, use blank lines to separate setup, mutation, verification, and termination, and leave `_exit(...)` in its own final block when it closes the branch.

### Comments

- Keep comments short and specific.
- Say what semantic is being tested, not every mechanical step.
- Match the surrounding file style; avoid turning one test into a mini design doc.

## Validation

After changing a test, validate with the narrowest commands first:

```bash
make initramfs ENABLE_BASIC_TEST=true
# then run the closest single test binary or smallest relevant suite
```

If the edited file builds to a dedicated binary, run that binary directly instead of a broader suite.

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
