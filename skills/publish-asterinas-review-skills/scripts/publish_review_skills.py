#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path


DEFAULT_REMOTE = "git@github.com:StevenJiang1110/asterinas-review-skills.git"
DEFAULT_REPO_DIR = Path.home() / "asterinas-review-skills"
DEFAULT_SOURCE_ROOT = Path.home() / ".codex" / "skills"
DEFAULT_BRANCH = "main"
DEFAULT_SKILLS = (
    "review-asterinas",
    "review-asterinas-general",
    "review-asterinas-ipc",
    "review-asterinas-namespace",
    "review-asterinas-process",
    "review-asterinas-security",
    "review-asterinas-test",
    "update-asterinas-review-skills",
    "publish-asterinas-review-skills",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync local Asterinas review skills into the shared Git repo."
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=DEFAULT_SOURCE_ROOT,
        help="Source skills root. Defaults to ~/.codex/skills.",
    )
    parser.add_argument(
        "--repo-dir",
        type=Path,
        default=DEFAULT_REPO_DIR,
        help="Local checkout of the shared Git repo.",
    )
    parser.add_argument(
        "--remote",
        default=DEFAULT_REMOTE,
        help="Git remote used when the repo checkout must be cloned.",
    )
    parser.add_argument(
        "--branch",
        default=DEFAULT_BRANCH,
        help="Git branch to push. Defaults to main.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        dest="skills",
        help="Publish only the named skill. Repeat to publish multiple skills.",
    )
    parser.add_argument(
        "--commit-message",
        help="Commit message. Defaults to a timestamped sync message.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned sync without copying files or invoking Git.",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Commit locally but do not push.",
    )
    parser.add_argument(
        "--allow-dirty-repo",
        action="store_true",
        help="Allow publishing from a repo checkout that already has local changes.",
    )
    return parser.parse_args()


def run(
    args: list[str],
    *,
    cwd: Path | None = None,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=capture_output,
    )


def ensure_repo(repo_dir: Path, remote: str, dry_run: bool) -> None:
    if repo_dir.exists():
        return

    print(f"Cloning {remote} into {repo_dir}")
    if dry_run:
        return

    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", remote, str(repo_dir)])


def ensure_clean_repo(repo_dir: Path, allow_dirty_repo: bool, dry_run: bool) -> None:
    if dry_run or allow_dirty_repo:
        return

    status = run(
        ["git", "status", "--porcelain"],
        cwd=repo_dir,
        capture_output=True,
    ).stdout.strip()
    if status:
        raise SystemExit(
            "Repository has local changes. Commit or stash them first, "
            "or rerun with --allow-dirty-repo."
        )


def ensure_branch(repo_dir: Path, branch: str, dry_run: bool) -> None:
    if dry_run:
        print(f"Would ensure branch {branch}")
        return

    current_branch = run(
        ["git", "branch", "--show-current"],
        cwd=repo_dir,
        capture_output=True,
    ).stdout.strip()

    if current_branch == branch:
        return

    local_branch = subprocess.run(
        ["git", "rev-parse", "--verify", branch],
        cwd=repo_dir,
        check=False,
        text=True,
        capture_output=True,
    )
    if local_branch.returncode == 0:
        run(["git", "checkout", branch], cwd=repo_dir)
        return

    run(["git", "checkout", "-b", branch], cwd=repo_dir)


def validate_skills(source_root: Path, skills: list[str]) -> list[Path]:
    paths: list[Path] = []
    for skill in skills:
        skill_dir = source_root / skill
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            raise SystemExit(f"Missing source skill: {skill_file}")
        paths.append(skill_dir)
    return paths


def copy_skill(source_dir: Path, dest_dir: Path, dry_run: bool) -> None:
    print(f"Syncing {source_dir.name} -> {dest_dir}")
    if dry_run:
        return

    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.copytree(
        source_dir,
        dest_dir,
        ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"),
    )


def stage_changes(repo_dir: Path, skills: list[str], dry_run: bool) -> None:
    git_args = ["git", "add", "-A", "--"]
    git_args.extend(f"skills/{skill}" for skill in skills)
    print("Staging synced skills")
    if not dry_run:
        run(git_args, cwd=repo_dir)


def has_staged_changes(repo_dir: Path) -> bool:
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo_dir,
        text=True,
    )
    return result.returncode != 0


def commit_changes(repo_dir: Path, commit_message: str, dry_run: bool) -> str | None:
    if dry_run:
        print(f'Would commit with message: "{commit_message}"')
        return None

    if not has_staged_changes(repo_dir):
        print("No skill changes to commit.")
        return None

    run(["git", "commit", "-m", commit_message], cwd=repo_dir)
    commit_hash = run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_dir,
        capture_output=True,
    ).stdout.strip()
    print(f"Created commit {commit_hash}")
    return commit_hash


def push_changes(repo_dir: Path, branch: str, dry_run: bool) -> None:
    print(f"Pushing branch {branch}")
    if not dry_run:
        run(["git", "push", "-u", "origin", branch], cwd=repo_dir)


def default_commit_message() -> str:
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d")
    return f"Update Asterinas review skills ({timestamp})"


def main() -> int:
    args = parse_args()
    skills = args.skills or list(DEFAULT_SKILLS)
    commit_message = args.commit_message or default_commit_message()

    ensure_repo(args.repo_dir, args.remote, args.dry_run)
    ensure_clean_repo(args.repo_dir, args.allow_dirty_repo, args.dry_run)
    ensure_branch(args.repo_dir, args.branch, args.dry_run)

    source_dirs = validate_skills(args.source_root, skills)
    repo_skills_root = args.repo_dir / "skills"
    if args.dry_run:
        print(f"Would sync into {repo_skills_root}")
    else:
        repo_skills_root.mkdir(parents=True, exist_ok=True)

    for source_dir in source_dirs:
        copy_skill(source_dir, repo_skills_root / source_dir.name, args.dry_run)

    stage_changes(args.repo_dir, skills, args.dry_run)
    commit_hash = commit_changes(args.repo_dir, commit_message, args.dry_run)
    if commit_hash is None:
        return 0

    if args.no_push:
        print("Skipping push because --no-push was set.")
        return 0

    push_changes(args.repo_dir, args.branch, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
