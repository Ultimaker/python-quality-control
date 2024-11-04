#!/bin/sh
set -eu

PARENT_BRANCH=${PARENT_BRANCH:-main}
CHANGED_BRANCH_FILES=$(git diff --name-only --diff-filter=d origin/"${PARENT_BRANCH}"...HEAD :^tests | grep -i .py$ | cat )
EXCLUDE_FILE_NAME="linting_excluded_files.txt"

if [ -z "${ONLY_CHECK_STAGED:=""}" ] ; then
    echo "Local + staged + branch changes"
    CHANGED_LOCAL_FILES=$(git diff --name-only --diff-filter=d HEAD :^tests | grep -i .py$ | cat)
else
    echo "Staged + branch changes"
    CHANGED_LOCAL_FILES=$(git diff --name-only --diff-filter=d --staged :^tests | grep -i .py$ | cat)
fi

CHANGED_FILES=$(echo "${CHANGED_BRANCH_FILES}" "${CHANGED_LOCAL_FILES}" | tr ' ' '\n' | sort | uniq)

# Debug: Print changed files before exclusion
echo "Changed files before exclusion:"
echo "${CHANGED_FILES}"

# Remove excluded files from changed files
if [ -f "${EXCLUDE_FILE_NAME}" ]; then
    EXCLUDED_FILES=$(cat "${EXCLUDE_FILE_NAME}")
    # Debug: Print excluded files
    echo "Excluded files:"
    echo "${EXCLUDED_FILES}"
    CHANGED_FILES=$(echo "${CHANGED_FILES}" | grep -vF "${EXCLUDED_FILES}")
fi

# Debug: Print changed files after exclusion
echo "Changed files after exclusion:"
echo "${CHANGED_FILES}"

export PARENT_BRANCH
export CHANGED_FILES