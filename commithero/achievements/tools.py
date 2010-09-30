from . import Achievement

class AutomakeHell(Achievement):
    def on_commit(self, author, commit):
        return any(path.endswith('Makefile.am')
           for path in commit.get_changed_files())

class AutoconfHell(Achievement):
    def on_commit(self, author, commit):
        return any(path.endswith('configure.in')
           for path in commit.get_changed_files())

class HandwrittenConfigure(Achievement):
    "Your configure script is a beautiful and unique butterfly."
    name = "I Can Do Better Than GNU"
    def on_commit(self, author, commit):
        return any(path.endswith('configure') and
                   ('GNU Autoconf' not in commit[path]
                    or 'autoconf' not in commit[path])
           for path in commit.get_changed_files())
