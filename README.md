# upload_podspec

A python script for auto lint and push podspec, include auto commit and push code, then push a git tag, finally lint and push podspec.

## How to use ?

Step 1 : You just need to modify global variable in `upload.py` file like below.

```python 
spec_path = './iMetisSDK.podspec'
spec_name = 'iMetisSDK.podspec'
specs_name = 'AIjiaSpecs'
source_specs_url = 'ssh://git@gitlab.263nt.com:2200/italkbbspecs/italkbbspecs.git'
```

Step2 : Add executable permissions to the script

```python
chmod 777 upload.py
```

Step3: Run `upload.py` on python3

```python
# run it as python-script 
./upload.py 

# also run it on python3
python3 upload.py
```

