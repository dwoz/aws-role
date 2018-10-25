#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if [ -e $DIR/venv/bin/activate ];then
  . $DIR/venv/bin/activate
fi

proxy_args=""
cmd=""
cmd_start=0
while [[ $# -gt 0 ]]; do

  if [[ "$1" = "--" ]]; then
     cmd_start=1;
  elif [[ $cmd_start = 1 ]]; then
     cmd="$cmd $1";
  else
     proxy_args="$proxy_args $1";
  fi
  shift;

done

echo "$proxy_args";
echo "--";
echo "$cmd";

python $DIR/role.py --ensure-session $proxy_args

/usr/bin/env $(python $DIR/role.py $proxy_args) $cmd
