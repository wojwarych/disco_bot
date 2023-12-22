#!/usr/bin/env bash
PROC=$(pgrep -f 'python src/main.py')

if [ ! -z "$PROC" ]
then
  kill ${PROC}
fi
