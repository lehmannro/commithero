from . import Achievement
from datetime import timedelta
from collections import deque

class Insomniac(Achievement):
    "More coding, less sleeping."
    def on_commit(self, author, commit):
        return commit.time.hour in (2, 3, 4)

class EarlyBird(Achievement):
    "Early to rise, early to commit."
    def on_commit(self, author, commit):
        return commit.time.hour in (5, 6)

class SantaClaus(Achievement):
    "Bring some commits for Christmas."
    def on_commit(self, author, commit):
        return commit.time.month == 12 and commit.time.day in (24, 25)

class Laborer(Achievement):
    "Craft some commits during the working hours."
    def on_commit(self, author, commit):
        return commit.time.hour in (9, 10, 11, 12, 13, 14, 15, 16)  # 9 to 5

class GrandfatherParadox(Achievement):
    "Technically, you are your own parent now."
    def on_commit(self, author, commit):
        return any(commit.time < parent.time for parent in commit.parents)

class FastestGunInTheWest(Achievement):
    "Shoot, shoot."
    def on_commit(self, author, commit):
        return any(abs(commit.time - parent.time) < timedelta(seconds=1)
           for parent in commit.parents)

class FifteenMinutesOfFame(Achievement):
    "A dozen commits while waiting for your tea."
    def on_commit(self, author, commit):
        recent = 1
        queue = deque(commit.parents)
        while queue:
            current = queue.pop()
            if commit.time - current.time < timedelta(minutes=15):
                queue.extend(current.parents)
                if current.author == commit.author:
                    recent += 1
                    if recent >= 12:
                        break # optimization
        return recent >= 12

class ShomerShabbos(Achievement):
    "Check-in on a Saturday."
    def on_commit(self, author, commit):
        return commit.time.isoweekday() == 7
