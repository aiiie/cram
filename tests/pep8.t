Skip this test if pycodestyle isn't available:

  $ command -v pycodestyle > /dev/null || exit 80

Check that the Python source code style is PEP 8 compliant:

  $ pycodestyle --config="$TESTDIR/.."/setup.cfg --repeat "$TESTDIR/.."
