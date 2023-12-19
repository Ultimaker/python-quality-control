#!/bin/bash
set -eu

SCRIPT_DIR=$(dirname "${0}")
source "${SCRIPT_DIR}/references.sh"

# Log version to track if the non specified version has changed and is breaking stuff.
pylint --version

if [ -n "${CHANGED_FILES}" ]; then
    echo "PyLint testing:"
    echo "${CHANGED_FILES}"
    # Ignore shellcheck for variable without quotes
    # shellcheck disable=SC2086
    pylint --rcfile=./ci/cfg/.pylintrc  ${CHANGED_FILES}
fi

exit 0
