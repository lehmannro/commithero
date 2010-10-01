from . import Achievement

class AssemblyHacker(Achievement):
    "Compilers are for wusses!"
    def on_commit(self, author, commit):
        return any(path.upper().endswith('.S') or path.lower().endswith('.asm')
           for path in commit.get_changed_files())
