``commithero`` analyzes a repository for commits and awards achievements based on
each author's work.

It caches results from previous runs in the repository for performance reasons.
A `Repository` is pickled to a file called ``.commithero`` (see ``-c`` to
modify its name) and loaded in consecutive passes.  Use ``--nocache`` to skip
the cache.

If your committers screw up their settings -- and boy, they do! -- you can
supply a file mapping author names to real identities via ``--pseudonyms``
(defaults to ``.names``).  It is a simple, two-column CSV file with the fields
*committer*, and *real author*.

You can define additional achievements in a very simple manner:  You have to
inherit from `commithero.achievements.Achievement` and must define a
``on_commit`` method which takes an *author* (a string) and a *commit* (a
`anyvc.common.Revision`).  Whenever you return `True` from such a method the
system considers this particular achievement unlocked.

The achievement description is automatically retrieved from its docstring and
its name is generated from its class name (eg. a class ``WellDone`` becomes
*Well Done*).  See ``commithero/achievements/`` for samples.

* You are free to set ``name`` on your achievement class if you are unhappy
  with restrictions imposed by Python.
* If you need to generated several achievements from a single class you can
  return a tuple of *title* and *description*.
* See ``ProgressiveAchievement`` for achievements which have multiple levels.
