ARG PYTHON_VERSION=alpine3.17
FROM python:$PYTHON_VERSION

RUN apk --no-cache add curl gcc musl-dev libffi-dev make
COPY github-influx.* /

RUN addgroup -S python && \
    adduser -S python -G python && \
    chmod +x /github-influx.sh

USER python
COPY requirements.yml /home/python
RUN export PATH=$PATH:/home/python/.local/bin \
    && pip3 install -U pip \
    && pip3 install --requirement /home/python/requirements.yml

ENV GITHUB_TOKEN="" \
    GITHUB_DAYS="" \
    INFLUX_ULR="" \
    INFLUX_CREDS="" \
    INFLUX_LABELS=""

ENTRYPOINT ["/bin/sh"]
CMD ["/github-influx.sh"]
