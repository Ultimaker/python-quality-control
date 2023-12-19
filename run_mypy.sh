#!/bin/bash
set -eu

# shellcheck disable=SC1091

SCRIPT_DIR=$(dirname "${0}")
source "${SCRIPT_DIR}/references.sh"

# Log version to track if the non specified version has changed and is breaking stuff.
mypy -V

if [ -n "${CHANGED_FILES}" ]; then
    echo "Mypy testing for "
    echo "${CHANGED_FILES}"
    # Ignore shellcheck for variable without quotes
    # shellcheck disable=SC2086
    mypy --config-file=./ci/cfg/mypy.ini --follow-imports=skip --cache-dir=/dev/null ${CHANGED_FILES}
fi

exit 0
