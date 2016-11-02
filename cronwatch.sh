#!/usr/bin/env bash

if [[ -n "$DEBUG" ]]; then 
  set -x
fi

set -o pipefail  # trace ERR through pipes
set -o errtrace  # trace ERR through 'time command' and other functions
set -o nounset   ## set -u : exit the script if you try to use an uninitialised variable
set -o errexit   ## set -e : exit the script if any statement returns a non-true return value

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" # http://stackoverflow.com/questions/59895
cd $DIR

PATH=$HOME/python3/bin:$PATH:$HOME/.local/bin:$HOME/bin

# test the exit status from the status command
set +e
$DIR/monitor.py status > /dev/null
exit=$?
set -e 

# if the exit code is not zero, try to start it up
if ! [[ $exit -eq 0 ]]
  then
    $DIR/monitor.py start
fi
