Set up prysk alias and example tests:

  $ . "$TESTDIR"/setup.sh

Make sure md5 is aliased to our python implementation:

  $ md5 -h | head -n 1
  usage: md5.py.* (re)

Test md5 with a single input file:

  $ cat > input-1.txt <<EOF
  > FOO BAR
  > LOREM IPSUM
  > LOREM IPSUM LOREM IPSUM
  > EOF

  $ md5 input-1.txt
  .*\b8832541c7c7fd2e8aed563c8e23a60f7\b.* (re)

Test md5 with multiple input files:

  $ cat > input-2.txt <<EOF
  > FOO BAR
  > LOREM IPSUM LOREM IPSUM
  > EOF

  $ md5 input-1.txt input-2.txt input-1.txt
  .*\b8832541c7c7fd2e8aed563c8e23a60f7\b.* (re)
  .*\b06c8eaf05708ec6d207d582a3f9bcc59\b.* (re)
  .*\b8832541c7c7fd2e8aed563c8e23a60f7\b.* (re)
