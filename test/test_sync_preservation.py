"""Offline regression tests for PR synchronization and concurrent preview pushes."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run(cwd, *args, check=True, env=None):
    result = subprocess.run(args, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and result.returncode:
        raise AssertionError(result.stdout)
    return result


def write(root, name, content):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def commit(repo, message):
    run(repo, 'git', 'add', '.')
    run(repo, 'git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com',
        'commit', '-m', message)


class SyncPreservationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL='/dev/null',
                        GIT_CONFIG_NOSYSTEM='1', GIT_AUTHOR_NAME='Test',
                        GIT_AUTHOR_EMAIL='test@example.com', GIT_COMMITTER_NAME='Test',
                        GIT_COMMITTER_EMAIL='test@example.com')

    def test_only_pr_files_are_copied_and_processed(self):
        source = self.root / 'temp/docs'
        source.mkdir(parents=True)
        run(source, 'git', 'init', '-b', 'master')
        write(source, 'variables.json', '{"name": "PR value"}')
        write(source, 'changed.md', 'old\n')
        commit(source, 'base')
        run(source, 'git', 'update-ref', 'refs/remotes/origin/master', 'HEAD')
        write(source, 'changed.md', '{{{ .name }}}\n{{< copyable "sql" >}}\n\nSQL\n')
        write(source, 'TOC-tidb-cloud.md', '# PR TOC\n')
        write(source, 'tidb-cloud-filesystem/new.md', '{{{ .name }}}\n')
        write(source, 'media/pr.png', 'PR bytes')
        commit(source, 'PR')
        dest = 'markdown-pages/en/tidbcloud/master'
        untouched = '{{{ .missing }}}\n{{< copyable "sql" >}}\n\nkeep\n'
        write(self.root, dest + '/manual.md', untouched)
        write(self.root, dest + '/changed.md', 'preview copy\n')
        write(self.root, dest + '/variables.json', '{"name": "preview value"}')
        write(self.root, dest + '/media/manual.png', 'manual image')
        write(self.root, dest + '/media/pr.png', 'old data')
        # Rsync's size/mtime shortcut must not skip a different PR file.
        os.utime(source / 'media/pr.png', (1000000000, 1000000000))
        os.utime(self.root / dest / 'media/pr.png', (1000000000, 1000000000))
        shutil.copytree(ROOT / 'scripts', self.root / 'scripts')
        functions = (ROOT / 'sync_pr.sh').read_text().split(
            '# Select the appropriate version of sed')[0]
        write(self.root, 'functions.sh', functions)
        env = dict(self.env, TEST='1', SYNC_FILES_MANIFEST=str(self.root / 'manifest'))
        run(self.root, 'bash', '-c', '''
source functions.sh
REPO_DIR=temp/docs
REPO_NAME=docs
REPO_OWNER=pingcap
PR_NUMBER=1
PREVIEW_PRODUCT=preview-cloud
BASE_BRANCH=master
SED=$(command -v gsed || command -v sed)
parse_i18n_base
get_destination_suffix
perform_sync_task
''', env=env)
        self.assertEqual((self.root / dest / 'changed.md').read_text(), 'PR value\nSQL\n')
        self.assertEqual((self.root / dest / 'manual.md').read_text(), untouched)
        self.assertEqual((self.root / dest / 'variables.json').read_text(),
                         '{"name": "preview value"}')
        self.assertEqual((self.root / dest / 'media/manual.png').read_text(), 'manual image')
        self.assertEqual((self.root / dest / 'media/pr.png').read_text(), 'PR bytes')
        self.assertEqual((self.root / dest / 'TOC.md').read_text(), '# PR TOC\n')
        self.assertEqual((self.root / 'markdown-pages/en/tidb-cloud-filesystem/master/tidb-cloud-filesystem/new.md')
                         .read_text(), 'PR value\n')
        manifest = (self.root / 'manifest').read_bytes().split(b'\0')
        self.assertNotIn((dest + '/manual.md').encode(), manifest)
        self.assertIn((dest + '/TOC.md').encode(), manifest)

    def test_stable_namespace_uses_target_variables_and_preserves_other_pages(self):
        source = self.root / 'temp/docs'
        source.mkdir(parents=True)
        run(source, 'git', 'init', '-b', 'master')
        write(source, 'variables.json', '{"name": "dev"}')
        commit(source, 'base')
        run(source, 'git', 'update-ref', 'refs/remotes/origin/master', 'HEAD')
        write(source, 'develop/example.md', '{{{ .name }}}\n')
        commit(source, 'PR')
        stable = 'markdown-pages/en/tidb/release-8.5'
        write(self.root, stable + '/variables.json', '{"name": "stable"}')
        write(self.root, stable + '/manual.md', '{{{ .missing }}}\n')
        write(self.root, 'docs.json', '{"docs": {"tidb": {"stable": "release-8.5"}}}')
        shutil.copytree(ROOT / 'scripts', self.root / 'scripts')
        functions = (ROOT / 'sync_pr.sh').read_text().split(
            '# Select the appropriate version of sed')[0]
        write(self.root, 'functions.sh', functions)
        run(self.root, 'bash', '-c', '''
source functions.sh
REPO_DIR=temp/docs
REPO_NAME=docs
REPO_OWNER=pingcap
PR_NUMBER=1
PREVIEW_PRODUCT=preview
BASE_BRANCH=master
SED=$(command -v gsed || command -v sed)
parse_i18n_base
get_destination_suffix
perform_sync_task
''', env=dict(self.env, TEST='1'))
        self.assertEqual((self.root / 'markdown-pages/en/tidb/master/develop/example.md')
                         .read_text(), 'dev\n')
        self.assertEqual((self.root / stable / 'develop/example.md').read_text(), 'stable\n')
        self.assertEqual((self.root / stable / 'manual.md').read_text(), '{{{ .missing }}}\n')

    def setup_push(self, shallow=False):
        remote = self.root / 'remote.git'
        run(self.root, 'git', 'init', '--bare', str(remote))
        writer = self.root / 'writer'
        run(self.root, 'git', 'clone', remote.as_uri(), str(writer))
        run(writer, 'git', 'checkout', '-b', 'preview')
        write(writer, 'markdown-pages/changed.md', 'first\nsecond\nthird\n')
        write(writer, 'markdown-pages/unchanged-pr.md', 'PR unchanged\n')
        write(writer, 'markdown-pages/manual.md', 'original\n')
        commit(writer, 'base')
        run(writer, 'git', 'push', 'origin', 'preview')
        worker = self.root / 'worker'
        args = ['git', 'clone', '-b', 'preview']
        if shallow:
            args += ['--depth=1']
        run(self.root, *args, remote.as_uri(), str(worker))
        return remote, writer, worker

    def push_script(self, worker, paths):
        manifest = self.root / 'manifest'
        manifest.write_bytes(b''.join(p.encode() + b'\0' for p in paths))
        return run(worker, 'bash', str(ROOT / '.github/git_push.sh'), 'preview',
                   env=dict(self.env, SYNC_FILES_MANIFEST=str(manifest)), check=False)

    def test_remote_files_preserved_and_pr_files_replace_entire_content(self):
        remote, writer, worker = self.setup_push(shallow=True)
        # Disjoint line edits would merge cleanly, but the complete PR file must win.
        write(worker, 'markdown-pages/changed.md', 'PR first\nsecond\nthird\n')
        write(worker, 'markdown-pages/TOC.md', 'PR TOC\n')
        commit(worker, 'sync PR')
        write(writer, 'markdown-pages/changed.md', 'first\nsecond\nremote third\n')
        write(writer, 'markdown-pages/TOC.md', 'remote TOC\n')
        write(writer, 'markdown-pages/unchanged-pr.md', 'remote edit\n')
        write(writer, 'markdown-pages/manual.md', 'manual edit\n')
        write(writer, 'markdown-pages/media/extra.png', 'manual image')
        commit(writer, 'manual preview changes')
        remote_tip = run(writer, 'git', 'rev-parse', 'HEAD').stdout.strip()
        run(writer, 'git', 'push', 'origin', 'preview')
        result = self.push_script(worker, ['markdown-pages/changed.md',
                                          'markdown-pages/TOC.md',
                                          'markdown-pages/unchanged-pr.md'])
        self.assertEqual(result.returncode, 0, result.stdout)
        run(writer, 'git', 'pull', '--ff-only', 'origin', 'preview')
        self.assertEqual((writer / 'markdown-pages/changed.md').read_text(),
                         'PR first\nsecond\nthird\n')
        self.assertEqual((writer / 'markdown-pages/TOC.md').read_text(), 'PR TOC\n')
        self.assertEqual((writer / 'markdown-pages/unchanged-pr.md').read_text(), 'PR unchanged\n')
        self.assertEqual((writer / 'markdown-pages/manual.md').read_text(), 'manual edit\n')
        self.assertEqual((writer / 'markdown-pages/media/extra.png').read_text(), 'manual image')
        run(writer, 'git', 'merge-base', '--is-ancestor', remote_tip, 'HEAD')

    def test_unrelated_conflict_fails_without_changing_remote(self):
        remote, writer, worker = self.setup_push()
        write(worker, 'markdown-pages/manual.md', 'worker manual\n')
        commit(worker, 'local manual')
        write(writer, 'markdown-pages/manual.md', 'remote manual\n')
        commit(writer, 'remote manual')
        remote_tip = run(writer, 'git', 'rev-parse', 'HEAD').stdout.strip()
        run(writer, 'git', 'push', 'origin', 'preview')
        result = self.push_script(worker, ['markdown-pages/changed.md'])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('require manual resolution', result.stdout)
        self.assertEqual(run(remote, 'git', 'rev-parse', 'refs/heads/preview').stdout.strip(),
                         remote_tip)
        self.assertFalse((worker / '.git/MERGE_HEAD').exists())


if __name__ == '__main__':
    unittest.main()
