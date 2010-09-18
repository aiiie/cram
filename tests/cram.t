Note: Never return cram without any arguments in this test. You'll
most likely send it into an infinte loop as the test tries to run
itself.

  $ cram() {
  >   "$PYTHON" -m cram $@
  > }

Usage:

  $ cram -h
  usage: cram [-v|--verbose] [-h|--help] [TESTS]
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
