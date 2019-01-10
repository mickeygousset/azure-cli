#!/usr/bin/env bash

set -e

echo 'mickey: start of verify linter'
echo 'mickey: rocks'

#. $(cd $(dirname $0); pwd)/artifacts.sh
. $(cd $(dirname $0); pwd)/artifacts.sh

echo 'mickey: rocks2'

echo 'mickey: share folder:'
echo $share_folder

ls -la $share_folder/build

echo 'Mickey: All Modules'

ALL_MODULES=`find $share_folder/build/ -name "*.whl"`

pip install -e ./tools
[ -d privates ] && pip install -qqq privates/*.whl
pip install $ALL_MODULES

azdev cli-lint --ci
