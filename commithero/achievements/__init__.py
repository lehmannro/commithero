from collections import defaultdict
import re

TITLECASE = re.compile(r'(?<=.)([A-Z])')

class Achievement(object):
    registry = set()
    class __metaclass__(type):
        def __init__(cls, name, bases, clsdict):
            cls.registry.add(cls)
            #XXX explicitly mark achievements as abstract?
            cls.registry -= set(bases)
            cls.name = TITLECASE.sub(r' \1', cls.__name__)

    def on_commit(self, author, commit):
        raise NotImplementedError


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

    def check(self, author, commit):
        raise NotImplementedError

from . import commits
from . import meta