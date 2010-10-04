from . import Achievement

class CAchievement(Achievement):
    ext = [
           'h', 'c', 'i' # C
           'ii', 'cc', 'cp', 'cxx', 'cpp', 'c++', # C++
           'hh', 'hp', 'hxx', 'hpp', 'h++', 'tcc', # C++ headers
           'm', 'mi', # Objective-C
           'xs', # Perl External Subroutine
          ]

class ThreeStarProgrammer(CAchievement):
    "Cram at least three levels of indirection into your head."
    def on_change(self, old, new):
        return new.count('void***') - old.count('void***') > 0

class Win32Hell(CAchievement):
    "My life for Redmond!"
    def on_change(self, old, new):
        return sum(new.count(line) - old.count(line) for line in
                   ("\n#ifdef _WIN32", "\n#ifdef WIN32",
                    "\n#if defined(_WIN32)", "\n#if defined(WIN32)")
               ) > 0

class Pragmatic(CAchievement):
    "Dear compiler, why are you always so mean to me?"
    def on_change(self, old, new):
        return new.count("\n#pragma ") - old.count("\n#pragma ") > 0

class MrImportant(CAchievement):
    "Promote a library to a system header."
    def on_change(self, old, new):
        line = "\n#pragma GCC system_header"
        return new.count(line) - old.count(line) > 0
