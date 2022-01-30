Set up prysk alias and example tests:

  $ . "$TESTDIR"/setup.sh


No file provided

  $ python $SCRIPTS/md5.py
  usage: md5.py [-h] FILE [FILE ...]
  md5.py: error: the following arguments are required: FILE
  [2]


Test md5 with a single input file:

  $ cat > input-1.txt <<EOF
  > FOO BAR
  > LOREM IPSUM
  > LOREM IPSUM LOREM IPSUM
  > EOF

  $ python $SCRIPTS/md5.py input-1.txt
  .*\b8832541c7c7fd2e8aed563c8e23a60f7\b.* (re)

Test md5 with multiple input files:

  $ cat > input-2.txt <<EOF
  > FOO BAR
  > LOREM IPSUM LOREM IPSUM
  > EOF

  $ python $SCRIPTS/md5.py input-1.txt input-2.txt input-1.txt
  .*\b8832541c7c7fd2e8aed563c8e23a60f7\b.* (re)
  .*\b06c8eaf05708ec6d207d582a3f9bcc59\b.* (re)
  .*\b8832541c7c7fd2e8aed563c8e23a60f7\b.* (re)
