**Commit Hero** analyzes a repository for commits and awards achievements based
on each author's work.  It works on a number of version control systems thanks
to anyvc_.

.. _anyvc: http://bitbucket.org/RonnyPfannschmidt/anyvc/

Installation
============

Install Commit Hero through setuptools__::

   python setup.py install

.. __: http://packages.python.org/distribute/

It depends on anyvc_ (which is automatically installed by Setuptools) and the
backend for the repository in question, including but not limited to:

* `Dulwich <http://pypi.python.org/pypi/dulwich>`_ for Git
* `mercurial <http://pypi.python.org/pypi/Mercurial>`_ for Mercurial
* `bzr <http://pypi.python.org/pypi/bzr>`_ for Bazaar
* `subvertpy <http://pypi.python.org/pypi/subvertpy>`_ for Subversion

Check `anyvc's Dependencies`__ for a comprehensive and up-to-date list.

.. __: http://pypi.python.org/pypi/anyvc/#dependencies

Run it like so::

   commithero --help

The shipped ``Makefile`` offers to install Commit Hero into a virtual
environment.  See ``make help`` for details.  If you, for example, wish to run
it on your Mercurial repository ``~/myrepo``, use::

   make install-hg run R=~/myrepo


Synopsis
========

Achievements are unlocked when committing to a repository and subsequently
running Commit Hero over it.

Results from previous runs are cached for performance reasons.  Technically, a
`commithero.state.Repository` is pickled to a file called ``.commithero`` (see
``--cache`` to modify its name) and loaded in consecutive passes.  Use
``--nocache`` to skip the cache.

If your committers screw up their settings -- and boy, they do! -- you can
supply a file mapping author names to real identities via ``--pseudonyms``
(defaults to ``.names``).  It is a simple file with the fields *committer* and
*real author* delimited either by a space or, if necessary, by an equality
sign. [1]_  Committer is checked for with the complete originating address (eg.
``John Doe <john@doe.com>``), only the email, and only the username, in that
order.

.. [1] This is compatible with the format used by hgchurn__.  Use your
       repository's ``.hgchurn`` file with the ``--mercurial`` option.
.. __: http://mercurial.selenic.com/wiki/ChurnExtension

By default, only achievements unlocked since the last run are displayed.
Supplying ``--all`` will show all achievements (but still hit the cache so it
is lightning fast);  ``--table`` shows all achievements ordered by author
instead of date unlocked.


Hacking
=======

You can define additional achievements in a very simple manner:  Define a class
derived from `commithero.achievements.Achievement` and implement its
``on_commit`` method which takes an *author* (a string) and a *commit* (a
`anyvc.common.repository.Revision`).  Whenever you return `True` from such a
method the system considers this particular achievement unlocked.  Implementing
``on_change``, which takes two strings *old* and *new* with file contents,
allows you to implement per-file achievements.

The achievement description is automatically retrieved from its docstring and
its name is generated from its class name (eg. a class ``WellDone`` becomes
*Well Done*).  See ``commithero/achievements/`` for examples.

* You are free to set ``name`` on your achievement class if you are unhappy
  with restrictions imposed by Python.
* If you need to generate several achievements from a single class you can
  return a tuple of *title* and *description* on every single invocation.
* See `ProgressiveAchievement` for achievements which have multiple levels.

Achievements are currently limited to one repository and can **not** be shared
among several repositories.  While there is technically no problem with walking
multiple repository histories from one shared state, some achievements assume
they are operating on a single repository for semantic purposes.


See Also
========

* git-achievements_ lets users acquire achievements while using Git.  It
  enables achievements based solely on local actions such as supplying
  ``--help`` to ``git`` which Commit Hero can never do.  Commit Hero is
  targeted to be run post-factum on already-written version histories and
  supports a wide range of version control systems.
* `Python Achievements`_, tentatively tagged *#pychievements*, are a collection
  of achievements invented by the Python community.
* `IT achievements/trophies` are a collection of achievements invented by the
  Something Awful forums.

.. _git-achievements: http://github.com/icefox/git-achievements
.. _Python Achievements: https://docs.google.com/View?id=dfsf8s3r_45388t5rdd
.. _IT achievements/trophies:
   http://forums.somethingawful.com/showthread.php?threadid=3355600
