======================
 Cram: It's test time
======================

Cram is a functional testing framework for command line applications
based on Mercurial_'s `unified test format`_.

Cram tests look like snippets of interactive shell sessions. Cram runs
each command and compares the command output in the test with the
command's actual output.

Here's a snippet from `Cram's own test suite`_::

    The $PYTHON environment variable should be set when running this
    test from Python.

      $ [ -n "$PYTHON" ] || PYTHON="`which python`"
      $ if [ -n "$COVERAGE" ]; then
      >   coverage erase
      >   alias cram="`which coverage` run -a $TESTDIR/../cram.py"
      > else
      >   alias cram="$PYTHON $TESTDIR/../cram.py"
      > fi
      $ command -v md5 > /dev/null || alias md5=md5sum

    Usage:

      $ cram -h
      [Uu]sage: cram \[OPTIONS\] TESTS\.\.\. (re)

      [Oo]ptions: (re)
        -h, --help         show this help message and exit
        -V, --version      show version information and exit
        -q, --quiet        don't print diffs
        -v, --verbose      show filenames and test status
        -i, --interactive  interactively merge changed test output
        -y, --yes          answer yes to all questions
        -n, --no           answer no to all questions
        --keep-tmpdir      keep temporary directories
        -E                 don't reset common environment variables

The format in a nutshell:

* Cram tests use the ``.t`` file extension.

* Lines beginning with two spaces, a dollar sign, and a space are run
  in the shell.

* Lines beginning with two spaces, a greater than sign, and a space
  allow multi-line commands.

* All other lines beginning with two spaces are considered command
  output.

* Output lines ending with a space and the keyword ``(re)`` are
  matched as `Perl-compatible regular expressions`_.

* Lines ending with a space and the keyword ``(glob)`` are matched
  with a glob-like syntax. The only special characters supported are
  ``*`` and ``?``. Both characters can be escaped using ``\``, and the
  backslash can be escaped itself.

* Output lines ending with either of the above keywords are always
  first matched literally with actual command output.

* Lines ending with a space and the keyword ``(no-eol)`` will match
  actual output that doesn't end in a newline.

* Actual output containing unprintable characters are escaped and
  suffixed with a space and the keyword ``(esc)``. Lines matching
  unprintable output must also contain the keyword.

* Anything else is a comment.

.. _Mercurial: http://mercurial.selenic.com/
.. _unified test format: http://www.selenic.com/blog/?p=663
.. _Cram's own test suite: http://bitbucket.org/brodie/cram/src/tip/tests/cram.t
.. _Perl-compatible regular expressions: http://en.wikipedia.org/wiki/Perl_Compatible_Regular_Expressions


Download
--------

* cram-0.5.tar.gz_ (22 KB, requires Python 2.4-2.7 or Python 3.1-3.2)

.. _cram-0.5.tar.gz: http://bitheap.org/cram/cram-0.5.tar.gz

Installation
------------

You can use pip_ to install Cram::

    $ pip install cram

Or you can install Cram the old fashioned way::

    $ wget http://bitheap.org/cram/cram-0.5.tar.gz
    $ tar zxvf cram-0.5.tar.gz
    $ cd cram-0.5.tar.gz
    $ python setup.py install

.. _pip: http://pypi.python.org/pypi/pip


Usage
-----

Cram will print a dot for each passing test. If a test fails, a
`unified context diff`_ is printed showing the test's expected output
and the actual output. Skipped tests (empty tests and tests that exit
with return code ``80``) are marked with ``s`` instead of a dot.

For example, if we run Cram on `its own example tests`_::

    .s.!
    --- /home/brodie/src/cram/examples/fail.t
    +++ /home/brodie/src/cram/examples/fail.t.err
    @@ -3,21 +3,22 @@
       $ echo 1
       1
       $ echo 1
    -  2
    +  1
       $ echo 1
       1

     Invalid regex:

       $ echo 1
    -  +++ (re)
    +  1

     Offset regular expression:

       $ printf 'foo\nbar\nbaz\n\n1\nA\n@\n'
       foo
    +  bar
       baz

       \d (re)
       [A-Z] (re)
    -  #
    +  @
    s.
    # Ran 6 tests, 2 skipped, 1 failed.

Cram will also write the test with its actual output to
``examples/fail.t.err``.

When you're first writing a test, you might just write the commands
and run the test to see what happens. If you run Cram with ``-i`` or
``--interactive``, you'll be prompted to merge the actual output back
into the test. This makes it easy to quickly prototype new tests.

Note that the following environment variables are reset before tests
are run:

* ``TMPDIR``, ``TEMP``, and ``TMP`` are set to the test runner's
  ``tmp`` directory.

* ``LANG``, ``LC_ALL``, and ``LANGUAGE`` are set to ``C``.

* ``TZ`` is set to ``GMT``.

* ``COLUMNS`` is set to ``80``.

* ``CDPATH`` and ``GREP_OPTIONS`` are set to an empty string.

Cram also provides the following environment variables to tests:

* ``CRAMTMP``, set to the test runner's temporary directory.

* ``TESTDIR``, set to the directory containing the test file.

.. _unified context diff: http://en.wikipedia.org/wiki/Diff#Unified_format
.. _its own example tests: http://bitbucket.org/brodie/cram/src/tip/examples/


News
----

Version 0.5 (Jan. 8, 2011)
``````````````````````````
* **The test format has changed:** Matching output not ending in a
    newline now requires the ``(no-eol)`` keyword instead of ending
    the line in ``%``.

* Matching output containing unprintable characters now requires the
  ``(esc)`` keyword. Real output containing unprintable characters
  will automatically receive ``(esc)``.

* If an expected line matches its real output line exactly, special
  matching like ``(re)`` or ``(glob)`` will be ignored.

* Regular expressions ending in a trailing backslash are now
  considered invalid.

* Added an ``--indent`` option for changing the default amount of
  indentation required to specify commands and output.

* Added support for specifying command line options in the ``CRAM``
  environment variable.

* The ``--quiet`` and ``--verbose`` options can now be used together.

* When running Cram under Python 3, Unicode-specific line break
  characters will no longer be parsed as newlines.

* Tests are no longer required to end in a trailing newline.


Version 0.4 (Sep. 28, 2010)
```````````````````````````
* **The test format has changed:** Output lines containing regular
  expressions must now end in ``(re)`` or they'll be matched
  literally. Lines ending with keywords are matched literally first,
  however.

* Regular expressions are now matched from beginning to end. In other
  words ``\d (re)`` is matched as ``^\d$``.

* In addition to ``(re)``, ``(glob)`` has been added. It supports
  ``*``, ``?``, and escaping both characters (and backslashes) using
  ``\``.

* **Environment settings have changed:** The ``-D`` flag has been
  removed, ``$TESTDIR`` is now set to the directory containing the
  ``.t`` file, and ``$CRAMTMP`` is set to the test runner's temporary
  directory.

* ``-i``/``--interactive`` now requires ``patch(1)``. Instead of
  ``.err`` files replacing ``.t`` files during merges, diffs are
  applied using ``patch(1)``. This prevents matching regular
  expressions and globs from getting clobbered.

* Previous ``.err`` files are now removed when tests pass.

* Cram now exits with return code ``1`` if any tests failed.

* If a test exits with return code ``80``, it's considered a skipped a
  test. This is useful for intentionally disabling tests when they
  only work on certain platforms or in certain settings.

* The number of tests, the number of skipped tests, and the number of
  failed tests are now printed after all tests are finished.

* Added ``-q``/``--quiet`` to suppress diff output.

* Added `contrib/cram.vim`_ syntax file for Vim. Contributed by `Steve
  Losh`_.

.. _contrib/cram.vim: http://bitbucket.org/brodie/cram/src/tip/contrib/cram.vim
.. _Steve Losh: http://stevelosh.com/

Version 0.3 (Sep. 20, 2010)
```````````````````````````
* Implemented resetting of common environment variables. This behavior
  can be disabled using the ``-E`` flag.

* Changed the test runner to first make its own overall random
  temporary directory, make ``tmp`` inside of it and set ``TMPDIR``,
  etc. to its path, and run each test with a random temporary working
  directory inside of that.

* Added ``--keep-tmpdir``. Temporary directories are named by test
  filename (along with a random string).

* Added ``-i``/``--interactive`` to merge actual output back to into
  tests interactively.

* Added ability to match command output not ending in a newline by
  suffixing output in the test with ``%``.

Version 0.2 (Sep. 19, 2010)
```````````````````````````
* Changed the test runner to run tests with a random temporary working
  directory.

Version 0.1 (Sep. 19, 2010)
```````````````````````````
* Initial release.


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
