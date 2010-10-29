from . import Achievement
from . import ProgressiveAchievement
import os.path
import re

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
    "Close issues."
    goals = {
        1: ("Handyman", "Close an issue."),
        5: ("Craftsman", "Close five issues."),
        15: ("Bug Squasher", "Close fifteen issues."),
        30: ("Exterminator", "Close thirty issues."),
    }
    def check(self, commit):
        msg = commit.message.lower()
        return "closes #" in msg or "closes gh-" in msg

class BugFixesAgain(Achievement):
    "Close an issue which has already been closed."
    def __init__(self):
        self.closed = set()
    def on_commit(self, author, commit):
        closes = set(re.findall(r'closes (?:gh-|#)(\d+)',
                                commit.message.lower()))
        again = not self.closed.isdisjoint(closes)
        self.closed.update(closed)
        return again

class MultilineCommitMessages(Achievement):
    "Span multiple lines with your commit message."
    goals = {
        2: ("Long-Winded", "Conciseness isn't your strength."),
        4: ("Blah Blah Blah", "Tell the newest gossip in commit messages."),
        10: ("Essayist", "Document your project in commit messages."),
    }
    def on_commit(self, author, commit):
        #XXX score should be number of lines
        return commit.message.count('\n')

class Polyglot(Achievement):
    "Master multiple languages in one commit."
    goals = {
        2: ("Pidgin", "Master a pair of languages."),
        3: ("Polyglot", "Master three languages."),
        6: ("Impressive Resume", "Master half a dozen of languages."),
        10: ("Peter Norvig", "Master ten languages."),
    }
    def on_commit(self, author, commit):
        exts = set(os.path.splitext(path)[1][1:].lower()
                   for path in commit.get_changed_files()
               ) - set(['in', 'txt', ''])
        #XXX binary files
        return len(exts)

class MuffinMan(Achievement):
    "Om nom nom, that's one rich commit."
    def on_change(self, old, new):
        return new and len(new) > 10 * 1024 * 1024 # 10MB
