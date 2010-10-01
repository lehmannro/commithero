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

class MakefileKungFu(Achievement):
    "Your Makefile consists of more than 30 lines!"
    name = "Makefile Kung-Fu"
    def on_commit(self, author, commit):
        for fname in commit.get_changed_files():
            if not any(fname.endswith(makefile) for makefile in
                ['Makefile', 'makefile', 'GNUmakefile']):
               continue
            if commit.exists(fname):
                content = commit.file_content(fname)
                if content.count('\n') >= 30:
                    return True
                # Do not return if condition did not match because other
                # Makefiles could well match.

class DirtyTempFile(Achievement):
    "Including your temporary files is not gonna help."
    name = "You dirty little..."
    def on_commit(self, author, commit):
        return any(path.endswith('~') or path.endswith('.swp')
           for path in commit.get_changed_files())
