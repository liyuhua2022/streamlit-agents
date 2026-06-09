#!/bin/bash
# .claude/hooks/check-git-before-coder.sh
#
# Runs when the coder subagent starts.
# Blocks the subagent if:
#   1. Not inside a git repository
#   2. Working tree has uncommitted changes
#   3. Current branch is main or master

set -euo pipefail

# ── 1. Must be inside a git repo ────────────────────────────────────────────
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "ERROR: Not inside a git repository. The coder subagent requires a git repo." >&2
  exit 2
fi

# ── 2. Working tree must be clean ────────────────────────────────────────────
UNCOMMITTED=$(git status --porcelain)
if [ -n "$UNCOMMITTED" ]; then
  echo "ERROR: Working tree has uncommitted changes. Clean up before starting." >&2
  echo "" >&2
  echo "Uncommitted files:" >&2
  git status --short >&2
  echo "" >&2
  echo "Options:" >&2
  echo "  git stash        — stash changes temporarily" >&2
  echo "  git add && git commit — commit changes first" >&2
  exit 2
fi

# ── 3. Must NOT be on main or master ─────────────────────────────────────────
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
  echo "ERROR: Currently on protected branch '$CURRENT_BRANCH'." >&2
  echo "" >&2
  echo "Create a feature branch before starting:" >&2
  echo "  feat/<description>     — new feature" >&2
  echo "  fix/<description>      — bug fix" >&2
  echo "  refactor/<description> — refactoring" >&2
  echo "  test/<description>     — tests only" >&2
  echo "  chore/<description>    — maintenance" >&2
  echo "  docs/<description>     — documentation" >&2
  echo "" >&2
  echo "Example: git checkout -b feat/user-authentication" >&2
  exit 2
fi

# ── 4. Validate branch name prefix ───────────────────────────────────────────
VALID_PREFIXES="^(feat|fix|refactor|test|chore|docs)/"
if ! echo "$CURRENT_BRANCH" | grep -qE "$VALID_PREFIXES"; then
  echo "WARNING: Branch '$CURRENT_BRANCH' does not follow naming conventions." >&2
  echo "" >&2
  echo "Expected prefix: feat/, fix/, refactor/, test/, chore/, docs/" >&2
  echo "Current branch : $CURRENT_BRANCH" >&2
  echo "" >&2
  echo "Proceeding anyway — but consider renaming your branch." >&2
  # exit 0: warn only, do not block
fi

# ── All checks passed ─────────────────────────────────────────────────────────
echo "Git check passed: branch='$CURRENT_BRANCH', working tree clean." >&2
exit 0