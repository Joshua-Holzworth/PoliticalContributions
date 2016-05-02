#!/bin/bash
# Must run this script using dot (i.e. . ./install.sh instead of just ./install.sh)
# This is so that the source command on the last line is applied to the parent's shell
# environment instead of just this script's subshell environment

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname $(dirname $CURRENT_DIR))"

printf "PYTHONPATH=\${PYTHONPATH}:$PROJECT_ROOT\n" >> ~/.bash_profile
printf "export PYTHONPATH\n" >> ~/.bash_profile

source ~/.bash_profile
