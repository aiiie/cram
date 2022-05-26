#!/bin/sh

PROJECT_ROOT="$TESTDIR"/../../..
# Bash doesn't expand aliases by default in non-interactive mode, so
# we enable it manually if the test is run with --shell=/bin/bash.
[ -n "$BASH" ] && shopt -s expand_aliases

# The $PYTHON environment variable should be set when running this test
# from Python.
[ -n "$PYTHON" ] || PYTHON="`which python3`"
[ -n "$PYTHONPATH" ] || PYTHONPATH=${PROJECT_ROOT} && export PYTHONPATH
if [ -n "$COVERAGE" ]; then
  if [ -z "$COVERAGE_FILE" ]; then
    COVERAGE_FILE=${PROJECT_ROOT}/.coverage
    export COVERAGE_FILE
  fi

  alias prysk="`which "$COVERAGE"` run -a --rcfile=${PROJECT_ROOT}/pyproject.toml \
${PROJECT_ROOT}/prysk --shell=$TESTSHELL"
  alias md5="$PYTHON ${PROJECT_ROOT}/scripts/md5.py"
else
  PYTHON="`command -v "$PYTHON" || echo "$PYTHON"`"
  alias prysk="$PYTHON -m prysk --shell=$TESTSHELL"
  alias md5="$PYTHON ${PROJECT_ROOT}/scripts/md5.py"
fi

# Copy in example tests
cp -R ${PROJECT_ROOT}/examples .
find . -name '*.err' -exec rm '{}' \;
