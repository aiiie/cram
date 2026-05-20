Skip this test if basedpyright isn't available:

  $ command -v basedpyright > /dev/null || exit 80

Do strict type checking of the source code:

  $ cd "$TESTDIR/.."
  $ basedpyright
  0 errors, 0 warnings, 0 notes
