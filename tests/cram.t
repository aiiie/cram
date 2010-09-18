Run cram:

  $ python -m cram examples
  ..
  --- examples/fail.t 
  +++ examples/fail.t.out 
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

  $ python -m cram -v examples
  examples/bare.t: passed
  examples/empty.t: empty
  examples/fail.t: failed
  --- examples/fail.t 
  +++ examples/fail.t.out 
  @@ -3,6 +3,6 @@
     $ echo 1
     1
     $ echo 1
  -  2
  +  1
     $ echo 1
     1
  examples/test.t: passed
