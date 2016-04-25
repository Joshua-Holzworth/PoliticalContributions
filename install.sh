#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

printf "PYTHONPATH=\${PYTHONPATH}:$DIR\n" >> ~/.profile
printf "export PYTHONPATH\n" >> ~/.profile
source ~/.profile

printf "PYTHONPATH=\${PYTHONPATH}:$DIR\n" >> ~/.bash_profile
printf "export PYTHONPATH\n" >> ~/.bash_profile
source ~/.bash_profile
