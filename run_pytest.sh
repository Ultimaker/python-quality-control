#!/bin/sh

set -eu

py3clean .
rm -rf ./.cache
rm -rf ./.pytest_cache
rm -rf ./.mypy_cache
rm -rf ./cov_report
rm -rf ./pstats

echo "#####################   TESTING SUDO COMMAND"
set -x
cat /etc/passwd
echo "#####################"
cat /etc/group
echo "#####################"
whoami
echo "#####################"
groups
echo "#####################"
sudo -l
echo "#####################"
sudo ls /
echo "#####################"
sudo -- dbus-daemon --fork --session --print-address
echo "#####################   DONE"

pytest -c ./ci/cfg/pytest.ini --cov=. --cov-report=html --cov-report=xml --cov-config=./ci/cfg/coverage.ini "${@}" --profile-svg --pstats-dir=./pstats

py3clean .

echo "Getting coverage report"

coverage report

exit 0
