#!/bin/sh
. ci/references.sh

set -eu
# Log version to track if the non specified version has changed and is breaking stuff.
flake8 --version

if [ -n "${CHANGED_FILES}" ]; then
    echo "Flake8 testing:"
    echo "${CHANGED_FILES}"
    # Ignore shellcheck for variable without quotes
    # shellcheck disable=SC2086
    flake8 --config ./ci/cfg/flake8.ini ${CHANGED_FILES}
fi

exit 0
