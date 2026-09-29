#!/bin/bash

set -e

BRANCH="$1"

# Merge concurrent remote changes and replace only files synchronized from PRs.
# Never rewrite the remote history to resolve a content conflict.
reconcile_remote() {
  local sync_commit
  local file
  sync_commit=$(git rev-parse HEAD)

  # Actions checkouts are shallow by default; a merge requires the common history.
  if [[ "$(git rev-parse --is-shallow-repository)" == true ]]; then
    git fetch --unshallow origin
  fi
  git fetch origin "$BRANCH"

  if ! git merge --no-commit --no-ff FETCH_HEAD; then
    # Only PR-owned files can be resolved automatically.
    if [[ ! -f "$(git rev-parse --git-path MERGE_HEAD)" ]]; then
      return 1
    fi
  fi

  if [[ -n "$SYNC_FILES_MANIFEST" && -f "$SYNC_FILES_MANIFEST" ]]; then
    while IFS= read -r -d '' file; do
      # Restore the entire processed PR file, including non-conflicting changes.
      if git cat-file -e "$sync_commit:$file" 2>/dev/null; then
        git restore --source="$sync_commit" --staged --worktree -- "$file"
      else
        git rm -f --ignore-unmatch -- "$file"
      fi
    done < "$SYNC_FILES_MANIFEST"
  fi

  if [[ -n "$(git ls-files -u)" ]]; then
    echo "Conflicts outside the synchronized PR files require manual resolution:"
    git diff --name-only --diff-filter=U
    git merge --abort
    return 1
  fi

  if [[ -f "$(git rev-parse --git-path MERGE_HEAD)" ]]; then
    git commit -m "Merge remote preview changes, preserving synchronized PR files"
  elif ! git diff --cached --quiet; then
    git commit -m "Restore synchronized PR files after remote update"
  fi
}

# Retry boundedly if another writer advances the branch during reconciliation.
for attempt in 1 2 3; do
  if git push origin "HEAD:refs/heads/$BRANCH"; then
    [[ -z "$SYNC_FILES_MANIFEST" ]] || rm -f "$SYNC_FILES_MANIFEST"
    exit 0
  fi
  if [[ "$attempt" == 3 ]]; then
    echo "Push failed after three attempts; remote history was preserved."
    exit 1
  fi
  reconcile_remote
done
