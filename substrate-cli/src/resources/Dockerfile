# Container for building the environment
FROM --platform=linux/amd64 nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu20.04 as conda

RUN DEBIAN_FRONTEND=noninteractive && apt update && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.10 python3-pip python3-setuptools python3-distutils && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN python3.10 -m pip install --upgrade pip && \
    python3.10 -m pip install --no-cache-dir -r /requirements.txt

COPY ./src /src

ARG MAIN_FILE_LOCATION=/src/main.py

ENTRYPOINT ["python3", ${MAIN_FILE_LOCATION}]
