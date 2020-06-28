# upload_podspec

Python自动化脚本，内容包含自动commit，打版本tag，lint检查podspec合法性，并上传至指定specs地址。

## 如何使用 ?

- 在`xxx.podspec`中指定`s.version`对应的版本，若为`Binary`二进制版本则需要在版本后加`.Binary`
（例如：1.5.0.Binary）
- 新增`upload.ini`版本更新说明
- 修改`upload.py`文件信息

```python 
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
```
- 授权并执行脚本即可

```python
chmod 777 upload.py
python3 upload.py
```

