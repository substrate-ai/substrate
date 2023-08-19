FROM --platform=linux/amd64 nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu20.04


ARG DEBIAN_FRONTEND=noninteractive

ARG PYTHON_VERSION=3.10

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential software-properties-common curl && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get install --no-install-recommends -y python${PYTHON_VERSION} python3-pip python3-setuptools python${PYTHON_VERSION}-distutils && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

COPY requirements.txt /requirements.txt

RUN  python${PYTHON_VERSION} -m pip install --no-cache-dir -r /requirements.txt

COPY . /code

ARG MAIN_FILE_LOCATION=/code/main.py

ENTRYPOINT ["python3", "/code/main.py"]