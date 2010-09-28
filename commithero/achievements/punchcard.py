from . import Achievement

class Insomniac(Achievement):
    "More coding, less sleeping."
    def on_commit(self, author, commit):
        return commit.time.hour in (2, 3, 4)
