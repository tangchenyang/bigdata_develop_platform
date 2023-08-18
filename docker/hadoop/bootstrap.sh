#!/bin/bash
/etc/init.d/ssh start &
start-all.sh

if [[ $1 == "-d" ]]; then
  while true; do sleep 1000; done
fi
