#!/bin/sh

set -e

metrics=$(python3 /github-influx.py)
echo "$metrics"

if [ -n "$INFLUX_URL" -a -n "$INFLUX_CREDS" ]; then
  result=$(echo "$metrics" | curl -q -X POST -u $INFLUX_CREDS "$INFLUX_URL/write?db=telegraf&precision=s" --data-binary @-)
  [ -n "$(echo "$result" | jq '.error' 2> /dev/null)" ] && { echo "$result"; exit 1; }
  echo "Successfully sent to $INFLUX_URL"
fi
