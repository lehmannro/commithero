from . import Achievement

class LambdaCalculus(Achievement):
    "Because inline function are, like, totally more readable!"
    ext = ['py']
    def on_change(self, old, new):
        #XXX moved chunks across files
        return new.count('lambda') - old.count('lambda') > 0

class Fedex(Achievement):
    "Introduce a new Python package."
    name = "FedEx"
    path = ['__init__.py']
    def on_change(self, old, new):
        # file has been added
        return old is None
