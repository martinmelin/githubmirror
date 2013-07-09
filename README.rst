githubmirror
============

A small script to keep a local bare copy of every repo in a Github
organization, for faster cloning and deploys

Install
-------

Download and run::

    $ python setup.py install

Or install from `PyPi`_::

    $ pip install githubmirror


Usage
-----

To initialize a bare repository on your local machine for every repository in
your Github organization::

    $ github-mirror init <organization>

By default, github-mirror will create the repositories in your current working
directory. Override this using the --workdir option.

When your repositories have been initialized, you can now trigger a git fetch
for each repo by running::

    $ github-mirror sync <organization>

To only sync or initialize a single repo, use the --only-repo=<repo> option.

Security
--------

To access the Github API to find your organization's private repositories,
github-mirror asks you for an `API token`_. If you create a personal API token,
it gives the same access to your account as your username and password, but can
be revoked separately.

github-mirror will save your token to a .githubmirror file in your working
directory. Please take care to protect this file from unauthorized access.

.. _API token: https://github.com/settings/applications
.. _PyPI: https://pypi.python.org/pypi/githubmirror
