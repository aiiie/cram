Skip this test if ruff isn't available:

  $ command -v ruff > /dev/null || exit 80

Run ruff's linters on the source code:

  $ cd "$TESTDIR/.."
  $ ruff check
  All checks passed!
