from . import Achievement
import string

CHARS = ''.join(chr(i) for i in xrange(256))

def remove_whitespace(s):
    return s.translate(CHARS, string.whitespace)

class WhitespaceChanges(Achievement):
    "Removing whitespace is a valuable compression."
    name = "Anal"
    def on_change(self, old, new):
        return old and new and len(old) > len(new) and \
               remove_whitespace(old) == remove_whitespace(new)
