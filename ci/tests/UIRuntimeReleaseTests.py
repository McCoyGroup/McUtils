"""Content identity, verified CDN selection, and publication against local Git."""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"

import ast
import contextlib
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[2]
STATE=runpy.run_path(str(ROOT/'McUtils/Jupyter/JHTML/JavaScript.py'))['JSState']
PUBLISHER=runpy.run_path(str(ROOT/'ci/publish_ui_runtime.py'))
MANIFEST='McUtils/Jupyter/JHTML/resources/runtime.json'


class RuntimeIdentityTests(unittest.TestCase):
    def files(self):
        return {path:(ROOT/path).read_bytes() for path in STATE.runtime_info()['assets']}

    def test_content_identity_ignores_json_format_and_checkout_line_endings(self):
        files=self.files();expected=STATE.runtime_info(read=files.__getitem__)
        files[MANIFEST]=json.dumps(json.loads(files[MANIFEST]),sort_keys=True).encode()
        for path in files:
            if path!=MANIFEST:files[path]=files[path].replace(b'\n',b'\r\n')
        self.assertEqual(STATE.runtime_info(read=files.__getitem__),expected)
        self.assertRegex(expected['tag'],r'^mcui-1-[0-9a-f]{64}$')

    def test_asset_contract_and_dependency_changes_each_change_identity(self):
        original=self.files();identity=STATE.runtime_info(read=original.__getitem__)
        for change in ('asset','contract','dependency','interface'):
            with self.subTest(change=change):
                files=dict(original);metadata=json.loads(files[MANIFEST])
                if change=='asset':files[metadata['assets'][1]]+=b'\n/* updated */\n'
                if change=='contract':metadata['bindings']['dom']['text']='both'
                if change=='dependency':metadata['dependencies']['plotly']='https://example.test/plotly.js'
                if change=='interface':metadata['interface']=2
                files[MANIFEST]=json.dumps(metadata).encode()
                new=STATE.runtime_info(read=files.__getitem__)
                self.assertNotEqual(new['fingerprint'],identity['fingerprint'])
                if change=='interface':self.assertTrue(new['tag'].startswith('mcui-2-'))

    def test_invalid_manifest_cannot_escape_asset_tree(self):
        for key,value in [('interface',True),('interface',0),('repository','bad/repo\nname'),
                          ('assets',['../outside.js'])]:
            files=self.files();metadata=json.loads(files[MANIFEST]);metadata[key]=value
            if key=='assets':metadata['entry']=value[0]
            files[MANIFEST]=json.dumps(metadata).encode()
            with self.subTest(key=key),self.assertRaises(ValueError):
                STATE.runtime_info(read=files.__getitem__)

    def test_cdn_export_verifies_all_assets_once_and_rejects_unpublished_edits(self):
        namespace=STATE.cdn_url.__func__.__globals__
        verify=namespace['_verify_runtime_assets'];verify.cache_clear()
        files=self.files();info=STATE.runtime_info()
        def fetch(url):return files[url.removeprefix(info['base'])].decode()
        try:
            with mock.patch.dict(namespace,{'_fetch_asset':mock.Mock(side_effect=fetch)}):
                self.assertEqual(STATE.runtime_path(javascript_path='cdn'),info['script'])
                self.assertEqual(STATE.cdn_url(),info['script'])
                self.assertEqual(namespace['_fetch_asset'].call_count,len(files))
            verify.cache_clear()
            with mock.patch.dict(namespace,{'_fetch_asset':mock.Mock(side_effect=OSError('not published'))}):
                with self.assertRaisesRegex(RuntimeError,'inline'):STATE.cdn_url()
            verify.cache_clear();files['McUtils/Jupyter/Apps/resources/native.css']+=b'bad'
            with mock.patch.dict(namespace,{'_fetch_asset':fetch}):
                with self.assertRaisesRegex(RuntimeError,'does not match'):STATE.cdn_url()
        finally:verify.cache_clear()


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory();self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name);self.work=self.root/'work';self.work.mkdir()
        self.remote=self.root/'remote.git'
        self.environment=mock.patch.dict(os.environ,{'GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_SYSTEM':'/dev/null',
                                                    'GIT_TERMINAL_PROMPT':'0','GIT_AUTHOR_DATE':'2026-11-07T12:00:00Z',
                                                    'GIT_COMMITTER_DATE':'2026-11-07T12:00:00Z'})
        self.environment.start();self.addCleanup(self.environment.stop)
        paths=set(STATE.runtime_info()['assets'])|{'McUtils/Jupyter/JHTML/JavaScript.py','ci/publish_ui_runtime.py'}
        for path in paths:
            dest=self.work/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,dest)
        self.git('init','--bare',str(self.remote))
        self.git('init')
        self.git('config','user.name','UI Runtime Test')
        self.git('config','user.email','runtime-test@example.invalid')
        self.git('remote','add','origin',str(self.remote))
        self.commit('initial')

    def git(self,*args):
        return subprocess.run(['git',*args],cwd=self.work,check=True,capture_output=True,text=True).stdout.strip()

    def commit(self,message):
        self.git('add','.')
        self.git('commit','-m',message)
        return self.git('rev-parse','HEAD')

    def publish(self,**options):return PUBLISHER['publish'](self.work,**options)

    def test_first_publish_then_reuse_after_unrelated_commit(self):
        first=self.publish();self.assertEqual(first['status'],'published')
        (self.work/'unrelated.txt').write_text('numerical change')
        self.commit('unrelated')
        second=self.publish();self.assertEqual(second['status'],'reused')
        self.assertEqual(first['tag'],second['tag']);self.assertEqual(first['commit'],second['commit'])
        self.assertEqual(len(self.git('ls-remote','--tags','origin').splitlines()),1)

    def test_changed_runtime_creates_new_tag_and_preserves_old_tag(self):
        first=self.publish()
        css=self.work/'McUtils/Jupyter/Apps/resources/native.css';css.write_bytes(css.read_bytes()+b'\n/* new */\n')
        self.commit('runtime update');second=self.publish()
        self.assertEqual(second['status'],'published');self.assertNotEqual(first['tag'],second['tag'])
        self.assertEqual(self.git('ls-remote','--tags','origin','refs/tags/'+first['tag']).split()[0],first['commit'])

    def test_uncommitted_assets_and_wrong_validated_identity_cannot_publish(self):
        with self.assertRaisesRegex(RuntimeError,'passed validation'):self.publish(expected_tag='wrong')
        css=self.work/'McUtils/Jupyter/Apps/resources/native.css';css.write_bytes(css.read_bytes()+b'\nchanged')
        with self.assertRaisesRegex(RuntimeError,'uncommitted'):self.publish()
        self.assertEqual(self.git('ls-remote','--tags','origin'),'')

    def test_existing_wrong_tag_is_never_overwritten(self):
        old=self.git('rev-parse','HEAD')
        css=self.work/'McUtils/Jupyter/Apps/resources/native.css';css.write_bytes(css.read_bytes()+b'\nchanged')
        self.commit('new runtime')
        identity=PUBLISHER['load_state'](self.work).runtime_info();ref='refs/tags/'+identity['tag']
        self.git('push','origin',old+':'+ref)
        with self.assertRaisesRegex(RuntimeError,'refusing to overwrite'):self.publish()
        self.assertEqual(self.git('ls-remote','--tags','origin',ref).split()[0],old)

    def test_identical_annotated_tag_is_reused(self):
        identity=PUBLISHER['load_state'](self.work).runtime_info()
        self.git('tag','-a',identity['tag'],'-m','same assets');self.git('push','origin','refs/tags/'+identity['tag'])
        self.assertEqual(self.publish()['status'],'reused')

    def test_concurrent_identical_publication_is_reused_after_push_rejection(self):
        namespace=PUBLISHER['publish'].__globals__;original=namespace['git']
        def race(root,*arguments,**kwargs):
            if arguments[0]=='push':
                original(root,*arguments)
                return subprocess.CompletedProcess(['git'],1,stdout=b'',stderr=b'already exists')
            return original(root,*arguments,**kwargs)
        with mock.patch.dict(namespace,{'git':race}):
            self.assertEqual(self.publish()['status'],'reused')

    def test_identity_and_dry_run_work_without_git_metadata_or_numerical_dependencies(self):
        shutil.rmtree(self.work/'.git')
        self.assertEqual(PUBLISHER['load_state'](self.work).runtime_info(),STATE.runtime_info())
        with contextlib.redirect_stdout(io.StringIO()),mock.patch.dict(os.environ,{'GITHUB_OUTPUT':'','GITHUB_STEP_SUMMARY':''}):
            result=PUBLISHER['main'](['--root',str(self.work)])
        self.assertEqual(result['status'],'inspected')
        self.assertFalse((self.work/'.git').exists())

    def test_python_package_version_ignores_runtime_tags(self):
        self.git('tag','v2.0.0')
        (self.work/'unrelated.txt').write_text('later');self.commit('later');self.publish()
        # Execute only the existing setup.py version function, never setup().
        tree=ast.parse((ROOT/'setup.py').read_text())
        function=next(item for item in tree.body if isinstance(item,ast.FunctionDef) and item.name=='get_version')
        namespace={};exec(compile(ast.Module(body=[function],type_ignores=[]),'<get_version>','exec'),namespace)
        original=subprocess.run
        def run(args,**options):return original(args,cwd=self.work,**options)
        with mock.patch('subprocess.run',side_effect=run):self.assertEqual(namespace['get_version'](),'2.0.0')


class WorkflowTests(unittest.TestCase):
    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_publication_requires_validation_and_default_branch_with_isolated_write_permission(self):
        try:import yaml
        except ImportError:self.skipTest('PyYAML is optional for local workflow checks')
        workflow=yaml.load((ROOT/'.github/workflows/ui-runtime.yml').read_text(),Loader=yaml.BaseLoader)
        self.assertEqual(workflow['permissions'],{'contents':'read'})
        self.assertIn('pull_request',workflow['on']);self.assertNotIn('pull_request_target',workflow['on'])
        publish=workflow['jobs']['publish']
        self.assertEqual(publish['needs'],'validate');self.assertEqual(publish['permissions'],{'contents':'write'})
        self.assertIn("github.event_name != 'pull_request'",publish['if'])
        self.assertIn('github.event.repository.default_branch',publish['if'])
        self.assertEqual(publish['steps'][0]['with']['ref'],'${{ github.sha }}')
        command=publish['steps'][-1]['run']
        self.assertIn('--expected-tag',command);self.assertNotIn('--force',command)
        pypi=yaml.load((ROOT/'.github/workflows/publish.yml').read_text(),Loader=yaml.BaseLoader)
        self.assertEqual(pypi['jobs']['pypi-publish']['if'],"startsWith(github.event.release.tag_name, 'v')")


if __name__=='__main__':unittest.main()
