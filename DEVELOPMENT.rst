.. highlight:: shell

===========
Development
===========

Get Started!
------------

Ready to contribute? Here's how to set up `spend_pi` for local development.

#. Clone the `spend_pi` repo from GitHub::

    $ git clone spend-pi.git

#. Ensure `poetry is installed`_.
#. Install dependencies and start your virtualenv::

    $ poetry install
    $ poetry shell

#. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

#. When you're done making changes, check that your changes pass the
   tests, including testing other Python versions, with tox::

    $ tox

#. Commit your changes and push your branch to GitLab::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

#. Submit a merge request through GitLab

.. _poetry is installed: https://python-poetry.org/docs/

Merge Request Guidelines
-------------------------

Before you submit a merge request, check that it meets these guidelines:

1. The merge request should only include changes relating to one ticket.
2. The merge request should include tests to cover any added changes and
   check that all existing and new tests pass.
3. If the merge request adds functionality, the docs should be updated.
   Put your new functionality into a function with a docstring, and add
   the feature to the list in README.rst.
4. The team should be informed of any impactful changes.

Tips
----

#. To run a subset of tests::

    $ pytest tests.test_spend_pi

Deploying to PyPI
-----------------

For every release:

#. Update HISTORY.rst

#. Update version number (can also be patch or major)::

    bump2version minor

#. Run the static analysis and tests::

    tox

#. Commit the changes::

    git add HISTORY.rst
    git commit -m "Changelog for upcoming release <#.#.#>"

#. Push the commit::

    git push

The CI pipeline will then deploy to PyPI if tests pass.
