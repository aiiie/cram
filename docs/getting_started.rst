Getting Started
---------------

Installation
++++++++++++

Install `prysk` globally using pip_:

.. code-block:: console

    python -m pip install -U prysk

or install it into the `user site`_:

.. code-block:: console

    python -m pip install -U --user prysk

.. _pip: https://pip.pypa.io/en/stable/
.. _user site: https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-to-the-user-site


Create your first test
++++++++++++++++++++++

#. Create an empty folder for your tests

    .. code-block:: console

        $ mkdir -p tests

#. Change into the test directory

    .. code-block:: console

        $ cd tests

#. Create an empty prysk test file

    .. code-block:: console

        $ touch my_test.t

#. Add the following content to your test file

    .. code-block:: console

        This is a comment

            $ echo "foo bar"

#. If you run the test now you should get a failure

    .. code-block:: console

       $ prysk my_test.t
       !
       --- my_test.t
       +++ my_test.t.err
       @@ -1,3 +1,4 @@
        This is a comment

          $ echo "foo bar"
       +  foo bar

       # Ran 1 tests, 0 skipped, 1 failed.

    In order to define the test assumption you can make use of the
    interactive mode `-i` to get yourself jump started

#. Use the interactive mode to define the initial assumptions

    .. code-block:: console

        $ prysk -i my_first_test.t
        !
        --- my_test.t
        +++ my_test.t.err
        @@ -1,3 +1,4 @@
         This is a comment

           $ echo "foo bar"
        +  foo bar
        Accept this change? [yN]

    Confirm with `y` and check our test file `my_test.t` afterwards.

#. Check if your test file `my_test.t` was updated

    .. code-block:: console

        $ cat my_first_test.t
           $ echo "foo bar"
           foo bar

#. If you run your test again, it should pass now just fine

    .. code-block:: console

        $ prysk -i my_first_test.t
        .
        # Ran 1 tests, 0 skipped, 0 failed.

