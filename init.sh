#!/bin/sh

export PYTHONPATH="`pwd`/src:$PYTHONPATH"
echo $PYTHONPATH
export PIPENV_VENV_IN_PROJECT=1
pipenv install
pipenv shell
echo `which python` 

echo enviroment created !!

