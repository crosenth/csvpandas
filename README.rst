=================================================================
csvpandas: A command line csv toolkit wrapping the Pandas library
=================================================================

csvpandas - A wrapper of the Pandas high performance data analysis library to view and manipulate csv files 

.. contents:: Table of Contents

authors
=======

* Chris Rosenthal

notes
=====

This is strictly an experimental package and potentially full of bugs.  I am still in the process of planning and 
writing up specifications.  The motivation is to take advantage of Python Pandas high performance libraries for 
manipulating csv files on a file system.

dependencies
============

* Python 2.7.x
* setuptools
* Pandas 0.16.2

installation
============

To install csvpandas and python dependencies, run setup.py or pip from the
project directory::

  % cd csvpandas
  % python setup.py install
  # or
  % pip install -U .

If you don't want to install the dependencies (numpy and pandas take a
while to compile), use::

  % pip install --no-deps -U .

Numpy and pandas require many dependencies to compile (and you'll
likely need to compile them because versions in package managers are
typically out of date). Fortunately, these can pretty easily be
installed on Ubuntu 12.04 by running::

  % sudo apt-get build-dep python-numpy python-pandas

unit tests
==========

Unit tests are implemented using the ``unittest`` module in the Python
standard library. The ``tests`` subdirectory is itself a Python
package that imports the local version (ie, the version in the project
directory, not the version installed to the system) of the
package. All unit tests can be run like this::

    % ./testall
    ...........
    ----------------------------------------------------------------------
    Ran 11 tests in 0.059s

    OK

A single unit test can be run by referring to a specific module,
class, or method within the ``tests`` package using dot notation::

    % ./testone -v tests.test_utils

documentation
=============

To build the Sphinx docs::

  (cd docs && make html)

And to publish to GitHub pages::

  ghp-import -p docs/_build/html

(ghp-import and Sphinx are both included in the requirements.txt)


license
=======

Copyright (c) 2015 Chris Rosenthal

Released under the `GPLv3 <http://www.gnu.org/copyleft/gpl.html>`_ License
