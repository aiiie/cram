The $PYTHON environment variable must be set to run these tests
manually.

  $ [ -z "$PYTHON" ] && PYTHON=python || true
  $ cram() {
  >   "$PYTHON" -c 'import sys, cram; sys.exit(cram.main(sys.argv[1:]))' $@
  > }

Usage:

  $ cram -h
  Usage: cram [OPTIONS] TESTS...
  
  Options:
    -h, --help     show this help message and exit
    -v, --verbose  Show filenames and test status
  $ cram
  Usage: cram [OPTIONS] TESTS...
  [1]

Run cram exmples:

  $ cram examples examples/.hidden.t examples/fail.t
  ..
  \-\-\- examples/fail\.t\s*
  \+\+\+ examples/fail\.t\.out\s*
  @@ -3,6 +3,6 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
  ..

Verbose mode:

  $ cram -v examples examples/.hidden.t examples/fail.t
  examples/bare.t: passed
  examples/empty.t: empty
  examples/fail.t: failed
  \-\-\- examples/fail\.t\s*
  \+\+\+ examples/fail\.t\.out\s*
  @@ -3,6 +3,6 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
  examples/test.t: passed
