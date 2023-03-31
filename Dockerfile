ARG PYTHON_VERSION=alpine3.17
FROM python:$PYTHON_VERSION AS builder

RUN apk --no-cache add curl gcc musl-dev libffi-dev make jq

RUN addgroup -S python && \
    adduser -S python -G python

USER python
COPY requirements.yml /home/python
RUN export PATH=$PATH:/home/python/.local/bin \
    && pip3 install -U pip \
    && pip3 install --requirement /home/python/requirements.yml

USER root
RUN apk --purge del gcc musl-dev libffi-dev make

FROM scratch
COPY --from=builder / /
COPY github-influx.* /
RUN chmod +x /github-influx.sh

USER python
WORKDIR /home/python
ENV GITHUB_TOKEN="" \
    GITHUB_DAYS="3" \
    INFLUX_ULR="" \
    INFLUX_CREDS="" \
    INFLUX_LABELS=""

ENTRYPOINT ["/bin/sh"]
CMD ["/github-influx.sh"]
