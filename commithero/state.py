from .achievements import Achievement
from email.utils import parseaddr
from collections import defaultdict, deque
import operator


class Repository(object):
    """Pickle-able metadata collection of a repository.

    Allows to lazily update a set of commits, ie. when having run `commithero`
    from a previous checkout and now updating the achievements with only recent
    commits.

    All instance variables are primitive types ready for pickling.

    :ivar visited: set of visited revision IDs (explicitly does not store whole
                   revision objects to allow sane pickling)
    :ivar emails: cached mapping of emails to author names to account for users
                  temporarily misconfiguring their username but not their email

    :ivar achievements: keeps track of achievements by author
    :ivar history: same as :ivar:`achievements` but denormalized to
                   chronological order

    :ivar listeners: instances of `Achievement` waiting for commit events
    :ivar synonyms: mapping of aliases to authors, set by calls to this
                    instance when entering context

    """
    def __init__(self):
        self.visited = set()
        self.emails = {}
        # (achievement, description, commit)
        self.achievements = defaultdict(list)
        # (date, author, (achievement, description), commit)
        self.history = deque()
        # fetch listening achievements
        self.listeners = [ach() for ach in Achievement.registry]
        self.synonyms = {}

    def clean_author(self, origin):
        # aliasfile may override determined authors
        if origin in self.synonyms:
            return self.synonyms[origin]
        author, mail = parseaddr(origin)
        # strip comments from author
        lparen = author.rfind(' (')
        if author.rfind(')') > lparen:
            author = author[:lparen]
        # restore author from mail
        if author not in self.achievements:
            if mail in self.emails:
                author = self.emails[mail]
            else:
                # map new email to author
                self.emails[mail] = author
        # try aliasfile again for properly stripped names
        if author in self.synonyms:
            return self.synonyms[author]
        return author

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
        all listening achievements about this new commit (commits which have
        already been processed will be silently ignored).

        :param commit: `anyvc.common.Revision`

        """
        author = self.clean_author(commit.author)

        # notify all listeners
        for ach in self.listeners:
            result = ach.on_commit(author, commit)
            if result:
                if result is True: # support lazy achievements
                    result = ach.name, ach.__doc__
                self.achievements[author].append(result + (commit.id,))
                self.history.append((commit.time, author, result, commit.id))

    def walk(self, repo):
        """Examine a repository for new commits.

        :param repo: `anyvc.common.Repository`

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
