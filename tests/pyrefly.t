Skip this test if pyrefly isn't available:

  $ command -v pyrefly > /dev/null || exit 80

Do basic type checking of the source code:

  $ cd "$TESTDIR/.."
  $ pyrefly check
   INFO Checking project configured at `*/cram/pyproject.toml` (glob)
   INFO 0 errors
