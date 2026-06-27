# AGENTS.md

Repo of shell + Python tooling that syncs PingCAP doc PRs into `markdown-pages/`
for preview deployments. The Gatsby site itself lives in a separate repo
(`pingcap/website-docs`) cloned on demand by `build.sh`; this repo only feeds it
content and config.

## Commands

- Preview site locally: `./build.sh dev` (or `build.sh develop`).
- Production build: `./build.sh` (defaults to `build`). Both commands auto-clone
  `pingcap/website-docs` into `./website-docs/`, symlink `markdown-pages/` into
  it, copy `docs.json` + `tooltip-terms.json`, then run `pnpm install --frozen-
  lockfile` inside that clone.
- Run all tests: `python3 test/test.py` from repo root.
- There is no root `pnpm install`, lint, or typecheck — `package.json` only pins
  the pnpm version used inside `website-docs/`.

## Test setup (easy to miss)

Tests are driven by `test_config.toml` + `test/test.py` (Python 3.11, uses
`tomllib`). The runner **requires a root-level `.env`** (gitignored) containing
at minimum:

```
GITHUB_TOKEN=<repo-scope token>
TEST=1
DOCS_PR=<num>
DOCS_CN_PR=<num>
CLOUD_DOCS_PR=<num>
OPERATOR_DOCS_PR=<num>
RELEASE_DIR=release-6.7
```

CI populates this file in `.github/workflows/run_tests.yml`. Without `.env`
locally the runner crashes at `_load_env`. `TEST=1` makes the sync scripts
skip commits so the test harness can diff `data/` against the generated
`actual/` directory.

## Toolchain quirks

- Shell scripts prefer GNU coreutils: they resolve `gfind`/`gsed` before
  `find`/`sed`. On macOS install `findutils` + `gnu-sed` via Homebrew or the
  image-path rewrites in `build.sh` and the `{{< copyable >}}` stripping in
  `sync_pr.sh` will misbehave.
- `jq` is required by `sync_pr.sh` and `prune_preview_branches.sh`.
- Python scripts use `#!/usr/bin/env python3`; `replace_variables.py` replaces
  `{{{ .path.to.var }}}` placeholders in Markdown from `variables.json`.

## Branch naming convention (drives sync behavior)

`sync_pr.sh` parses the *current* git branch name to decide what to sync. The
prefix is load-bearing:

- `preview/pingcap/docs/<PR>` → TiDB docs (`en` by default)
- `preview/pingcap/docs-cn/<PR>` → TiDB docs (`zh`)
- `preview-cloud/pingcap/docs/<PR>` → TiDB Cloud (`en/tidbcloud/master`)
- `preview-operator/pingcap/docs-tidb-operator/<PR>` → operator docs (both
  `en/` and `zh/` under `tidb-in-kubernetes/`)

A PR base branch of the form `i18n-<locale>-<master|release-*>` is normalized to
`markdown-pages/<locale>/<product>/<master|release-*>`. `preview_docs.sh` is the
helper that creates these branches and pushes them; it refuses to push to
`main`, `master`, or `release-*`.

## Sync flow & env vars

- `sync_scaffold.sh` pulls `TOC*.md`, `_index.md`, `_docHome.md`, `docs.json`,
  and `tooltip-terms.json` from `pingcap/docs-staging` (default `main`, or a
  commit/branch passed as `$1`). Triggered by `sync_scaffold.yml` every 15 days.
- `sync_pr.sh` clones the source repo, fetches the PR ref, and copies only
  files changed relative to the PR base (`git diff --merge-base`), then runs
  `scripts/replace_variables.py` and strips `{{< copyable "..." >}}` lines. For
  `preview`/`preview-operator` it also mirrors TOC-namespace folders
  (`ai`, `develop`, `best-practices`, `api`, `releases` for tidb; `releases`
  for operator) into the stable branch path read from `docs.json` so previews
  reflect canonical URLs.
- `sync_mult_prs.sh` calls `sync_pr.sh` four times and rsyncs `master` →
  `RELEASE_DIR`. Env vars it reads (must match what `sync_mult_prs.yml` sets):
  `DOCS_PR`, `DOCS_CN_PR`, `CLOUD_DOCS_PR`, `OPERATOR_DOCS_PR`, `RELEASE_DIR`.
  Note the `CLOUD_DOCS_PR` spelling — `preview_docs.sh --cloud-pr` maps to this
  name, not `CLOUD_PR`.
- `TEST` env var (any non-empty value) makes every sync script skip its
  `git commit` step. Essential for tests; easy to leave set by accident in a
  real shell session.
- All sync workflows commit via `.github/git_push.sh <ref>` using
  `Docsite Preview Bot` identity; pushes happen back to the same branch the
  workflow ran on.

## Source-of-truth files

- `docs.json` — declares products, languages, version lists, stable branch,
  deprecated/archived/dmr versions, and TiDB Cloud OpenAPI spec URLs. Both
  `build.sh` and `sync_pr.sh` read it. Update here, not in `website-docs/`.
- `test_config.toml` — declares each test target script, its `diff_command`,
  `test_dependencies`, and per-case `args` + expected-output `directory`.

## Conventions

- Generated/clone artifacts `temp/`, `website-docs/`, and `.env` are gitignored
  — never commit them. `preview_docs.sh` stages only
  `.github/workflows/sync_mult_prs.yml` in multi-PR mode to avoid sweeping up
  stray `temp/` clones; follow that pattern when adding new flows.
- Preview branches (`preview*`) are pruned by `prune_preview_branches.sh` /
  `prune_branches.yml` once the upstream PR is merged. `DELETE_BRANCHES=remote`
  deletes on `origin`; default (unset) takes no delete action.
- Tests diff `data/` (expected) vs `actual/` (generated under each
  `test/<case>/`). When changing sync behavior, update the committed `data/`
  fixtures, not the runner.