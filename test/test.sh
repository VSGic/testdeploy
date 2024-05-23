#!/bin/bash

LOCUST_USERS=1000
LOCUST_HATCH_RATE=1000
LOCUST_DURATION=180s
LOCUST_HOST=http://192.168.1.67:5000
LOCUST_RESULTS=/mnt/locust/locust_output

docker run -v ./:/mnt/locust/ locustio/locust \
  -f /mnt/locust/locustfile.py \
  --headless \
  -u $LOCUST_USERS \
  -r $LOCUST_HATCH_RATE \
  -t $LOCUST_DURATION \
  --csv $LOCUST_RESULTS \
  --host $LOCUST_HOST
