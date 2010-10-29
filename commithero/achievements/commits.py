from . import Achievement
from . import ProgressiveAchievement

class Commits(ProgressiveAchievement):
    "Commit at least X times."
    goals = {
        1: ("Script Kiddie", "Commit at least once."),
        5: ("Volunteer", "Commit at least five times."),
        20: ("Contributor", "Commit at least twenty times."),
        50: ("Developer", "Commit at least fifty times."),
        100: ("Core Developer", "Commit at least hundred times."),
        200: ("Full-Time Developer", "Commit at least two hundred times."),
        500: ("Maniac", "Commit at least five hundred times."),
    }
    def check(self, commit):
        #XXX honour merge conflicts
        return len(commit.parents) <= 1

class Merges(ProgressiveAchievement):
    "Merge at least X times."
    goals = {
        1: ("Team Player", "Merge from another source."),
    }
    def check(self, commit):
        return len(commit.parents) > 1 \
           and any(p.author != commit.author for p in commit.parents)

class Rollback(Achievement):
    "Immediately withdraw one of your changes again."
    name = "Ooopsie"
    def on_commit(self, author, commit):
        if len(commit.parents) != 1 or len(commit.parents[0].parents) != 1:
            return
        parent = commit.parents[0].parents[0]
        for f in commit.get_changed_files():
            old = parent.file_content(f) if parent.exists(f) else None
            new = commit.file_content(f) if commit.exists(f) else None
            if old == new:
                return True

class CommitStreak(Achievement):
    "Commit without remote interaction or branching."
    goals = {
        10: ("Lone Star", "Commit ten times in a row."),
        30: ("Flawless Hat-Trick", "Commit thirty times in a row."),
        50: ("Nap Hand", "Commit fifty times in a row."),
        100: ("Hello?! Is Anybody Out There?",
              "Commit a hundred times in a row."),
    }
    def on_commit(self, author, commit):
        current = commit
        for streak in xrange(100): # do not loop longer than necessary
            if len(current.parents) != 1 or current.author != commit.author:
                break
            current, = current.parents
        # starts from 0 but the current commit is always part of a streak
        return streak + 1
