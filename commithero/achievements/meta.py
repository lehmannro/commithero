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

class LargeFile(Achievement):
    "Commit a very large file."
    goals = {
        1*1024*1024: ("Obesity", "Grow a file over one megabyte."),
        10*1024*1024: ("Muffin Man", "Om nom nom, that's one rich commit."),
        50*1024*1024: ("Kirby", "Inhale a file at least fifty MB in size."),
    }
    def on_change(self, old, new):
        return new and len(new)

class MultipleIdentities(Achievement):
    "Commit from more than one identity."
    goals = {
        2: ("Schizophrenia", "Contribute from two or more identities."),
        6: ("Jason Bourne", "Cover your tracks with half a dozen of identities."),
        300: ("Sparta", "These, uh, 300 men are my personal bodyguard."),
    }
    def __init__(self):
        self.idents = {}
    def on_commit(self, author, commit):
        idents = self.idents.setdefault(author, set())
        idents.add(commit.author.lower())
        return len(idents)

try:
    from collections import Counter
except ImportError:
    class Counter(dict):
        def update(self, iterable):
            self_get = self.get
            for elem in iterable:
                self[elem] = self_get(elem, 0) + 1
        def subtract(self, iterable):
            self_get = self.get
            for elem in iterable:
                self[elem] = self_get(elem, 0) - 1
from anyvc.diff import diff_for_file

class Mover(Achievement):
    "Contribute no original work."
    goals = {
        1: ("Moving Target", "Move a line through your code base."),
        25: ("Trucker", "Transport twenty-five or more lines around."),
        50: ("Relocation Service", "Ship at least fifty lines around."),
    }
    def on_commit(self, author, commit):
        added = Counter()
        removed = Counter()
        # get_parent_diff would be fine if headers were not harder to parse
        for path in commit.get_changed_files():
            diff = list(diff_for_file(commit, path))[2:] # strip off header
            added.update(line[1:] for line in diff if line.startswith('+'))
            removed.update(line[1:] for line in diff if line.startswith('-'))
        added.subtract(removed)
        # all additions are remedied by removals
        if all(val == 0 for val in added.itervalues()):
            return sum(removed.itervalues())

class SecretAgent(Achievement):
    "Modify a hidden file."
    def on_commit(self, author, commit):
        return any(os.path.split(path)[1].startswith('.')
                   for path in commit.get_changed_files())
