#!/bin/bash
export SERVER_PORT=8000
export AI_SERVER_ENV=production
export LC_ALL=en_US.UTF-8

# auto start uwsgi
cd /projects/AI_SERVER
pids=$(lsof -i:$SERVER_PORT | awk '{print $2}' | grep -v "PID" | tr -s '\n' ' ')
echo "pids=$pids"
if [[ ! ${pids} ]]; then
  echo "uwsgi-server is not running, begin to start it."
  uwsgi --ini uwsgi.ini
  echo "start uwsgi-server successfully"
else
  echo "uwsgi-server is running"
fi
echo "----------------------------"
