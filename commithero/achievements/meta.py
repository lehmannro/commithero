from . import Achievement
from . import ProgressiveAchievement

class FoundingFather(Achievement):
    "Start the repository"
    def on_commit(self, author, commit):
        if not commit.parents:
            return True

class OctoMerge(Achievement):
    "Merge from more than two sources simultaneously"
    def on_commit(self, author, commit):
        if len(commit.parents) > 2:
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
