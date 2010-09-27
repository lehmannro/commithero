from . import Achievement

class LambdaCalculus(Achievement):
    "Because inline function are, like, totally more readable!"
    def on_commit(self, author, commit):
        lambdas = 0
        for fname, old, new in commit.changes:
            if not fname.lower().endswith('.py'):
                continue
            lambdas += new.count("lambda") - old.count("lambda")
        if lambdas > 0:
            return True
