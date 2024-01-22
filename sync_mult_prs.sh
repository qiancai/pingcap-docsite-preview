#!/bin/bash

# Synchronize the content of multiple PRs to the markdown-pages folder to deploy a preview website.

# Usage: ./sync_mult_prs.sh

set -ex

# Get the directory of this script.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR"


# Define the PRs to sync.
# The PRs will be synced in the order of the following statements.
./sync_pr.sh preview/pingcap/docs/15702
./sync_pr.sh preview/pingcap/docs-cn/15667
./sync_pr.sh preview/pingcap/docs/16041
./sync_pr.sh preview/pingcap/docs-cn/16060
# ./sync_pr.sh preview-cloud/pingcap/docs/xxxx
# ./sync_pr.sh preview-operator/pingcap/docs-tidb-operator/"$OPERATOR_DOCS_PR"

# Synchronize the content from master to release-7.6 directories.
rsync -av markdown-pages/zh/tidb/master/ markdown-pages/zh/tidb/release-7.6/
rsync -av markdown-pages/en/tidb/master/ markdown-pages/en/tidb/release-7.6/
# rsync -av markdown-pages/en/tidb-in-kubernetes/master/ markdown-pages/en/tidb-in-kubernetes/"$RELEASE_DIR"/
# rsync -av markdown-pages/zh/tidb-in-kubernetes/master/ markdown-pages/zh/tidb-in-kubernetes/"$RELEASE_DIR"/

commit_changes() {
  # Exit if TEST is set and not empty.
  test -n "$TEST" && echo "Test mode, exiting..." && exit 0
  # Handle untracked files.
  git add .
  # Commit changes, if any.
  git commit -m "Update the {release-x.y} directory" || echo "No changes to commit"
}

commit_changes
