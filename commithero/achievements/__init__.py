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
    logged to the tracked repository.  See `commithero.state.Repository.award`
    for details.

    :cvar registry: all achievements

    All leaf subclasses of `Achievement` are automagically added to `registry`
    for easy collection.

    """
    registry = set()
    class __metaclass__(type):
        def __init__(cls, name, bases, clsdict):
            assert '__doc__' in clsdict, "docstring becomes description"
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
        :return: see `commithero.state.Repository.award`

        """
        pass

    def on_change(self, old, new):
        """Assess a specific change to a file.

        :param string old: contents in base parent commit
        :param string new: contents in current commit
        :return: see `commithero.state.Repository.award`

        This method is merely a convenience method to save iteration over all
        of the commit's files (`get_changed_files`);  it *can* be implemented
        solely by the means of `on_commit`.

        There are two ways to limit its invokation based on the handled file:

            * Set ``path`` to a list of file names.
            * Set ``ext`` to a list of file suffixes.

        """
        pass


class ProgressiveAchievement(Achievement):
    goals = {}
    def __init__(self):
        self.counter = defaultdict(int)

    def on_commit(self, author, commit):
        if self.check(commit):
            self.counter[author] += 1
            count = self.counter[author]
            if count in self.goals:
                return self.goals[count]

    def check(self, commit):
        """Detect if a commit counts as progress towards a goal.

        :param commit: `anyvc.common.repository.Revision`
        :rtype: boolean

        """
        raise NotImplementedError

from . import commits
from . import meta
from . import punchcard
from . import python
from . import gcc
from . import asm
from . import tools
