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
        return len(commit.parents) == 1

class Merges(ProgressiveAchievement):
    goals = {
        1: ("Team Mate", "Merge from another source"),
    }
    def check(self, commit):
        #XXX this could be a local merge, too
        return len(commit.parents) > 1
