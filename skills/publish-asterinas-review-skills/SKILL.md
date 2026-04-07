---
name: publish-asterinas-review-skills
description: Sync local Asterinas review skills into the shared GitHub repository, commit the changes, and push them. Use when the user wants to publish updated review skills from `~/.codex/skills/`.
---

# Publish Asterinas Review Skills

Use this skill to publish the local Asterinas review skills to the shared repository.

## Tracked skills

By default, sync these skill directories from `~/.codex/skills/`:

- `review-asterinas`
- `review-asterinas-general`
- `review-asterinas-ipc`
- `review-asterinas-process`
- `review-asterinas-test`
- `publish-asterinas-review-skills`

## Workflow

1. Treat the local `~/.codex/skills/` copies as the source of truth.
2. Use the bundled script instead of manually copying files:

```bash
python3 scripts/publish_review_skills.py \
  --repo-dir ~/asterinas-review-skills \
  --remote git@github.com:StevenJiang1110/asterinas-review-skills.git \
  --commit-message "Update Asterinas review skills"
```

3. The script clones the repo when `~/asterinas-review-skills` does not exist yet.
4. The script syncs the tracked skills into `<repo>/skills/`, stages the changes, commits them, and pushes them unless `--no-push` is set.
5. After the script completes, report the changed skills, the commit hash, and whether the push succeeded.

## Options

- Use `--skill <name>` repeatedly to publish only a subset.
- Use `--dry-run` to preview what would change.
- Use `--no-push` to stop after the local commit.
- Use `--allow-dirty-repo` only when you intentionally want to reuse a repo checkout that already has local changes.

## Guardrails

- Fail if a tracked source skill directory is missing.
- Fail if the repo checkout is dirty unless `--allow-dirty-repo` is set.
- Keep the repository layout stable under `skills/<skill-name>/`.
- Do not edit unrelated files in the repo while publishing.
