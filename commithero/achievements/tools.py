from . import Achievement

class AutomakeHell(Achievement):
    "We can't abandon m68k just yet!"
    path = ['Makefile.am']
    def on_change(self, old, new):
        return new is not None

class AutoconfHell(Achievement):
    "Do you compile correctly on Cray systems?"
    path = ['configure.in']
    def on_change(self, old, new):
        return new is not None

class HandwrittenConfigure(Achievement):
    "Your configure script is a beautiful and unique butterfly."
    name = "I Can Do Better Than GNU"
    path = ['configure']
    def on_change(self, old, new):
        return new and 'GNU Autoconf' not in new and 'autoconf' not in new

class MakefileKungFu(Achievement):
    "Your Makefile consists of more than 30 lines!"
    name = "Makefile Kung-Fu"
    path = ['Makefile', 'GNUmakefile']
    def on_change(self, old, new):
        return new and new.count('\n') >= 30

class DirtyTempFile(Achievement):
    "Including your temporary files is not gonna help."
    name = "You dirty little..."
    ext = ['swp']
    def on_change(self, old, new):
        return old is None
    def on_commit(self, author, commit):
        return any(path.endswith('~') and commit.exists(path)
           for path in commit.get_changed_files())
