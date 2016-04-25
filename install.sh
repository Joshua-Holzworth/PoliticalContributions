#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

printf "PYTHONPATH=\${PYTHONPATH}:$DIR/src\n" >> ~/.profile
printf "PYTHONPATH=\${PYTHONPATH}:$DIR/test\n" >> ~/.profile
printf "export PYTHONPATH\n" >> ~/.profile
source ~/.profile

printf "PYTHONPATH=\${PYTHONPATH}:$DIR/src\n" >> ~/.bash_profile
printf "PYTHONPATH=\${PYTHONPATH}:$DIR/test\n" >> ~/.bash_profile
printf "export PYTHONPATH\n" >> ~/.bash_profile
source ~/.bash_profile
