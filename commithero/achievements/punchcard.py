from . import Achievement

class Insomniac(Achievement):
    "More coding, less sleeping."
    def on_commit(self, author, commit):
        return commit.time.hour in (2, 3, 4)

class GrandfatherParadox(Achievement):
    "Technically, you are your own parent now."
    def on_commit(self, author, commit):
        return any(commit.time < parent.time for parent in commit.parents)
