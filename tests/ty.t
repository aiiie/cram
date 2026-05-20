Skip this test if ty isn't available:

  $ command -v ty > /dev/null || exit 80

Do basic type checking of the source code:

  $ cd "$TESTDIR/.."
  $ ty check
  All checks passed!
