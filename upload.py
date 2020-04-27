#!/usr/bin/env python3
# coding=utf-8
# @file   : upload.py
# @author : wyh
# @date   : 2020/4/27
# @version: 1.0
# @desc   : use python script to upload podspec

import re, os, time

spec_path = './iMetisSDK.podspec'
spec_name = 'iMetisSDK.podspec'
specs_name = 'AIjiaSpecs'
source_specs_url = 'ssh://git@gitlab.263nt.com:2200/italkbbspecs/italkbbspecs.git'

def run():
    tag = search_podspec_tag(spec_path)
    pushTag(tag)
    lint_push_podspec(spec_name,specs_name,source_specs_url)
    update_local_specs(specs_name)

# Update local specs
def update_local_specs(specs_name):
    os.system('pod repo update %s'%specs_name)

# PosSpec Lint and push
def lint_push_podspec(spec_name,specs_name,source_specs_url):
    print('code git push complete, ready to lint and push spec !')
    time.sleep(3)

    spec_lint = 'pod lib lint --sources=%s --allow-warnings --verbose'%source_specs_url
    print(spec_lint)
    res = os.system(spec_lint)

    if res == 0:
        spec_push = 'pod repo push %s %s --allow-warnings --verbose'%(specs_name,spec_name)
        print(spec_push)
        os.system(spec_push)

# Tags
def pushTag(tag):

    git_add = 'git add .'
    print(git_add)
    os.system(git_add)

    git_status = 'git status'
    print(git_status)
    os.system(git_status)

    git_commit = "git commit -m 'ready to push %s'"%tag
    print(git_commit)
    os.system(git_commit)

    git_push = 'git push origin' # git push -u origin master
    print(git_push)
    os.system(git_push)

    git_tag = 'git tag %s'%tag
    print(git_tag)
    os.system(git_tag)
    os.system('git push origin --tags')

# File

def search_podspec_tag(file_path):

    with open(file_path,'r') as f:
        contents = f.read().replace('\n', '').replace('\r', '').replace(' ', '')
        version = findContentInMiddle(contents,'s.version=','s')
        print('find podspec version %s from %s'%(version,file_path))
        return version

def findContentInMiddle(contents,a ,b):

    str = "(?s)(?<=%s).*?(?=%s)" %(a,b)

    res = re.search(str,contents).group()
    return res


if __name__ == '__main__':
    run()
