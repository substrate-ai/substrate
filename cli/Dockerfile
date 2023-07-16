# Container for building the environment
FROM --platform=linux/amd64 condaforge/mambaforge as conda

# Install the package as normal:
COPY environment.yml .

RUN conda env create -f environment.yml && \
    conda install -c conda-forge conda-pack && \
    conda clean -ya

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n substrate-conda-env -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM --platform=linux/amd64 nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu20.04 as runtime

# Copy /venv from the previous stage:
COPY --from=conda /venv /venv

RUN du -sh /venv && sleep 100

COPY code ~/code

# When image is run, run the code with the environment
# activated:
SHELL ["/bin/bash", "-c"]
RUN chmod +x /venv/bin/activate

ENTRYPOINT ["/venv/bin/activate", "&&", "python", "~/code/main.py"]