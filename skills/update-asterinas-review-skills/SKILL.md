---
name: update-asterinas-review-skills
description: Update the local Asterinas review skills under `~/.codex/skills/review-asterinas*` based on user review feedback. Use when the user asks to refine the review taxonomy, move guidance between skills, add a new review lens, split mixed responsibilities, or align `SKILL.md` and `agents/openai.yaml`. New skills must be added as clearly separated categories, not mixed into an unrelated skill.
---

# Update Asterinas Review Skills

Use this skill to turn review feedback about the Asterinas review-skill set into concrete edits under `~/.codex/skills/`.

## Goals

- Keep each review skill focused on one review lens.
- Treat `test`, `process`, `ipc`, `namespace`, `security`, and `general` as peer categories rather than dumping related advice into one place.
- When feedback introduces a reusable new lens, create a new sibling skill instead of widening an unrelated one.

## Workflow

1. Read the user's feedback and split it into atomic guidance items.
2. Classify each item before editing:
   - taxonomy change
   - scope tightening
   - scope expansion within an existing lens
   - new lens required
   - metadata sync
3. Map each item to one primary target skill first.
4. If one feedback item spans multiple concerns, split the content by concern and move each part into the proper skill. Do not preserve mixed ownership just because the original feedback was mixed.
5. When the feedback defines a reusable new category, create a new sibling `review-asterinas-<topic>` skill with its own `SKILL.md` and `agents/openai.yaml`.
6. When taxonomy changes, update the top-level router in `~/.codex/skills/review-asterinas/SKILL.md`.
7. Keep every touched `agents/openai.yaml` aligned with the actual scope of its `SKILL.md`.
8. Sanity-check overlaps after editing. Descriptions, examples, and trigger conditions should be separated enough that each skill has a clear job.

## Classification Rules

### Keep by review lens, not by example

- Put test-structure, assertion, cleanup, isolation, and validation guidance in `review-asterinas-test`.
- Put namespace semantics, `clone`/`unshare`/`setns`, nsfs exposure, and namespace lifetime rules in `review-asterinas-namespace`.
- Put credentials, capabilities, authorization, trust-boundary checks, and object-exposure rules in `review-asterinas-security`.
- Put System V IPC and semaphore semantics in `review-asterinas-ipc`.
- Put process lifecycle, job control, sessions, process groups, signals, terminals, and wait semantics in `review-asterinas-process`.
- Keep `review-asterinas-general` as the fallback for other kernel or OSTD implementation review guidance.

### Create a new skill when

- the feedback defines a reusable review lens with its own trigger conditions
- the content would make an existing skill mixed-scope
- the lens is likely to recur across multiple reviews

### Do not mix

- test mechanics with subsystem semantics
- namespace semantics with general process guidance
- security policy with unrelated abstraction or naming advice
- reusable category-specific rules into one-off examples inside another skill

## Editing Rules

- Prefer moving or deleting misplaced guidance over layering disclaimers on top of it.
- Keep frontmatter `description` explicit about when the skill should be used.
- Keep `SKILL.md` focused on workflow, scope, priorities, and output rules.
- Avoid embedding narrow patch-specific examples unless they define a reusable trigger pattern.
- Add new categories as sibling skills under `~/.codex/skills/`; do not stack unrelated categories into one large skill.

## Minimum Deliverables

For each update, do all applicable items:

- patch the target `SKILL.md`
- patch or create the matching `agents/openai.yaml`
- patch `review-asterinas/SKILL.md` if routing changed
- summarize what was split, moved, added, or removed

## Example Requests

- “请根据我的这些 review 意见来更新 review asterinas skills”
- “把 namespace 相关内容从 test skill 拆出去，单独建 skill”
- “review-asterinas-process 太宽了，帮我重新分类”
- “这些 review 经验已经成体系了，帮我拆成几个独立 skill，不要混在一起”
