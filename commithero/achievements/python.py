from . import Achievement

class LambdaCalculus(Achievement):
    "Because inline function are, like, totally more readable!"
    def on_commit(self, author, commit):
        lambdas = 0
        for fname in commit.get_changed_files():
            if not fname.lower().endswith('.py'):
                continue
            try:
                new = commit.file_content(fname)
            except IOError: # removed file
                new = ""
            try:
                old = commit.parents[0].file_content(fname)
            except (IOError, IndexError): # added file
                old = ""
            lambdas += new.count("lambda") - old.count("lambda")
        return lambdas > 0

class Fedex(Achievement):
    "Introduce a new Python package."
    name = "FedEx"
    def on_commit(self, author, commit):
        for path in commit.get_changed_files():
            if path.endswith('__init__.py'):
                for parent in commit.parents:
                    if parent.exists(path):
                        break
                else:
                    return True
