from collections import defaultdict
import re

TITLECASE = re.compile(r'(?<=.)([A-Z])')

class Achievement:
    """An achievement and the rules for its award.

    It may hold state related to the repository it has been applied to (even
    though it does not know which repository that is, check
    `ProgressiveAchievement` for one such implementation).  Thus it needs to
    remain pickleable.

    :cvar string name: title
    :cvar __doc__: description

    Once an achievement has been awarded its representation is permanently
    logged to the tracked repository.  See `~commithero.state.Repository.award`
    for details.

    :cvar registry: all achievements

    All leaf subclasses of `Achievement` are automagically added to
    `registry`:attr: for easy collection.

    """
    registry = set()
    class __metaclass__(type):
        def __init__(cls, name, bases, clsdict):
            assert '__doc__' in clsdict, \
                "%s misses description docstring" % name
            cls.registry.add(cls)
            #XXX explicitly mark achievements as abstract?
            cls.registry -= set(bases)
            if 'name' not in clsdict: # class did not genuinely specify a name
                cls.name = TITLECASE.sub(r' \1', cls.__name__)
            cls.ext = [s.lower() for s in clsdict.get('ext', [])]
            cls.path = [s.lower() for s in clsdict.get('path', [])]
            for base in bases:
                cls.ext.extend(base.ext)
                cls.path.extend(base.path)

    def on_commit(self, author, commit):
        """Assess a commit.

        :param string author: clean name
        :param commit: `anyvc.common.repository.Revision`
        :return: see `commithero.Repository.award`

        """
        pass

    def on_change(self, old, new):
        """Assess a specific change to a file.

        :param string old: contents in base parent commit
        :param string new: contents in current commit
        :return: see `commithero.state.Repository.award`

        If either of *old* or *new* are None the file in question has been
        added or removed, respectively.

        This method is merely a convenience method to save iteration over all
        of the commit's files
        (`~anyvc.common.repository.Revision.get_changed_files`);  it *can* be
        implemented solely by the means of `on_commit`.

        There are two ways to limit its invocation based on the handled file:

            * Set ``path`` to a list of file names.
            * Set ``ext`` to a list of file suffixes.

        """
        pass


class ProgressiveAchievement(Achievement):
    """Achievements with multiple tiers."""
    def __init__(self):
        self.counter = defaultdict(int)

    def on_commit(self, author, commit):
        if self.check(commit):
            # strictly stepwise
            self.counter[author] += 1
            return self.counter[author]

    def check(self, commit):
        """Detect if a commit counts as progress towards a goal.

        :param commit: `anyvc.common.repository.Revision`
        :rtype: boolean

        """
        raise NotImplementedError

class MetricAchievement(Achievement):
    """Achievements awarded when a particular scoring criteria has increased.

    """

    def on_change(self, old, new):
        old_score = self.score(old) if old else 0
        new_score = self.score(new) if new else 0
        return new_score > old_score

    def score(self, content):
        """Assess a score for a particular chunk of file content.

        :param string content: chunk

        """
        raise NotImplementedError

class AdditionAchievement(Achievement):
    """Achievement which counts occurrences of text snippets in changed files.

    :cvar string added: text which should have been added, or list of them

    """
    # Could possibly be migrated to a MetricAchievement with its score computed
    # as sum(content.count(snippet) for snippet in self.added) but this would
    # not award the achievement if *one* of the snippets has been replaced by
    # another one (which is feasible as it demonstrates work in that niche)
    #XXX moved chunks across files
    def on_change(self, old, new):
        for snippet in self.added:
            new_count = new.count(snippet) if new else 0
            old_count = old.count(snippet) if old else 0
            # cannot just return comparison result as we are in a loop
            if new_count > old_count:
                return True

from . import commits
from . import message
from . import meta
from . import punchcard
from . import text
from . import python
from . import gcc
from . import asm
from . import tools
