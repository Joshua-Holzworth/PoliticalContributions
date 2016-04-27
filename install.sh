#!/bin/bash
# Must run this script using dot (i.e. . ./install.sh instead of just ./install.sh)
# This is so that the source command on the last line is applied to the parent's shell
# environment instead of just this script's subshell environment

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

printf "PYTHONPATH=\${PYTHONPATH}:$DIR\n" >> ~/.bash_profile
printf "export PYTHONPATH\n" >> ~/.bash_profile

source ~/.bash_profile
