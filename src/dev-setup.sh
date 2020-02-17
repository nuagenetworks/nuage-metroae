#!/bin/sh

# This git hook is written to automatically run schema renumbering and example generation script while changing the schema

BASE_DIRECTORY=..

if [[ -d schemas/  ]]; then
    BASE_DIRECTORY=.
fi

pushd $BASE_DIRECTORY

if [[ src/pre-commit ]]; then
  cp src/pre-commit .git/hooks/
fi

popd
