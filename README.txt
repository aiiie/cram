======================
 Cram: It's test time
======================

Cram is a functional testing framework for command line applications
based on Mercurial_'s `unified test format`_.

Here's a snippet from ``cram.t`` in `Cram's own test suite`_::

    The $PYTHON environment variable should be set when running this
    test from Python.

      $ [ -n "$PYTHON" ] || PYTHON=python
      $ if [ -n "$COVERAGE" ]; then
      >   coverage erase
      >   alias cram='coverage run -a cram.py'
      > else
      >   alias cram="$PYTHON cram.py"
      > fi

    Usage:

      $ cram -h
      [Uu]sage: cram \[OPTIONS\] TESTS\.\.\.

      [Oo]ptions:
        -h, --help     show this help message and exit
        -v, --verbose  Show filenames and test status
      $ cram
      [Uu]sage: cram \[OPTIONS\] TESTS\.\.\.
      [1]

The format in a nutshell:

* Cram tests use the ``.t`` file extension.

* Lines beginning with two spaces, a dollar sign, and a space are run
  in the shell.

* Lines beginning with two spaces, a greater than sign, and a space
  allow multi-line commands.

* All other lines beginning with two spaces are considered command
  output.

* Command output in the test is first matched literally with the
  actual output. If it doesn't match, it's then compiled and matched
  as a `Perl-compatible regular expression`_.

* Command output in the test that ends with a percent sign will match
  actual output that doesn't end in a newline.

* Anything else is a comment.

.. _Mercurial: http://mercurial.selenic.com/
.. _unified test format: http://www.selenic.com/blog/?p=663
.. _Cram's own test suite: http://bitbucket.org/brodie/cram/src/tip/tests/cram.t
.. _Perl-compatible regular expression: http://en.wikipedia.org/wiki/Perl_Compatible_Regular_Expressions


Download
--------

* cram-0.2.tar.gz_ (13 KB, requires Python 2.4-2.7 or Python 3.1)

.. _cram-0.2.tar.gz: http://bitheap.org/cram/cram-0.2.tar.gz

Installation
------------

You can use pip_ to install Cram::

    $ sudo pip install cram

Or you can install Cram the old fashioned way::

    $ wget http://bitheap.org/cram/cram-0.2.tar.gz
    $ tar zxvf cram-0.2.tar.gz
    $ cd cram-0.2.tar.gz
    $ sudo python setup.py install

.. _pip: http://pypi.python.org/pypi/pip


Usage
-----

Cram will print a dot for each passing test. If a test fails, a
`unified context diff`_ is printed showing the test's expected output
and the actual output.

For example, if we run cram on `its own example tests`_::

    $ cram examples
    ..
    --- examples/fail.t
    +++ examples/fail.t.out
    @@ -3,11 +3,11 @@
       $ echo 1
       1
       $ echo 1
    -  2
    +  1
       $ echo 1
       1

     Invalid regex:

       $ echo 1
    -  +++
    +  1
    ..

Cram will also write the test with its actual output to
``examples/fail.t.err``.

When you're first writing a test, you might just write the commands
and run the test to see what happens. If you run Cram with ``-i`` or
``--interactive``, you'll be prompted to merge the actual output back
into the test. This makes it easy to quickly prototype new tests.

.. _unified context diff: http://en.wikipedia.org/wiki/Diff#Unified_format
.. _its own example tests: http://bitbucket.org/brodie/cram/src/tip/examples/


Development
-----------

Download the official development repository using Mercurial_::

    hg clone http://bitbucket.org/brodie/cram

Test Cram using Cram::

    make tests

Get a test coverage report using coverage.py_::

    make coverage

Visit Bitbucket_ if you'd like to fork the project, watch for new
changes, or report issues.

.. _Mercurial: http://mercurial.selenic.com/
.. _coverage.py: http://nedbatchelder.com/code/coverage/
.. _Bitbucket: http://bitbucket.org/brodie/cram
