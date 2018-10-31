#!/usr/bin/env bash

set -e

# install flake 8
#python -m pip install -qqq flake8
python -m pip install -qqq flake8

echo "Run flake8."
echo "$(ls -al ./)"
flake8 --statistics --config=./.flake8
#flake8 --statistics --config=./.flake8 

# build packages
#. $(cd $(dirname $0); pwd)/artifacts.sh

