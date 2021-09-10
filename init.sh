#!/bin/sh

export PYTHONPATH="`pwd`/src:$PYTHONPATH"
echo $PYTHONPATH
export PIPENV_VENV_IN_PROJECT=1
pipenv install
pipenv shell
echo `which python` 

echo enviroment created !!

echo building c++ booster
c++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup $(python3 -m pybind11 --includes) src/boosters/genetic_algorithms.cpp -o src/ga/genetic_algorithms$(python3-config --extension-suffix)

echo build!
