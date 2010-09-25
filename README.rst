``commithero`` analyzes a repository for commits and awards achievements based on
each author's work.

Synopsis
========

It caches results from previous runs in the repository for performance reasons.
A `commithero.state.Repository` is pickled to a file called ``.commithero``
(see ``--cache`` to modify its name) and loaded in consecutive passes.  Use
``--nocache`` to skip the cache.

If your committers screw up their settings -- and boy, they do! -- you can
supply a file mapping author names to real identities via ``--pseudonyms``
(defaults to ``.names``).  It is a simple two-column CSV file with the fields
*committer* and *real author*.

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
method the system considers this particular achievement unlocked.

The achievement description is automatically retrieved from its docstring and
its name is generated from its class name (eg. a class ``WellDone`` becomes
*Well Done*).  See ``commithero/achievements/`` for examples.

* You are free to set ``name`` on your achievement class if you are unhappy
  with restrictions imposed by Python.
* If you need to generate several achievements from a single class you can
  return a tuple of *title* and *description*.
* See `ProgressiveAchievement` for achievements which have multiple levels.
