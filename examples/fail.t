Wrong output and bad regexes:

  $ echo 1
  2
  $ printf '1\nfoo\n1\n'
  +++ (re)
  foo\ (re)
   (re)

Offset regular expression:

  $ printf 'foo\n\n1\n'
  
  \d (re)
