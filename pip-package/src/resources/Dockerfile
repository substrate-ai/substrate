FROM 038700340820.dkr.ecr.us-east-1.amazonaws.com/substrate-ai:base

ARG PYTHON_VERSION=3.10

COPY requirements.txt /requirements.txt

# --disable-pip-version-check --root-user-action=ignore --no-cache-dir
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_ROOT_USER_ACTION=ignore


RUN python${PYTHON_VERSION} -m pip install -r /requirements.txt

COPY ./code /code

ARG MAIN_LOCATION
ENV MAIN_LOCATION_VAR=$MAIN_LOCATION

ENTRYPOINT python3.10 /code/$MAIN_LOCATION_VAR