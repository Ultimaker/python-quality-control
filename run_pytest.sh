#!/bin/bash

set -eu

SCRIPT_DIR=$(dirname "${0}")

export USE_DUMMY_DBUS=true
export PYTHONPATH=:../dbus-interface-lib:../libpalantir:../libPalantir:../charon:../libCharon:../libsmeagol:../libSmeagol:../marvin-service/src:../libLogger:../ultiLib/libs

py3clean .
rm -rf ./.cache
rm -rf ./.pytest_cache
rm -rf ./.mypy_cache
rm -rf ./cov_report
rm -rf ./pstats

pytest -c "./${SCRIPT_DIR}/cfg/pytest.ini" --cov=. --cov-report=html --cov-report=xml --cov-config=./ci/cfg/coverage.ini "${@}" --profile-svg --pstats-dir=./pstats

py3clean .

echo "Getting coverage report"

coverage report

exit 0
