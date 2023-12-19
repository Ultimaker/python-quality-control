#!/bin/bash
set -eu

# shellcheck disable=SC1091

SCRIPT_DIR=$(dirname "${0}")
source "${SCRIPT_DIR}/references.sh"

# Log version to track if the non specified version has changed and is breaking stuff.
pycodestyle --version

if [ -n "${CHANGED_FILES}" ]; then
    echo "PyCodeStyle testing: "
    echo "${CHANGED_FILES}"
    # Ignore shellcheck for variable without quotes
    # shellcheck disable=SC2086
    pycodestyle --config=./ci/cfg/pycodestyle.ini ${CHANGED_FILES}
fi

exit 0
