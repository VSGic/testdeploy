#!/bin/bash

LOCUST_USERS=500
LOCUST_HATCH_RATE=500
LOCUST_DURATION=120s
LOCUST_HOST=http://app:5000

  -f ./locustfile.py \
  --headless \
  -u $LOCUST_USERS \
  -r $LOCUST_HATCH_RATE \
  -t $LOCUST_DURATION \
  --host $LOCUST_HOST
