#!/bin/bash

source venv3/bin/activate
pylint --rcfile=pylintrc *.py
pycco *.py
#python3 test_*.py
python3 -m unittest discover .
