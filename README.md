# Asterinas Review Skills

Shareable Codex skills for reviewing Asterinas patches.

## Included skills

- `review-asterinas`
- `review-asterinas-general`
- `review-asterinas-ipc`
- `review-asterinas-process`
- `review-asterinas-test`
- `publish-asterinas-review-skills`

## Repository layout

All installable skills live under `skills/<skill-name>/`.

## Install

Clone the repository and copy the skill directories into `~/.codex/skills/`:

```bash
git clone git@github.com:StevenJiang1110/asterinas-review-skills.git
mkdir -p ~/.codex/skills
cp -R asterinas-review-skills/skills/* ~/.codex/skills/
```

Restart Codex after installation.

## Update and publish

Edit the local skill copies under `~/.codex/skills/`, then publish them back to this repository with:

```bash
python3 ~/.codex/skills/publish-asterinas-review-skills/scripts/publish_review_skills.py \
  --repo-dir ~/asterinas-review-skills \
  --remote git@github.com:StevenJiang1110/asterinas-review-skills.git \
  --commit-message "Update Asterinas review skills"
```

You can also invoke the local `$publish-asterinas-review-skills` skill from Codex and let it run the same script for you.
