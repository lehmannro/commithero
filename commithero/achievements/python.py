from . import Achievement
from . import AdditionAchievement
from . import MetricAchievement
import itertools

class PyAchievement(Achievement):
    "Achievement granted for working on Python files."
    ext = ['py']

class Pythonista(PyAchievement):
    "You need not necessarily be Dutch."
    def on_change(self, old, new):
        return True

class LambdaCalculus(PyAchievement, AdditionAchievement):
    "Because inline functions are, like, totally more readable!"
    added = ["lambda"]

class Fedex(Achievement):
    "Introduce a new Python package."
    name = "FedEx"
    path = ['__init__.py']
    def on_change(self, old, new):
        # file has been added
        return old is None

class PartyDecorations(PyAchievement, MetricAchievement):
    "Use three or more decorators on one function."
    def score(self, content):
        return sum(1 for is_deco, lines
                   #XXX ignore empty lines between decorator and function
                   in itertools.groupby(content.splitlines(),
                      lambda line: line.startswith("@"))
                   if is_deco and len(list(lines)) >= 3)

class SpelunkingInUnderpants(PyAchievement, AdditionAchievement):
    "Pollute your environment by using star imports."
    added = ["import *"]

class UnderpantsGnome(PyAchievement, AdditionAchievement):
    "Commit debugger invocations into production code."
    added = ["pdb.set_trace()"]

class RocketScience(PyAchievement, AdditionAchievement):
    "Using 'while True' obviously means you know *exactly* what you're doing."
    added = ["while True:"]

class LooooongCode(PyAchievement, MetricAchievement):
    "Using lines longer than 80 characters shows off how large your screen really is."
    # ironically the line above is longer than 80
    def score(self, content):
        return sum(1 for line in content.splitlines() if len(line) > 80)

class Regex(PyAchievement, AdditionAchievement):
    "Now they have two problems."
    name = "I Know, I'll Use Regular Expressions"
    added = ["import re\n", "from re import "]
