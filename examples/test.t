Simple commands:

  $ echo foo
  foo
  $ printf 'bar\nbaz\n' | cat
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
  foobar.* (re)

Glob:

  $ printf '* \\foobarbaz {10}\n'
  \* \\fo?bar* {10} (glob)

Literal match ending in (re) and (glob):

  $ echo 'foo\Z\Z\Z bar (re)'
  foo\Z\Z\Z bar (re)
  $ echo 'baz??? quux (glob)'
  baz??? quux (glob)

Exit code:

  $ (exit 1)
  [1]

Write to stderr:

  $ echo foo >&2
  foo

No newline:

  $ python -c 'import sys; sys.stdout.write("foo"); sys.stdout.flush()'
  foo%
  $ python -c 'import sys; sys.stdout.write("foo\nbar"); sys.stdout.flush()'
  foo
  bar%
  $ python -c 'import sys; sys.stdout.write("  "); sys.stdout.flush()'
    %
  $ python -c 'import sys; sys.stdout.write("  \n  "); sys.stdout.flush()'
    
    %
  $ echo foo
  foo
