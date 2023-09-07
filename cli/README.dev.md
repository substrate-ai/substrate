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
python -m pip install -e ../cli   
```


## Notes

docker build -f Dockerfile.substrate-ai . -t substrate-ai