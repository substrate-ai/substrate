FROM 038700340820.dkr.ecr.us-east-1.amazonaws.com/substrate-ai:base

ARG PYTHON_VERSION=3.10

COPY requirements.txt /requirements.txt

RUN python${PYTHON_VERSION} -m pip install --no-cache-dir -r /requirements.txt

COPY ./code /code

ARG MAIN_LOCATION
ENV MAIN_LOCATION_VAR=$MAIN_LOCATION

ENTRYPOINT s3fs substrate-user-test /substrate; python3.10 /code/$MAIN_LOCATION_VAR