ARG PYTHON_VERSION=alpine
FROM python:$PYTHON_VERSION

RUN apk --no-cache add curl gcc musl-dev libffi-dev
COPY requirements.yml github-influx.* /
RUN pip3 install --requirement /requirements.yml

ENV GITHUB_TOKEN="" \
    INFLUX_ULR="" \
    INFLUX_CREDS=""

ENTRYPOINT ["/bin/sh"]
CMD ["/github-influx.sh"]
