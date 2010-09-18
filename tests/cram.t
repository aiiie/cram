  $ cram() {
  >   "$PYTHON" -c 'import sys, cram; sys.exit(cram.main(sys.argv[1:]))' $@
  > }

Usage:

  $ cram -h
  usage: cram [-v|--verbose] [-h|--help] TESTS...
  [1]
  $ cram
  usage: cram [-v|--verbose] [-h|--help] TESTS...
  [1]

Run cram:

  $ cram examples
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

  $ cram -v examples
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
