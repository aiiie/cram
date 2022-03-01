Set up prysk alias and example tests:

  $ . "$TESTDIR"/setup.sh

  $ COLUMNS=80

Usage:

  $ prysk -h
  [Uu]sage: prysk \[OPTIONS\] TESTS\.\.\. (re)
  
  positional arguments:
    TESTS               Path(s) to the tests to be executed
  
  (optional arguments|options): (re)
    -h, --help          show this help message and exit
    -V, --version       show program's version number and exit
    -q, --quiet         don't print diffs (default: False)
    -v, --verbose       show filenames and test status (default: False)
    -i, --interactive   interactively merge changed test output (default: False)
    -d, --debug         write script output directly to the terminal (default:
                        False)
    -y, --yes           answer yes to all questions (default: False)
    -n, --no            answer no to all questions (default: False)
    -E, --preserve-env  don't reset common environment variables (default:
                        False)
    --keep-tmpdir       keep temporary directories (default: False)
    --shell PATH        shell to use for running tests (default: /bin/sh)
    --shell-opts OPTS   arguments to invoke shell with (default: None)
    --indent NUM        number of spaces to use for indentation (default: 2)
    --xunit-file PATH   path to write xUnit XML output (default: None)


  $ prysk -V
  [0-9]+\.[0-9]+\.[0-9]+ (re)


  $ prysk
  [Uu]sage: prysk \[OPTIONS\] TESTS\.\.\. (re)
  prysk: error: the following arguments are required: TESTS
  [2]
  $ touch nop.t

  $ prysk -y -n not.t
  options --yes and --no are mutually exclusive
  [2]

  $ prysk non-existent also-not-here
  no such file: non-existent
  [2]

  $ mkdir empty

  $ prysk empty
  no tests found
  [2]

  $ prysk --shell=./badsh nop.t
  shell not found: ./badsh
  [2]
