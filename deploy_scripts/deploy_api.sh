#!/bin/bash

cd /home/ec2-user/FaceYelp-API
git reset --hard
git checkout master
git fetch origin
git pull
pkill -9 -ef "gunicorn"
pip install -r requirements.txt
./bin/run_server.sh 8000
./bin/start_celery_uploader_worker.sh
