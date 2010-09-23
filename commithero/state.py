from .achievements import Achievement
from email.utils import parseaddr
from collections import defaultdict, deque


class RepositoryState(object):
    """Pickle-able metadata collection of a repository.

    Allows to lazily update a set of commits, ie. when having run `commithero`
    from a previous checkout and now updating the achievements with only recent
    commits.

    """
    def __init__(self):
        # stores only IDs, not whole revision objects
        self.visited = set()
        # account for users temporarily misconfiguring their username
        self.emails = {}
        # keep track of achievements, mapping authors to tuples of
        # (achievement, description, commit)
        self.achievements = defaultdict(list)
        # same for chronological order, a sequence of tuples of
        # (date, author, (achievement, description), commit)
        self.history = deque()
        # fetch listening achievements
        self.listeners = [ach() for ach in Achievement.registry]
        # we expect applications to set _synonyms, a mapping of aliases to real
        # author names

    def clean_author(self, origin):
        # aliasfile may override determined authors
        if origin in self._synonyms:
            return self._synonyms[origin]
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
        if author in self._synonyms:
            return self._synonyms[author]
        return author

    def commit(self, commit):
        if commit.id in self.visited:
            return

        author = self.clean_author(commit.author)

        # notify all listeners
        for ach in self.listeners:
            result = ach.on_commit(author, commit)
            if result:
                if result is True: # support lazy achievements
                    result = ach.name, ach.__doc__
                self.achievements[author].append(result + (commit.id,))
                self.history.append((commit.time, author, result, commit.id))
