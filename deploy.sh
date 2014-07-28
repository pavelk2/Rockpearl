#!/bin/bash
echo 'Killing gunicorn'
pkill gunicorn
echo 'pulling from repository'
git reset --hard HEAD
git pull
echo 'starting gunicorn '
gunicorn --bind rockpearl.crowdcafe.io:80 rockpearl.wsgi:application
echo 'checking DEBUG'
less rockpearl/settings.py | grep 'DEBUG ='