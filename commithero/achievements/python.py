from . import Achievement
from . import AdditionAchievement

class PyAchievement(Achievement):
    "Achievement granted for working on Python files."
    ext = ['py']

class LambdaCalculus(PyAchievement, AdditionAchievement):
    "Because inline function are, like, totally more readable!"
    added = "lambda"

class Fedex(Achievement):
    "Introduce a new Python package."
    name = "FedEx"
    path = ['__init__.py']
    def on_change(self, old, new):
        # file has been added
        return old is None
