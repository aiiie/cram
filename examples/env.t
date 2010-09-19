Check environment variables:

  $ echo "$LANG"
  C
  $ echo "$LC_ALL"
  C
  $ echo "$LANGUAGE"
  C
  $ echo "$TZ"
  GMT
  $ echo "$CDPATH"
  
  $ echo "$COLUMNS"
  80
  $ echo "$GREP_OPTIONS"
  
  $ echo "$RUNDIR"
  .+
  $ echo "$TESTDIR"
  .+
  $ if [ "$RUNDIR" != "$TESTDIR" ]; then
  >   ls -a ..
  > else
  >   echo .
  >   echo ..
  >   echo env.t-0
  >   echo tmp
  > fi
  .
  ..
  env\.t-.*
  tmp
