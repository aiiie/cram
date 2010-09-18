Simple commands:

  $ echo foo
  foo
  $ echo 'bar\nbaz' | cat
  bar
  baz

Multi-line command:

  $ foo() {
  >     echo bar
  > }
  $ foo
  bar

Regular expression:

  $ echo foobarbaz
  foobar.*

Exit code:

  $ false
  [1]

Write to stderr:

  $ echo foo >&2
  foo
