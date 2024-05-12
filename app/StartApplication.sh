#!/bin/bash
echo "Starting service in the background ."
if [[ ! -d "logs" ]]; then
    mkdir logs
fi
uwsgi --http 0.0.0.0:5000 --module launcher:app  &
if [[ $? -ne 0 ]]; then
    echo "Server failed to start"
fi
echo "Server started successfully"
echo "$@"
tail -f /dev/null