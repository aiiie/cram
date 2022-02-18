Development
-----------

The Repository
+++++++++++++++
Download the official development repository using Git_

.. code-block:: console

    git clone https://github.com/nicoretti/prysk.git

Visit GitHub_ if you'd like to fork the project, watch for new changes, or
report issues.

Dependencies
++++++++++++

In order to run all tests locally you need to have the following tools
installed.

Python
______
* python >= 3.7
* poetry

Shells
______
* dash
* bash
* zsh

If you have these dependencies all setup, just run a

.. code-block:: console

    poetry install


within the root folder of the project. Now you should be good to go!

Nox
++++
Mostly all task you will need to take care of are automated
using nox_. So if you want to run all checks and build
the documentation etc. just run:

.. code-block:: console

    nox

To get a list of all available targets run:

.. code-block:: console

    nox --list

For running a specific target run:

.. code-block:: console

    nox -s <target>


.. _nox: https://nox.thea.codes/en/stable/
.. _Git: http://git-scm.com/
.. _GitHub: https://github.com/nicoretti/prysk
