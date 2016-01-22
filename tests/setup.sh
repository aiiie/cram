#!/bin/sh

# Bash doesn't expand aliases by default in non-interactive mode, so
# we enable it manually if the test is run with --shell=/bin/bash.
[ "$0" != "/bin/bash" ] || shopt -s expand_aliases

# The $PYTHON environment variable should be set when running this test
# from Python.
[ -n "$PYTHON" ] || PYTHON="`which python`"
[ -n "$PYTHONPATH" ] || PYTHONPATH="$TESTDIR/.." && export PYTHONPATH
if [ -n "$COVERAGE" ]; then
  alias cram="`which "$COVERAGE"` run -a $TESTDIR/../scripts/cram --shell=$0"
else
  alias cram="$PYTHON $TESTDIR/../scripts/cram --shell=$0"
fi
command -v md5 > /dev/null || alias md5=md5sum

# Copy in example tests
cp -R "$TESTDIR"/../examples .
find . -name '*.err' -exec rm '{}' \;
