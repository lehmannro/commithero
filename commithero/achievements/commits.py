from . import Achievement
from . import ProgressiveAchievement

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
        #XXX honour merge conflicts
        return len(commit.parents) <= 1

class Merges(ProgressiveAchievement):
    goals = {
        1: ("Team Player", "Merge from another source"),
    }
    def check(self, commit):
        return len(commit.parents) > 1 \
           and any(p.author != commit.author for p in commit.parents)

class Ooopsie(Achievement):
    "Immediately withdraw one of your changes again"
    def on_commit(self, author, commit):
        if len(commit.parents) != 1 or len(commit.parents[0].parents) != 1:
            return
        parent = commit.parents[0].parents[0]
        for f in commit.get_changed_files():
            print "change:", f
            try:
                old = parent.file_content(f)
            except IOError:
                old = ""
            try:
                new = commit.file_content(f)
            except IOError:
                new = ""
            if old == new:
                return True
