The $PYTHON environment variable should be set when running this test
from Python.

  $ [ -n "$PYTHON" ] || PYTHON=python
  $ if [ -n "$COVERAGE" ]; then
  >   coverage erase
  >   alias cram='coverage run -a cram.py'
  > else
  >   alias cram="$PYTHON cram.py"
  > fi
  $ command -v md5 || alias md5=md5sum

Usage:

  $ cram -h
  [Uu]sage: cram \[OPTIONS\] TESTS\.\.\.
  
  [Oo]ptions:
    -h, --help     show this help message and exit
    -v, --verbose  Show filenames and test status
    -D DIR         Run tests in DIR
  $ cram
  [Uu]sage: cram \[OPTIONS\] TESTS\.\.\.
  [1]

Run cram examples:

  $ cram -D . examples examples/fail.t examples/.hidden.t
  ..
  \-\-\- .*/examples/fail\.t\s*
  \+\+\+ .*/examples/fail\.t\.err\s*
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
  $ md5 examples/fail.t examples/fail.t.err
  .*\b6ed4b99c2184f1bac5afc144f334a115\b.*
  .*\bb2ad57fc6bcf13972901470979859b78\b.*
  $ rm examples/fail.t.err

Verbose mode:

  $ cram -D . -v examples/fail.t examples examples/.hidden.t
  examples/bare.t: passed
  examples/empty.t: empty
  examples/fail.t: failed
  \-\-\- .*/examples/fail\.t\s*
  \+\+\+ .*/examples/fail\.t\.err\s*
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
  $ md5 examples/fail.t examples/fail.t.err
  .*\b6ed4b99c2184f1bac5afc144f334a115\b.*
  .*\bb2ad57fc6bcf13972901470979859b78\b.*
  $ rm examples/fail.t.err

Use temp dirs:

  $ cram examples
  ..
  \-\-\- .*/examples/fail\.t\s*
  \+\+\+ .*/examples/fail\.t\.err\s*
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

Invalid -D directory:

  $ cram -D foobarbaz examples
  no such directory: foobarbaz
  [2]
  $ mkdir foobarbaz
  $ chmod -x foobarbaz
  $ cram -D foobarbaz xamples
  can't change directory: Permission denied
  [2]
  $ rmdir foobarbaz
