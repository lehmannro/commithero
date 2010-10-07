from . import Achievement
from . import ProgressiveAchievement
import os.path

class FoundingFather(Achievement):
    "Start the repository."
    def on_commit(self, author, commit):
        return not commit.parents

class OctoMerge(Achievement):
    "Merge from more than two sources simultaneously."
    def on_commit(self, author, commit):
        return len(commit.parents) > 2 \
            or len(commit.parents) == 2 \
           and any(len(c.parents) > 1 for c in commit.parents
                   if c.author == commit.author)

class BugFixes(ProgressiveAchievement):
    "Close X issues."
    goals = {
        1: ("Handyman", "Close an issue."),
        5: ("Craftsman", "Close five issues."),
        15: ("Bug Squasher", "Close fifteen issues."),
        30: ("Exterminator", "Close thirty issues."),
    }
    def check(self, commit):
        return ". closes #" in commit.message.lower()

class BlahBlahBlah(Achievement):
    "Tell the newest gossip in commit messages."
    def on_commit(self, author, commit):
        return '\n' in commit.message

class Polyglot(Achievement):
    "Master at least three languages."
    def on_commit(self, author, commit):
        exts = set(os.path.splitext(path)[1][1:].lower()
                   for path in commit.get_changed_files()
               ) - set(['in', 'txt'])
        #XXX binary files
        return len(exts) >= 3

class MuffinMan(Achievement):
    "Om nom nom, that's one rich commit."
    def on_change(self, old, new):
        return new and len(new) > 10 * 1024 * 1024 # 10MB
