#!/bin/bash

NUM_CORES=$(grep ^cpu\\scores /proc/cpuinfo | uniq |  awk '{print $4}')
gunicorn -w $((NUM_CORES * 2 + 1)) -b "0.0.0.0:$1" "main:create_app()" -D
