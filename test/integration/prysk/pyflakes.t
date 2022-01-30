Set up prysk alias and example tests:

  $ . "$TESTDIR"/setup.sh

Skip this test if pyflakes isn't available:

  $ command -v pyflakes > /dev/null || exit 80

Check that there are no obvious Python source code errors:

  $ pyflakes ${PROJECT_ROOT}/prysk
