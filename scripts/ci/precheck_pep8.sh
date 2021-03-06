#!/usr/bin/env bash

set -e

# install flake 8
#python -m pip install -qqq flake8
python -m pip install -qqq flake8

echo "Run flake8."
echo "env variables"
echo $TRAVIS_EVENT_TYPE
echo "$TRAVIS_REPO_SLUG"

flake8 --statistics --config=./.flake8
#flake8 --statistics --config=./.flake8 

# build packages
. $(cd $(dirname $0); pwd)/artifacts.sh

