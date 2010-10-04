from . import Achievement
from . import AdditionAchievement

class CAchievement(Achievement):
    "Change a C-esque file with a suffix recognized by GCC."
    ext = [
           'h', 'c', 'i' # C
           'ii', 'cc', 'cp', 'cxx', 'cpp', 'c++', # C++
           'hh', 'hp', 'hxx', 'hpp', 'h++', 'tcc', # C++ headers
           'm', 'mi', # Objective-C
           'xs', # Perl External Subroutine
          ]

class ThreeStarProgrammer(CAchievement, AdditionAchievement):
    "Cram at least three levels of indirection into your head."
    added = "void***"

class Win32Hell(CAchievement):
    "My life for Redmond!"
    def on_change(self, old, new):
        return sum(new.count(line) - old.count(line) for line in
                   ("\n#ifdef _WIN32", "\n#ifdef WIN32",
                    "\n#if defined(_WIN32)", "\n#if defined(WIN32)")
               ) > 0

class Pragmatic(CAchievement, AdditionAchievement):
    "Dear compiler, why are you always so mean to me?"
    added = "\n#pragma "

class MrImportant(CAchievement, AdditionAchievement):
    "Promote a library to a system header."
    added = "\n#pragma GCC system_header"
