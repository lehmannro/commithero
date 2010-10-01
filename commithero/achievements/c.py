from . import Achievement

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
