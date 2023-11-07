# CLI 

## To install the CLI 

How to install the cli locally

create a conda environement 

``` bash
conda create --name substrate-ai-cli
```

Then activate it


``` bash
conda activate substrate-ai-cli
```


Install dependency to do once
``` bash
pip install -r requirements.txt
```

To install the substrate cli

``` bash
python -m pip install -e ../pip-package

# How to publish

``` bash
bumpver update --patch
```

``` bash
python -m build
```
``` bash
twine upload -r testpypi dist/*
```
``` bash
twine upload dist/*
```
``` bash
twine check dist/*
```

## Notes

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 038700340820.dkr.ecr.us-east-1.amazonaws.com

docker build -f Dockerfile.substrate-ai . -t substrate-ai-base
docker tag substrate-ai-base 038700340820.dkr.ecr.us-east-1.amazonaws.com/substrate-ai:base
docker push 038700340820.dkr.ecr.us-east-1.amazonaws.com/substrate-ai:base