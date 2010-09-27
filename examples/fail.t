Wrong output:

  $ echo 1
  1
  $ echo 1
  2
  $ echo 1
  1

Invalid regex:

  $ echo 1
  +++ (re)

Offset regular expression:

  $ printf 'foo\nbar\nbaz\n\n1\nA\n@\n'
  foo
  baz
  
  \d (re)
  [A-Z] (re)
  #
