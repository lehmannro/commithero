``commithero`` analyzes a repository for commits and awards individual authors
achievements based on their work.

It caches results from previous runs in the repository for performance reasons.
A `RepositoryState` is pickled to a file called ``.commithero`` (see ``-c`` to
modify its name) and loaded in consecutive passes.  Use ``--nocache`` to skip
the cache.

If your committers screw up their settings -- and boy, they do! -- you can
supply a file mapping author names to real identities via ``--pseudonyms``
(defaults to ``.names``).  It is a simple, two-column CSV file with the fields
*committer*, and *real author*.
