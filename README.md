# upload_podspec

中文文档移步：[中文文档](./README_zh.md)

Python automated scripts, including automatic commit, version tag, lint check podspec legality, and upload to the specified specs address.

## how to use ?

- Specify the version corresponding to `s.version` in `xxx.podspec`
- Modify `upload.py` file information

```python
spec_path ='./iMetisSDK.podspec'
spec_name ='iMetisSDK.podspec'
specs_name ='AIjiaSpecs'
source_specs_url ='ssh://git@gitlab.263nt.com:2200/italkbbspecs/italkbbspecs.git'

config_ini_path ='./upload.ini'

gitlab_remote ='origin'
gitlab_ref ='master'
gitlab_proj_id = 19
gitlab_user_access_token ='KLRVtbPLihP6eug-i7-d' #'qWXXuozFKgcDjCUWz26x'

gitlab_api_url ='https://gitlab.263nt.com/api/v4/projects/%d/releases'% gitlab_proj_id
```
- Just authorize and execute the script

```python
chmod 777 upload.py
python3 upload.py
```
