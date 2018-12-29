#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if [ -e $DIR/venv/bin/activate ];then
  . $DIR/venv/bin/activate
fi

# This requote function aims to re-construct the arguments with
# quotes so that we can pass the the quoted string as a single argument when
# they are prozied to the git command.
function requote() {
    local res=""
    for x in "${@}" ; do
        # try to figure out if quoting was required for the $x:
        grep -q "[[:space:]]" <<< "$x" && res="${res} '${x}'" || res="${res} ${x}"
    done
    # remove first space and print:
    sed -e 's/^ //' <<< "${res}"
}


proxy_args=""
cmd=""
cmd_start=0

while [[ $# -gt 0 ]]; do

  if [[ "$1" = "--" ]]; then
     cmd_start=1;
  elif [[ $cmd_start = 1 ]]; then
     break
  else
     proxy_args=$proxy_args $1;
  fi
  shift;

done


python $DIR/role.py --ensure-session $proxy_args

/usr/bin/env $(python $DIR/role.py $proxy_args) $(requote "${@}")
