from unittest import TestCase
from commithero.state import Repository
from anyvc.common import repository
import pickle
import datetime

class MockRevision(repository.Revision):
    def __init__(self):
        self.author = "John Doe <info@john.doe>"
        self.id = "1"
        self.message = "Added fake revision."
        self.time = datetime.datetime.now()
        self.parents = []
    def get_changed_files(self):
        return ["foo"]
    def file_content(self, path):
        if path in self.get_changed_files():
            return "lorem ipsum"
        raise IOError
    def exists(self, path):
        return path in self.get_changed_files()

class TestRepository(TestCase):
    def test_afresh(self):
        repo = Repository()
        self.failIf(repo.achievements)
        self.failIf(repo.history)
        self.failIf(repo.visited)
        self.assert_(repo.listeners, "no achievements found")

    def test_pickle_afresh(self):
        repo = Repository()
        pickle.loads(pickle.dumps(repo))

    def test_pickle(self):
        repo = Repository()
        repo.commit(MockRevision())
        restored = pickle.loads(pickle.dumps(repo))
        self.assertEquals(restored.achievements, repo.achievements)
        self.assertEquals(restored.history, repo.history)

    def test_clean_author(self):
        clean = Repository().clean_author
        self.assertEquals(clean("John"), "John")
        self.assertEquals(clean("John Doe"), "John Doe")
        self.assertEquals(clean("John Doe <jdoe@john.doe>"), "John Doe")

    def test_aliases(self):
        repo = Repository()
        clean = repo.clean_author
        aliases = {
            "John <mail@john.doe>": "john",
            "mail@john.doe": "Mr Doe",
            "John": "Jack",
        }
        with repo(aliases):
            self.assertEquals(clean("John <mail@john.doe>"), "john")
            self.assertEquals(clean("Jack <mail@john.doe>"), "Mr Doe")
            self.assertEquals(clean("John <no@e.mail>"), "Jack")
        self.assertEquals(clean("John"), "John")

    def test_history(self):
        repo = Repository()
        repo.commit(MockRevision())
        self.assert_(repo.achievements)
        self.assert_(repo.history)
        self.assert_("John Doe" in repo.achievements)
        self.assert_("John Doe" in repo.history[0])
