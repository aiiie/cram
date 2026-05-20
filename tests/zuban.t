Skip this test if zuban isn't available:

  $ command -v zuban > /dev/null || exit 80

Do basic type checking of the source code:

  $ cd "$TESTDIR/.."
  $ zuban check
  Success: no issues found in * source files (glob)
