ARG PYTHON_VERSION=alpine3.17
FROM python:$PYTHON_VERSION

RUN apk --no-cache add curl gcc musl-dev libffi-dev make
COPY requirements.yml github-influx.* /
RUN pip3 install --requirement /requirements.yml \
    && chmod +x /github-influx.sh

ENV GITHUB_TOKEN="" \
    GITHUB_DAYS="" \
    INFLUX_ULR="" \
    INFLUX_CREDS="" \
    INFLUX_LABELS=""

ENTRYPOINT ["/bin/sh"]
CMD ["/github-influx.sh"]
