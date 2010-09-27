The $PYTHON environment variable should be set when running this test
from Python.

  $ [ -n "$PYTHON" ] || PYTHON=python
  $ if [ -n "$COVERAGE" ]; then
  >   coverage erase
  >   alias cram='coverage run -a cram.py'
  > else
  >   alias cram="$PYTHON cram.py"
  > fi
  $ command -v md5 > /dev/null || alias md5=md5sum

Usage:

  $ cram -h
  [Uu]sage: cram \[OPTIONS\] TESTS\.\.\. (re)
  
  [Oo]ptions: (re)
    -h, --help            show this help message and exit
    -v, --verbose         show filenames and test status
    -i, --interactive     interactively merge changed test output
    -y, --yes             answer yes to all questions
    -n, --no              answer no to all questions
    -D DIR, --tmpdir=DIR  run tests in DIR
    --keep-tmpdir         keep temporary directories
    -E                    don't reset common environment variables
  $ cram
  [Uu]sage: cram \[OPTIONS\] TESTS\.\.\. (re)
  [1]
  $ cram -y -n
  options -y and -n are mutually exclusive
  [2]
  $ cram non-existent also-not-here
  no such file: non-existent
  [2]

Run cram examples:

  $ cram -D . examples examples/fail.t examples/.hidden.t
  ...
  \-\-\- .*/examples/fail\.t\s* (re)
  \+\+\+ .*/examples/fail\.t\.err\s* (re)
  @@ -3,21 +3,22 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
   
   Invalid regex:
   
     $ echo 1
  -  +++ (re)
  +  1
   
   Offset regular expression:
   
     $ echo 'foo\nbar\nbaz\n\n1\nA\n@'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  ..
  $ md5 examples/fail.t examples/fail.t.err
  .*\b571651198f015382b002c3ceaafb14c2\b.* (re)
  .*\b89bd872bf755ac3f190cc647be3a6cc7\b.* (re)
  $ rm examples/fail.t.err

Verbose mode:

  $ cram -D . -v examples/fail.t examples examples/.hidden.t
  examples/bare.t: passed
  examples/empty.t: empty
  examples/env.t: passed
  examples/fail.t: failed
  \-\-\- .*/examples/fail\.t\s* (re)
  \+\+\+ .*/examples/fail\.t\.err\s* (re)
  @@ -3,21 +3,22 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
   
   Invalid regex:
   
     $ echo 1
  -  +++ (re)
  +  1
   
   Offset regular expression:
   
     $ echo 'foo\nbar\nbaz\n\n1\nA\n@'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  examples/test.t: passed
  $ md5 examples/fail.t examples/fail.t.err
  .*\b571651198f015382b002c3ceaafb14c2\b.* (re)
  .*\b89bd872bf755ac3f190cc647be3a6cc7\b.* (re)
  $ rm examples/fail.t.err

Interactive mode (don't merge):

  $ cram -n -D . -i examples/fail.t
  
  \-\-\- .*/examples/fail\.t\s* (re)
  \+\+\+ .*/examples/fail\.t\.err\s* (re)
  @@ -3,21 +3,22 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
   
   Invalid regex:
   
     $ echo 1
  -  +++ (re)
  +  1
   
   Offset regular expression:
   
     $ echo 'foo\nbar\nbaz\n\n1\nA\n@'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  Accept this change? [yN] n
  .
  $ md5 examples/fail.t examples/fail.t.err
  .*\b571651198f015382b002c3ceaafb14c2\b.* (re)
  .*\b89bd872bf755ac3f190cc647be3a6cc7\b.* (re)

Interactive mode (merge):

  $ cp examples/fail.t examples/fail.t.orig
  $ cram -y -D . -i examples/fail.t
  
  \-\-\- .*/examples/fail\.t\s* (re)
  \+\+\+ .*/examples/fail\.t\.err\s* (re)
  @@ -3,21 +3,22 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
   
   Invalid regex:
   
     $ echo 1
  -  +++ (re)
  +  1
   
   Offset regular expression:
   
     $ echo 'foo\nbar\nbaz\n\n1\nA\n@'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  Accept this change? [yN] y
  .
  $ md5 examples/fail.t
  .*\b89bd872bf755ac3f190cc647be3a6cc7\b.* (re)
  $ mv examples/fail.t.orig examples/fail.t

Verbose interactive mode (answer manually and don't merge):

  $ printf 'bad\nn\n' | cram -v -D . -i examples/fail.t
  examples/fail.t: failed
  \-\-\- .*/examples/fail\.t\s* (re)
  \+\+\+ .*/examples/fail\.t\.err\s* (re)
  @@ -3,21 +3,22 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
   
   Invalid regex:
   
     $ echo 1
  -  +++ (re)
  +  1
   
   Offset regular expression:
   
     $ echo 'foo\nbar\nbaz\n\n1\nA\n@'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  Accept this change? [yN] Accept this change? [yN] %
  $ md5 examples/fail.t examples/fail.t.err
  .*\b571651198f015382b002c3ceaafb14c2\b.* (re)
  .*\b89bd872bf755ac3f190cc647be3a6cc7\b.* (re)
  $ printf 'bad\n\n' | cram -v -D . -i examples/fail.t
  examples/fail.t: failed
  \-\-\- .*/examples/fail\.t\s* (re)
  \+\+\+ .*/examples/fail\.t\.err\s* (re)
  @@ -3,21 +3,22 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
   
   Invalid regex:
   
     $ echo 1
  -  +++ (re)
  +  1
   
   Offset regular expression:
   
     $ echo 'foo\nbar\nbaz\n\n1\nA\n@'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  Accept this change? [yN] Accept this change? [yN] %
  $ md5 examples/fail.t examples/fail.t.err
  .*\b571651198f015382b002c3ceaafb14c2\b.* (re)
  .*\b89bd872bf755ac3f190cc647be3a6cc7\b.* (re)

Verbose interactive mode (answer manually and merge):

  $ cp examples/fail.t examples/fail.t.orig
  $ printf 'bad\ny\n' | cram -v -D . -i examples/fail.t
  examples/fail.t: failed
  \-\-\- .*/examples/fail\.t\s* (re)
  \+\+\+ .*/examples/fail\.t\.err\s* (re)
  @@ -3,21 +3,22 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
   
   Invalid regex:
   
     $ echo 1
  -  +++ (re)
  +  1
   
   Offset regular expression:
   
     $ echo 'foo\nbar\nbaz\n\n1\nA\n@'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  Accept this change? [yN] Accept this change? [yN] examples/fail.t: merged output
  $ md5 examples/fail.t
  .*\b89bd872bf755ac3f190cc647be3a6cc7\b.* (re)
  $ mv examples/fail.t.orig examples/fail.t

Use temp dirs:

  $ cram examples
  ...
  \-\-\- .*/examples/fail\.t\s* (re)
  \+\+\+ .*/examples/fail\.t\.err\s* (re)
  @@ -3,21 +3,22 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
   
   Invalid regex:
   
     $ echo 1
  -  +++ (re)
  +  1
   
   Offset regular expression:
   
     $ echo 'foo\nbar\nbaz\n\n1\nA\n@'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  ..

Invalid -D directory:

  $ cram -D foobarbaz examples
  no such directory: foobarbaz
  [2]
  $ mkdir foobarbaz
  $ chmod -x foobarbaz
  $ cram -D foobarbaz examples
  can't change directory: Permission denied
  [2]
  $ rmdir foobarbaz

Don't sterilize environment:

Note: We can't set the locale to foo because some shells will issue
warnings for invalid locales.

  $ TZ=foo; export TZ
  $ CDPATH=foo; export CDPATH
  $ COLUMNS=4815162342; export COLUMNS
  $ GREP_OPTIONS=foo; export GREP_OPTIONS
  $ cram -E examples/env.t
  
  \-\-\- .*/examples/env\.t\s* (re)
  \+\+\+ .*/examples/env\.t\.err\s* (re)
  @@ -7,13 +7,13 @@
     $ echo "$LANGUAGE"
     C
     $ echo "$TZ"
  -  GMT
  +  foo
     $ echo "$CDPATH"
  -  
  +  foo
     $ echo "$COLUMNS"
  -  80
  +  4815162342
     $ echo "$GREP_OPTIONS"
  -  
  +  foo
     $ echo "$RUNDIR"
     .+ (re)
     $ echo "$TESTDIR"
  .

Cleanup:

  $ rm examples/env.t.err
  $ rm examples/fail.t.err
