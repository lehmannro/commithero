from . import Achievement
from . import ProgressiveAchievement
import re

class MultilineCommitMessages(Achievement):
    "Span multiple lines with your commit message."
    goals = {
        3: ("Long-Winded", "Conciseness isn't your strength."),
        5: ("Blah Blah Blah", "Tell the newest gossip in commit messages."),
        10: ("Essayist", "Document your project in commit messages."),
    }
    def on_commit(self, author, commit):
        return sum(1 for line in commit.message.splitlines() if line)

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
        self.closed.update(closes)
        return again

class DirtyWords(Achievement):
    "Mention the dirty words in your commit message."
    goals = {
        1: ("Language!", "Mention a dirty word in your commit message."),
        2: ("PG-Rated", "Mention two dirty words in your commit message."),
        3: ("Choleric", "Mention three dirty words in your commit message."),
        7: ("George Carlin", "Mention all dirty words in your commit message"),
    }
    words = 'ass balls cocksucker cunt fuck motherfucker piss shit tits'.split()
    def on_commit(self, author, commit):
        # May trigger involuntarily, eg. with "assertion."
        return sum(1 for word in self.words if word in commit.message.lower())
