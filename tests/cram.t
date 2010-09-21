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
    -h, --help            show this help message and exit
    -v, --verbose         show filenames and test status
    -i, --interactive     interactively merge changed test output
    -y, --yes             answer yes to all questions
    -n, --no              answer no to all questions
    -D DIR, --tmpdir=DIR  run tests in DIR
    --keep-tmpdir         keep temporary directories
    -E                    don't reset common environment variables
  $ cram
  [Uu]sage: cram \[OPTIONS\] TESTS\.\.\.
  [1]
  $ cram -y -n
  options -y and -n are mutually exclusive
  [2]

Run cram examples:

  $ cram -D . examples examples/fail.t examples/.hidden.t
  ...
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
  examples/env.t: passed
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

Interactive mode (don't merge):

  $ cram -n -D . -i examples/fail.t
  
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
  Accept this change? [yN] n
  .
  $ md5 examples/fail.t examples/fail.t.err
  .*\b6ed4b99c2184f1bac5afc144f334a115\b.*
  .*\bb2ad57fc6bcf13972901470979859b78\b.*

Interactive mode (merge):

  $ cp examples/fail.t examples/fail.t.orig
  $ cram -y -D . -i examples/fail.t
  
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
  Accept this change? [yN] y
  .
  $ md5 examples/fail.t
  .*\bb2ad57fc6bcf13972901470979859b78\b.*
  $ mv examples/fail.t.orig examples/fail.t

Verbose interactive mode (answer manually and don't merge):

  $ echo 'bad\nn' | cram -v -D . -i examples/fail.t
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
  Accept this change? [yN] Accept this change? [yN] Accept this change? [yN] %
  $ md5 examples/fail.t examples/fail.t.err
  .*\b6ed4b99c2184f1bac5afc144f334a115\b.*
  .*\bb2ad57fc6bcf13972901470979859b78\b.*

Verbose interactive mode (answer manually and merge):

  $ cp examples/fail.t examples/fail.t.orig
  $ echo 'bad\ny' | cram -v -D . -i examples/fail.t
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
  Accept this change? [yN] Accept this change? [yN] examples/fail.t: merged output
  $ md5 examples/fail.t
  .*\bb2ad57fc6bcf13972901470979859b78\b.*
  $ mv examples/fail.t.orig examples/fail.t

Use temp dirs:

  $ cram examples
  ...
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
  $ cram -D foobarbaz examples
  can't change directory: Permission denied
  [2]
  $ rmdir foobarbaz

Don't sterilize environment:

  $ LANG=foo; export LANG
  $ LC_ALL=foo; export LC_ALL
  $ LANGUAGE=foo; export LANGUAGE
  $ TZ=foo; export TZ
  $ CDPATH=foo; export CDPATH
  $ COLUMNS=4815162342; export COLUMNS
  $ GREP_OPTIONS=foo; export GREP_OPTIONS
  $ cram -E examples/env.t
  
  \-\-\- .*/examples/env\.t\s*
  \+\+\+ .*/examples/env\.t\.err\s*
  @@ -1,19 +1,19 @@
   Check environment variables:
   
     $ echo "$LANG"
  -  C
  +  foo
     $ echo "$LC_ALL"
  -  C
  +  foo
     $ echo "$LANGUAGE"
  -  C
  +  foo
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
     .+
     $ echo "$TESTDIR"
  .

Cleanup:

  $ rm examples/env.t.err
  $ rm examples/fail.t.err
