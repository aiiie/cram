Set up prysk alias and example tests:

  $ . "$TESTDIR"/setup.sh

Usage:

  $ prysk -h
  [Uu]sage: prysk \[OPTIONS\] TESTS\.\.\. (re)
  
  [Oo]ptions: (re)
    -h, --help          show this help message and exit
    -V, --version       show version information and exit
    -q, --quiet         don't print diffs
    -v, --verbose       show filenames and test status
    -i, --interactive   interactively merge changed test output
    -d, --debug         write script output directly to the terminal
    -y, --yes           answer yes to all questions
    -n, --no            answer no to all questions
    -E, --preserve-env  don't reset common environment variables
    --keep-tmpdir       keep temporary directories
    --shell=PATH        shell to use for running tests (default: /bin/sh)
    --shell-opts=OPTS   arguments to invoke shell with
    --indent=NUM        number of spaces to use for indentation (default: 2)
    --xunit-file=PATH   path to write xUnit XML output
  $ prysk -V
  Cram CLI testing framework (version 0.8)
  
  Copyright (C) 2010-2021 Brodie Rao <brodie@bitheap.org> and others
  This is free software; see the source for copying conditions. There is NO
  warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  $ prysk
  [Uu]sage: prysk \[OPTIONS\] TESTS\.\.\. (re)
  [2]
  $ prysk -y -n
  options --yes and --no are mutually exclusive
  [2]
  $ prysk non-existent also-not-here
  no such file: non-existent
  [2]
  $ mkdir empty
  $ prysk empty
  no tests found
  [2]
  $ prysk --shell=./badsh
  shell not found: ./badsh
  [2]
