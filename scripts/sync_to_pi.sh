#!/usr/bin/env bash

set -euo pipefail


SCRIPTS_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
PROJECT_DIR=$(dirname "$SCRIPTS_DIR")

function usage() {
  echo "$0 host [--include-git]"
  echo ""
  echo "Copy the repository, excluding the venv, .venv, .mypy_cache, and .git directories"
  echo "host: The host to use sync to e.g. 'vis'"
  echo "--include-git: Also copy the .git directory"
}

if [ "$#" -lt 1 ]; then
  usage
  exit 1
fi
EXTRA_EXCLUSIONS=
if [ "$2" != "--include-git" ]; then
  usage
  exit 1
  EXTRA_EXCLUSIONS="--exclude .git"
fi

host="$1"


if which caffeinate &>/dev/null ; then
  CAFFEINATE='caffeinate -i'
else
  CAFFEINATE=
fi

$CAFFEINATE rsync -av \
    --exclude 'venv' \
    --exclude '.venv' \
    --exclude '.mypy_cache' \
    $EXTRA_EXCLUSIONS \
  "$PROJECT_DIR" "${host}:"
