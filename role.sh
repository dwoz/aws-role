#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if [ -e $DIR/venv/bin/activate ];then
  . $DIR/venv/bin/activate
fi

python $DIR/role.py --ensure-session

/usr/bin/env $(python $DIR/role.py) ${*}
