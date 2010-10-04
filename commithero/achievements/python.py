from . import Achievement
from . import AdditionAchievement

class LambdaCalculus(AdditionAchievement):
    "Because inline function are, like, totally more readable!"
    ext = ['py']
    added = "lambda"

class Fedex(Achievement):
    "Introduce a new Python package."
    name = "FedEx"
    path = ['__init__.py']
    def on_change(self, old, new):
        # file has been added
        return old is None
