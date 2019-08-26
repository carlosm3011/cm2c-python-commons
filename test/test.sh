#!/bin/bash
# v2, 20151201
# v3, 20190825

# change python interpreter here, if necessary
PYTHON="/usr/bin/env python"
export SRCHOME="$(pwd)"

####
export PYTHONPATH="$SRCHOME/lib:$SRCHOME/bin:$PYTHONPATH"

$PYTHON $*
