"""Inspect or publish a content-addressed UI tag; no Python package import needed.

Default invocation only prints identity/outputs. --publish validates committed
assets, reuses identical remote tags, and creates a lightweight tag without force
pushing or creating a GitHub Release. Intended for the validated default-branch
GitHub Actions job; also testable against a local bare remote.
"""
import argparse
import json
import os
from pathlib import Path
import re
import runpy
import subprocess


def load_state(root):
    return runpy.run_path(str(Path(root)/'McUtils/Jupyter/JHTML/JavaScript.py'))['JSState']


def git(root, *arguments, check=True):
    result=subprocess.run(['git',*arguments],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if check and result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8',errors='replace').strip())
    return result


def publish(root, *, remote='origin', expected_tag=None):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*',remote):
        raise ValueError('A configured Git remote name is required')
    state=load_state(root)
    identity=state.runtime_info()
    if expected_tag is not None and identity['tag']!=expected_tag:
        raise RuntimeError('UI assets differ from the identity that passed validation')
    head=git(root,'rev-parse','--verify','HEAD^{commit}').stdout.decode().strip()
    def read_tree(ref):
        return lambda path:git(root,'show',ref+':'+path).stdout
    if state.runtime_info(read=read_tree(head))!=identity:
        raise RuntimeError('Refusing to publish uncommitted UI assets; use inline export for local edits')
    ref='refs/tags/'+identity['tag']
    def existing():
        found=git(root,'ls-remote','--exit-code','--refs',remote,ref,check=False)
        if found.returncode==2:return None
        if found.returncode:
            raise RuntimeError('Cannot inspect the runtime tag: '+found.stderr.decode(errors='replace'))
        records=[line.split() for line in found.stdout.decode().splitlines()]
        if len(records)!=1 or records[0][1]!=ref:
            raise RuntimeError('Unexpected remote runtime tag response')
        git(root,'fetch','--no-tags',remote,ref)
        commit=git(root,'rev-parse','--verify','FETCH_HEAD^{commit}').stdout.decode().strip()
        if state.runtime_info(read=read_tree(commit))!=identity:
            raise RuntimeError('Existing runtime tag has different content; refusing to overwrite '+identity['tag'])
        return commit
    commit=existing()
    if commit is not None:
        return dict(identity,status='reused',commit=commit)
    pushed=git(root,'push',remote,head+':'+ref,check=False)
    if pushed.returncode:
        # Another validated run may have published the same content first.
        commit=existing()
        if commit is None:
            raise RuntimeError('Runtime tag push failed: '+pushed.stderr.decode(errors='replace'))
        return dict(identity,status='reused',commit=commit)
    return dict(identity,status='published',commit=head)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--publish',action='store_true')
    parser.add_argument('--remote',default='origin')
    parser.add_argument('--expected-tag')
    args=parser.parse_args(argv)
    if args.publish:
        result=publish(args.root,remote=args.remote,expected_tag=args.expected_tag)
    else:
        result=dict(load_state(args.root).runtime_info(),status='inspected')
    print(json.dumps(result,indent=2,sort_keys=True))
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'],'a',encoding='utf-8') as stream:
            for key in ('tag','script','interface','status'):
                stream.write('{}={}\n'.format(key,result[key]))
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a',encoding='utf-8') as stream:
            stream.write('UI runtime **{}**: `{}`\n\n[Exact CDN entry]({})\n'.format(
                result['status'],result['tag'],result['script']))
    return result


if __name__=='__main__':
    main()
