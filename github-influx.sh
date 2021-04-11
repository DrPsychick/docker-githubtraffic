#!/bin/sh

metrics=$(python3 /github-influx.py)
echo "$metrics"

if [ -n "$INFLUX_URL" -a -n "$INFLUX_CREDS" ]; then
  echo "$metrics" | curl -X POST -u $INFLUX_CREDS "$INFLUX_URL/write?db=telegraf&precision=s" --data-binary @- || exit 1
  echo "Successfully sent to $INFLUX_URL"
fi
