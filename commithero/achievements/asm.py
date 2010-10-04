from . import Achievement

class AssemblyHacker(Achievement):
    "Compilers are for wusses!"
    ext = ['S', 'asm', 'sx']
    def on_change(self, old, new):
        return new is not None
