from .achievements import Achievement
from email.utils import parseaddr
from collections import defaultdict, deque
import operator
import string


class Repository(object):
    """Pickle-able metadata collection of a repository.

    Allows to lazily update a set of commits, ie. when having run `commithero`
    from a previous checkout and now updating the achievements with only recent
    commits.

    All instance variables are primitive types ready for pickling.

    :ivar visited: set of visited revision IDs (explicitly does not store whole
                   revision objects to allow sane pickling)

    :ivar achievements: keeps track of achievements by author
    :ivar history: same as :ivar:`achievements` but denormalized to
                   chronological order

    :ivar listeners: instances of `Achievement` waiting for commit events
    :ivar synonyms: mapping of aliases to authors, set by calls to this
                    instance when entering context

    """
    def __init__(self):
        self.visited = set()
        # (achievement, description) -> (date, commit)
        self.achievements = defaultdict(dict)
        # (date, author, (achievement, description), commit)
        self.history = deque()
        # fetch listening achievements
        self.listeners = [ach() for ach in Achievement.registry]
        self.synonyms = {}

    def clean_author(self, origin):
        # aliasfile may override determined authors
        origin = origin.strip('"')
        if origin in self.synonyms:
            return self.synonyms[origin]

        if '<' in origin: # chances are high this is an email
            author, mail = parseaddr(origin)
            # try aliasfile again for name parts
            if mail in self.synonyms:
                return self.synonyms[mail]
            if author in self.synonyms:
                return self.synonyms[author]
            return author or mail
        return origin # if all else fails

    def __call__(self, aliases):
        """Pass in aliases and make ready to enter context."""
        assert not self.synonyms, "can only enter context once"
        self.synonyms = aliases
        return self
    def __enter__(self):
        pass
    def __exit__(self, typ, val, tb):
        self.synonyms = {}

    def commit(self, commit):
        """
        Process a commit.  It automatically extracts the author and notifies
        all listening achievements about this new commit (:ivar:`visited` is
        **ignored**).

        :param commit: `anyvc.common.repository.Revision`

        """
        author = self.clean_author(commit.author)

        commit.changes = changes = []
        for fname in commit.get_changed_files():
            try:
                new = commit.file_content(fname)
            except IOError: # removed file
                new = ""
            try:
                old = commit.parents[0].file_content(fname)
            except (IOError, IndexError): # added file
                old = ""
            changes.append((fname, old, new))

        # notify all listeners
        for ach in self.listeners:
            result = ach.on_commit(author, commit)
            self.award(author, ach, result, commit)

    def award(self, author, ach, result, commit):
        """
        Award an achievement `ach` based on its computed value `result` from a
        commit.  If `result` is ``None`` this call is a noop.

        :param string author: clean name
        :param ach: an `Achievement` subclass
        :param result: tuple of *title* and *description*
        :param commit: `anyvc.common.repository.Revision`

        Achievements are free to return ``True`` instead.  The name will be
        computed from its ``name`` attribute or, failing that, from its class
        name (NB. this is *actually* done in `Achievement`).  Its description
        is automatically fetched from its docstring.

        All descriptions are decorated with a trailing full stop if they do not
        end with a puncutation sign (as per `string.punctuation`).

        """
        if result:
            if result is True: # support lazy achievements
                result = ach.name, ach.__doc__
            name, desc = result
            if desc[-1] not in string.punctuation:
                result = name, desc + '.'
            if result in self.achievements[author]:
                return # do not award achievement again
            self.achievements[author][result] = (commit.time, commit.id)
            self.history.append((commit.time, author, result, commit.id))

    def walk(self, repo):
        """Examine a repository for new commits.

        :param repo: `anyvc.common.repository.Repository`

        """
        head = repo.get_default_head()
        if head.id in self.visited:
            return # no commits since last run

        # fetch all unvisited revisions
        queue = deque([head]) # traverse from HEAD
        revisions = deque() # strictly a subset of `visited`
        while queue:
            revision = queue.pop() # goes depth-first
            revisions.append(revision)
            self.visited.add(revision.id)
            queue.extend(parent for parent in revision.parents
                        if parent.id not in self.visited)

        # now commit all new revisions in order
        for revision in sorted(revisions, key=operator.attrgetter('time')):
            self.commit(revision)
