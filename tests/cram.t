The $PYTHON environment variable should be set when running this test
from Python.

  $ cp -R "$TESTDIR"/../examples .
  $ [ -n "$PYTHON" ] || PYTHON=python
  $ if [ -n "$COVERAGE" ]; then
  >   coverage erase
  >   alias cram="coverage run -a $TESTDIR/../cram.py"
  > else
  >   alias cram="$PYTHON $TESTDIR/../cram.py"
  > fi
  $ command -v md5 > /dev/null || alias md5=md5sum

Usage:

  $ cram -h
  [Uu]sage: cram \[OPTIONS\] TESTS\.\.\. (re)
  
  [Oo]ptions: (re)
    -h, --help         show this help message and exit
    -q, --quiet        don't print diffs
    -v, --verbose      show filenames and test status
    -i, --interactive  interactively merge changed test output
    -y, --yes          answer yes to all questions
    -n, --no           answer no to all questions
    --keep-tmpdir      keep temporary directories
    -E                 don't reset common environment variables
  $ cram
  [Uu]sage: cram \[OPTIONS\] TESTS\.\.\. (re)
  [2]
  $ cram -y -n
  options -y and -n are mutually exclusive
  [2]
  $ cram non-existent also-not-here
  no such file: non-existent
  [2]

Run cram examples:

  $ cram examples examples/fail.t examples/.hidden.t
  .s.!
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
   
     $ printf 'foo\nbar\nbaz\n\n1\nA\n@\n'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  .
  # Ran 5 tests, 1 skipped, 1 failed.
  $ md5 examples/fail.t examples/fail.t.err
  .*\ba36d8e81925296ce794f1a3b35994a68\b.* (re)
  .*\b6aed028cafd917d35ce7db5029e8f559\b.* (re)
  $ rm examples/fail.t.err

Verbose mode:

  $ cram -v examples examples/fail.t examples/.hidden.t
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
   
     $ printf 'foo\nbar\nbaz\n\n1\nA\n@\n'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  examples/test.t: passed
  # Ran 5 tests, 1 skipped, 1 failed.
  $ md5 examples/fail.t examples/fail.t.err
  .*\ba36d8e81925296ce794f1a3b35994a68\b.* (re)
  .*\b6aed028cafd917d35ce7db5029e8f559\b.* (re)
  $ rm examples/fail.t.err

Interactive mode (don't merge):

  $ cram -n -i examples/fail.t
  !
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
   
     $ printf 'foo\nbar\nbaz\n\n1\nA\n@\n'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  Accept this change? [yN] n
  
  # Ran 1 tests, 0 skipped, 1 failed.
  $ md5 examples/fail.t examples/fail.t.err
  .*\ba36d8e81925296ce794f1a3b35994a68\b.* (re)
  .*\b6aed028cafd917d35ce7db5029e8f559\b.* (re)

Interactive mode (merge):

  $ cp examples/fail.t examples/fail.t.orig
  $ cram -y -i examples/fail.t
  !
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
   
     $ printf 'foo\nbar\nbaz\n\n1\nA\n@\n'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  Accept this change? [yN] y
  
  # Ran 1 tests, 0 skipped, 1 failed.
  $ md5 examples/fail.t
  .*\b6aed028cafd917d35ce7db5029e8f559\b.* (re)
  $ mv examples/fail.t.orig examples/fail.t

Verbose interactive mode (answer manually and don't merge):

  $ printf 'bad\nn\n' | cram -v -i examples/fail.t
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
   
     $ printf 'foo\nbar\nbaz\n\n1\nA\n@\n'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  Accept this change? [yN] Accept this change? [yN] # Ran 1 tests, 0 skipped, 1 failed.
  $ md5 examples/fail.t examples/fail.t.err
  .*\ba36d8e81925296ce794f1a3b35994a68\b.* (re)
  .*\b6aed028cafd917d35ce7db5029e8f559\b.* (re)
  $ printf 'bad\n\n' | cram -v -i examples/fail.t
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
   
     $ printf 'foo\nbar\nbaz\n\n1\nA\n@\n'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  Accept this change? [yN] Accept this change? [yN] # Ran 1 tests, 0 skipped, 1 failed.
  $ md5 examples/fail.t examples/fail.t.err
  .*\ba36d8e81925296ce794f1a3b35994a68\b.* (re)
  .*\b6aed028cafd917d35ce7db5029e8f559\b.* (re)

Verbose interactive mode (answer manually and merge):

  $ cp examples/fail.t examples/fail.t.orig
  $ printf 'bad\ny\n' | cram -v -i examples/fail.t
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
   
     $ printf 'foo\nbar\nbaz\n\n1\nA\n@\n'
     foo
  +  bar
     baz
     
     \d (re)
     [A-Z] (re)
  -  #
  +  @
  Accept this change? [yN] Accept this change? [yN] examples/fail.t: merged output
  # Ran 1 tests, 0 skipped, 1 failed.
  $ md5 examples/fail.t
  .*\b6aed028cafd917d35ce7db5029e8f559\b.* (re)
  $ mv examples/fail.t.orig examples/fail.t

Don't sterilize environment:

Note: We can't set the locale to foo because some shells will issue
warnings for invalid locales.

  $ TZ=foo; export TZ
  $ CDPATH=foo; export CDPATH
  $ COLUMNS=4815162342; export COLUMNS
  $ GREP_OPTIONS=foo; export GREP_OPTIONS
  $ cram -E examples/env.t
  !
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
     $ echo "$CRAMTMP"
     .+ (re)
     $ echo "$TESTDIR"
  
  # Ran 1 tests, 0 skipped, 1 failed.
  $ rm examples/env.t.err
