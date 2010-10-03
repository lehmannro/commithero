from . import Achievement

class ThreeStarProgrammer(Achievement):
    "Cram at least three levels of indirection into your head."
    def on_commit(self, author, commit):
        diff = commit.get_parent_diff()
        for line in diff:
            if line.startswith('+'):
                if 'void***' in line:
                    return True

class Win32Hell(Achievement):
    "My life for Redmond!"
    def on_commit(self, author, commit):
        for path in commit.get_changed_files():
            diff = commit.get_parent_diff()
            if "\n+#ifdef _WIN32" in diff \
            or "\n+#ifdef WIN32" in diff \
            or "\n+#if defined(_WIN32)" in diff \
            or "\n+#if defined(WIN32)" in diff:
                return True
