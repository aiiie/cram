Set up prysk alias and example tests:

  $ . "$TESTDIR"/setup.sh

Run prysk examples:

  $ prysk -q examples examples/fail.t
  .s.!.s.
  # Ran 7 tests, 2 skipped, 1 failed.
  [1]
  $ md5 examples/fail.t examples/fail.t.err
  .*\b0f598c2b7b8ca5bcb8880e492ff6b452\b.* (re)
  .*\b7a23dfa85773c77648f619ad0f9df554\b.* (re)
  $ rm examples/fail.t.err

Run examples with bash:

  $ prysk --shell=/bin/bash -q examples examples/fail.t
  .s.!.s.
  # Ran 7 tests, 2 skipped, 1 failed.
  [1]
  $ md5 examples/fail.t examples/fail.t.err
  .*\b0f598c2b7b8ca5bcb8880e492ff6b452\b.* (re)
  .*\b7a23dfa85773c77648f619ad0f9df554\b.* (re)
  $ rm examples/fail.t.err

Verbose mode:

  $ prysk -q -v examples examples/fail.t
  examples/bare.t: passed
  examples/empty.t: empty
  examples/env.t: passed
  examples/fail.t: failed
  examples/missingeol.t: passed
  examples/skip.t: skipped
  examples/test.t: passed
  # Ran 7 tests, 2 skipped, 1 failed.
  [1]
  $ md5 examples/fail.t examples/fail.t.err
  .*\b0f598c2b7b8ca5bcb8880e492ff6b452\b.* (re)
  .*\b7a23dfa85773c77648f619ad0f9df554\b.* (re)
  $ rm examples/fail.t.err

Test that a fixed .err file is deleted:

  $ echo "  $ echo 1" > fixed.t
  $ prysk fixed.t
  !
  --- fixed.t
  +++ fixed.t.err
  @@ -1,1 +1,2 @@
     $ echo 1
  +  1
  
  # Ran 1 tests, 0 skipped, 1 failed.
  [1]
  $ cp fixed.t.err fixed.t
  $ prysk fixed.t
  .
  # Ran 1 tests, 0 skipped, 0 failed.
  $ test \! -f fixed.t.err
  $ rm fixed.t

Don't sterilize environment:

  $ TZ=foo; export TZ
  $ CDPATH=foo; export CDPATH
  $ GREP_OPTIONS=foo; export GREP_OPTIONS
  $ prysk -E examples/env.t
  !
  \-\-\- examples/env\.t\s* (re)
  \+\+\+ examples/env\.t\.err\s* (re)
  @@ -7,11 +7,11 @@
     $ echo "$LANGUAGE"
     C
     $ echo "$TZ"
  -  GMT
  +  foo
     $ echo "$CDPATH"
  -  
  +  foo
     $ echo "$GREP_OPTIONS"
  -  
  +  foo
     $ echo "$PRYSK_TEMP"
     .+ (re)
     $ echo "$TESTDIR"
  
  # Ran 1 tests, 0 skipped, 1 failed.
  [1]
  $ rm examples/env.t.err

Note: We can't set the locale to foo because some shells will issue
warnings for invalid locales.

Test --keep-tmpdir:

  $ prysk -q --keep-tmpdir examples/test.t | while read line; do
  >   echo "$line" 1>&2
  >   msg=`echo "$line" | cut -d ' ' -f 1-4`
  >   if [ "$msg" = '# Kept temporary directory:' ]; then
  >     echo "$line" | cut -d ' ' -f 5
  >   fi
  > done > keeptmp
  .
  # Ran 1 tests, 0 skipped, 0 failed.
  # Kept temporary directory: */prysk-tests-* (glob)
  $ ls "`cat keeptmp`" | sort
  test.t
  tmp

Custom indentation:

  $ cat > indent.t <<EOF
  > Indented by 4 spaces:
  > 
  >     $ echo foo
  >     foo
  > 
  > Not part of the test:
  > 
  >   $ echo foo
  >   bar
  > EOF
  $ prysk --indent=4 indent.t
  .
  # Ran 1 tests, 0 skipped, 0 failed.

Test running tests with the same filename in different directories:

  $ mkdir subdir1 subdir2
  $ cat > subdir1/test.t <<EOF
  >   $ echo 1
  > EOF
  $ cat > subdir2/test.t <<EOF
  >   $ echo 2
  > EOF
  $ prysk subdir1 subdir2
  !
  --- subdir1/test.t
  +++ subdir1/test.t.err
  @@ -1,1 +1,2 @@
     $ echo 1
  +  1
  !
  --- subdir2/test.t
  +++ subdir2/test.t.err
  @@ -1,1 +1,2 @@
     $ echo 2
  +  2
  
  # Ran 2 tests, 0 skipped, 2 failed.
  [1]
