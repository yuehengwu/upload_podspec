#!/usr/bin/env python3
# coding=utf-8
# @file   : upload.py
# @author : wyh
# @date   : 2020/4/27
# @version: 1.0
# @desc   : use python script to upload podspec

import re, os, time, requests, configparser

spec_path = './iMetisSDK.podspec'
spec_name = 'iMetisSDK.podspec'
specs_name = 'AIjiaSpecs'
source_specs_url = 'ssh://git@gitlab.263nt.com:2200/italkbbspecs/italkbbspecs.git'

config_ini_path = './upload.ini'

gitlab_remote = 'origin'
gitlab_ref = 'master'
gitlab_proj_id = 19
gitlab_user_access_token = 'KLRVtbPLihP6eug-i7-d'  # 'qWXXuozFKgcDjCUWz26x'

gitlab_api_url = 'https://gitlab.263nt.com/api/v4/projects/%d/releases' % gitlab_proj_id


def run():
    pod_install()

    tag = find_podspec_tag(spec_path)
    message = find_whatsnew_from_ini(config_ini_path,tag)
    git_commit(tag, message)
    push_release_tag(tag, message)

    res = lint_push_podspec(spec_name,specs_name,source_specs_url)
    if res != 0:
        delete_release_tag(tag)
    else :
        update_local_specs(specs_name)


# Update local specs
def update_local_specs(specs_name):
    os.system('pod repo update %s' % specs_name)

def pod_install():
    print('cd Example/')
    os.chdir('Example')

    print('pod install')
    os.system('pod install')

    print('cd ../')
    os.chdir('../')

# PosSpec Lint and push
def lint_push_podspec(spec_name, specs_name, source_specs_url):
    print('code git push complete, ready to lint and push spec !')
    time.sleep(3)

    spec_lint = 'pod lib lint --sources=%s --allow-warnings --verbose --use-libraries' % source_specs_url
    print(spec_lint)
    res = os.system(spec_lint)

    if res == 0:
        spec_push = 'pod repo push %s %s --allow-warnings --verbose --use-libraries' % (specs_name, spec_name)
        print(spec_push)
        res = os.system(spec_push)
    return res

# Tags
def git_commit(tag, commit_msg):
    git_add = 'git add .'
    print(git_add)
    os.system(git_add)

    git_status = 'git status'
    print(git_status)
    os.system(git_status)

    git_commit = "git commit -m '%s'" % commit_msg
    print(git_commit)
    os.system(git_commit)

    git_push = 'git push origin'
    print(git_push)
    res = os.system(git_push)
    return res
    # git_tag = 'git tag %s'%tag
    # print(git_tag)
    # os.system(git_tag)
    # os.system('git push origin --tags')


# Release HTTP
def push_release_tag(tag, description):
    # upload gitlab release tag
    print('[POST] Ready to push git release and tag:', tag)
    headers = {'Content-Type': 'application/json', 'PRIVATE-TOKEN': gitlab_user_access_token}
    body = {
        'id': gitlab_proj_id,
        'tag_name': tag,
        'description': description,
        'ref': gitlab_ref
    }

    http_res = requests.post(url=gitlab_api_url,
                             headers=headers,
                             json=body)
    print('[POST ]Push gitLab release and tag result:', http_res)


def delete_release_tag(tag):
    # delete gitlab release
    print('[Delete] step1 ready to delete git release', tag)
    headers = {'PRIVATE-TOKEN': gitlab_user_access_token}
    http_res = requests.delete(url=(gitlab_api_url + '/%s' % tag), headers=headers)

    print('[Delete] step1 delete result: ', http_res)

    # delete gitlab tag
    print('[Delete] step2 ready to delete git tag', tag)
    os.system('git tag -d %s' % tag)
    res = os.system('git push %s :refs/tags/%s' % (gitlab_remote, tag))
    print('[Delete] step2 delete git tag result', res)


# File
def find_whatsnew_from_ini(file_path,tag):
    if '.Binary' in tag:
        tag = tag.replace('.Binary','')
    cf = configparser.ConfigParser()
    cf.read(file_path,encoding='utf-8')

    whats_new = cf.get("v%s"%tag,"whats_new")
    if len(whats_new) == 0:
        whats_new = 'ready to push %s'%tag
    print('find whatsnew:',whats_new)
    return whats_new

    # with open(file_path, 'r') as f:
    #     contents = f.read().replace('\n', '').replace('\r', '')
    #     whatsnew = findContentInMiddle(contents, "s.summary='", "'s")
    #     print('find podspec summary %s from %s' % (whatsnew, file_path))
    #     return whatsnew


def find_podspec_tag(file_path):
    with open(file_path, 'r') as f:
        contents = f.read().replace('\n', '').replace('\r', '').replace(' ', '')
        version = findContentInMiddle(contents, "s.version='", "'s")
        print('find podspec version %s from %s' % (version, file_path))
        return version


def findContentInMiddle(contents, a, b):
    str = "(?s)(?<=%s).*?(?=%s)" % (a, b)

    res = re.search(str, contents).group()
    return res


if __name__ == '__main__':
    run()
