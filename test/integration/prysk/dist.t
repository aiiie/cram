Set up prysk alias and example tests:

  $ . "$TESTDIR"/setup.sh

Skip this test if check-manifest isn't available:

  $ command -v check-manifest > /dev/null || exit 80

Confirm that "make dist" isn't going to miss any files:

  $ check-manifest ${PROJECT_ROOT}
  lists of files in version control and sdist match
