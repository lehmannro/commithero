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
