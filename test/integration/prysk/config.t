Set up prysk alias and example tests:

  $ . "$TESTDIR"/setup.sh

Options in .pryskrc:

  $ cat > .pryskrc <<EOF
  > [prysk]
  > yes = True
  > no = 1
  > indent = 4
  > EOF
  $ prysk
  options --yes and --no are mutually exclusive
  [2]
  $ mv .pryskrc config
  $ PRYSKRC=config prysk
  options --yes and --no are mutually exclusive
  [2]
  $ rm config

Invalid option in .pryskrc:

  $ cat > .pryskrc <<EOF
  > [prysk]
  > indent = hmm
  > EOF
  $ prysk
  [Uu]sage: prysk \[OPTIONS\] TESTS\.\.\. (re)
  
  prysk: error: option --indent: invalid integer value: 'hmm'
  [2]
  $ rm .pryskrc
  $ cat > .pryskrc <<EOF
  > [prysk]
  > verbose = hmm
  > EOF
  $ prysk
  [Uu]sage: prysk \[OPTIONS\] TESTS\.\.\. (re)
  
  prysk: error: --verbose: invalid boolean value: 'hmm'
  [2]
  $ rm .pryskrc

Options in an environment variable:

  $ PRYSK='-y -n' prysk
  options --yes and --no are mutually exclusive
  [2]
