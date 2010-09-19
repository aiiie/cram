The $PYTHON environment variable must be set to run these tests
manually.

  $ [ -z "$PYTHON" ] && PYTHON=python || true
  $ if [ -n "$COVERAGE" ]; then
  >   coverage erase
  >   alias cram='coverage run -a cram.py'
  > else
  >   alias cram="$PYTHON cram.py"
  > fi

Usage:

  $ cram -h
  [Uu]sage: cram \[OPTIONS\] TESTS\.\.\.
  
  [Oo]ptions:
    -h, --help     show this help message and exit
    -v, --verbose  Show filenames and test status
  $ cram
  [Uu]sage: cram \[OPTIONS\] TESTS\.\.\.
  [1]

Run cram exmples:

  $ cram examples examples/fail.t examples/.hidden.t
  ..
  \-\-\- examples/fail\.t\s*
  \+\+\+ examples/fail\.t\.out\s*
  @@ -3,11 +3,11 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
   
   Invalid regex:
   
     $ echo 1
  -  +++
  +  1
  ..

Verbose mode:

  $ cram -v examples/fail.t examples examples/.hidden.t
  examples/bare.t: passed
  examples/empty.t: empty
  examples/fail.t: failed
  \-\-\- examples/fail\.t\s*
  \+\+\+ examples/fail\.t\.out\s*
  @@ -3,11 +3,11 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
   
   Invalid regex:
   
     $ echo 1
  -  +++
  +  1
  examples/test.t: passed
