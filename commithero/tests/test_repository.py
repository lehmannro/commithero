from unittest import TestCase
from commithero.state import Repository
import pickle

class TestRepository(TestCase):
    def test_pickle(self):
        repo = Repository()
        pickle.loads(pickle.dumps(repo))
