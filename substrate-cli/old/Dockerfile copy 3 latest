# Container for building the environment
FROM --platform=linux/amd64 nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu20.04 as conda


RUN apt-get update && DEBIAN_FRONTEND=noninteractive && apt-get install -y --no-install-recommends \
    curl && \
    rm -rf /var/lib/apt/lists/* && \
    curl -Lo ~/mambaforge.sh -O  https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh && \
    bash ~/mambaforge.sh -b -p /opt/conda

ENV PATH /opt/conda/bin:$PATH
ARG CONDA_ENV_NAME=substrate-conda-env


COPY environment.yml .

RUN conda env create -f environment.yml && \
    conda install -c conda-forge conda-pack && \
    conda clean -ya && \
    conda-pack -n ${CONDA_ENV_NAME} -o /tmp/env.tar && \
    mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
    rm /tmp/env.tar && \
    conda remove --name ${CONDA_ENV_NAME} --all && \
    /venv/bin/conda-unpack


FROM --platform=linux/amd64 nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu20.04 as runtime

COPY --from=conda /venv /venv

COPY src /src

SHELL ["/bin/bash", "-c"]
ENTRYPOINT source /venv/bin/activate && \
           python /src/main.py
