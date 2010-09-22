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

class Commits(ProgressiveAchievement):
    goals = {
        1: ("Script Kiddie", "Commit at least once"),
        5: ("Volunteer", "Commit at least five times"),
        20: ("Contributor", "Commit at least twenty times"),
        50: ("Developer", "Commit at least fifty times"),
        100: ("Core Developer", "Commit at least hundred times"),
        200: ("Full-Time Developer", "Commit at least two hundred times"),
        500: ("Maniac", "Commit at least five hundred times"),
    }
    def check(self, commit):
        if len(commit.parents) == 1: #XXX honour merge conflicts
            return True

class Merges(ProgressiveAchievement):
    goals = {
        1: ("Team Mate", "Merge from another source"),
    }
    def check(self, commit):
        if len(commit.parents) > 1:
            #XXX this could be a local merge, too
            return True

class OctoMerge(Achievement):
    "Merge from more than two sources simultaneously"
    def on_commit(self, author, commit):
        if len(commit.parents) > 2:
            return True

class InitialCommit(Achievement):
    "Start the repository"
    def on_commit(self, author, commit):
        if not commit.parents:
            return True

class BugFixes(ProgressiveAchievement):
    goals = {
        1: ("Handyman", "Close an issue"),
        5: ("Craftsman", "Close five issues"),
        15: ("Bug Squasher", "Close fifteen issues"),
        30: ("Exterminator", "Close thirty issues"),
    }
    def check(self, commit):
        if ". closes #" in commit.message.lower():
            return True
