Skip this test if mypy isn't available:

  $ command -v mypy > /dev/null || exit 80

Do basic type checking of the source code:

  $ cd "$TESTDIR/.."
  $ mypy .
  Success: no issues found in * source file* (glob)
