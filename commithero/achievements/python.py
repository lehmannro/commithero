from . import Achievement

class LambdaCalculus(Achievement):
    "Because inline function are, like, totally more readable!"
    def on_commit(self, author, commit):
        lambdas = 0
        for fname in commit.get_changed_files():
            if fname.lower().endswith('.py'):
                try:
                    new = commit.file_content(fname)
                except IOError: # removed file
                    new = ""
                try:
                    old = commit.parents[0].file_content(fname)
                except (IOError, IndexError): # added file
                    old = ""
                count_new = new.count("lambda")
                count_old = old.count("lambda")
                lambdas += count_new - count_old
        return lambdas > 0
