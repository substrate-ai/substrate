FROM us-east1-docker.pkg.dev/practical-robot-393509/substrate-ai/base:latest

ARG PYTHON_VERSION=3.10

COPY requirements.txt /requirements.txt

RUN python${PYTHON_VERSION} -m pip install --no-cache-dir -r /requirements.txt

COPY ./code /code

ARG MAIN_LOCATION
ENV MAIN_LOCATION_VAR=$MAIN_LOCATION

ENTRYPOINT python3.10 /code/$MAIN_LOCATION_VAR