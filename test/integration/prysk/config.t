Set up prysk alias and example tests:

  $ . "$TESTDIR"/setup.sh

Options in .pryskrc:

  $ cat > test.t <<EOF
  >  $ echo
  > EOF

  $ cat > .pryskrc <<EOF
  > [prysk]
  > yes = True
  > no = 1
  > indent = 4
  > EOF
  $ prysk test.t
  options --yes and --no are mutually exclusive
  [2]
  $ mv .pryskrc config
  $ PRYSKRC=config prysk test.t
  options --yes and --no are mutually exclusive
  [2]
  $ rm config

Invalid option in .pryskrc:

  $ cat > test.t <<EOF
  >  $ echo
  > EOF

  $ cat > .pryskrc <<EOF
  > [prysk]
  > indent = hmm
  > EOF
  $ prysk test.t
  [Uu]sage: prysk \[OPTIONS\] TESTS\.\.\. (re)
  
  prysk: error: --indent: invalid integer value: 'hmm'
  [2]
  $ rm .pryskrc
  $ cat > .pryskrc <<EOF
  > [prysk]
  > verbose = hmm
  > EOF
  $ prysk test.t
  [Uu]sage: prysk \[OPTIONS\] TESTS\.\.\. (re)
  
  prysk: error: --verbose: invalid boolean value: 'hmm'
  [2]
  $ rm .pryskrc

Options in an environment variable:

  $ cat > test.t <<EOF
  >  $ echo
  > EOF

  $ PRYSK='-y -n' prysk test.t
  options --yes and --no are mutually exclusive
  [2]
