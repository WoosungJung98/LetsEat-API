#!/bin/bash

NUM_VCPUS=$(grep -c ^processor /proc/cpuinfo)
gunicorn -w $((NUM_VCPUS)) -b "0.0.0.0:$1" "main:create_app()" -D
