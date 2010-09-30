from unittest import TestCase
from commithero.state import Repository
from anyvc.common import repository
import pickle
import datetime

class MockRevision(repository.Revision):
    "anyvc.common.repository.Revision object with forged data"
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
        "repositories are constructed clean"
        repo = Repository()
        self.failIf(repo.achievements)
        self.failIf(repo.history)
        self.failIf(repo.visited)
        self.assert_(repo.listeners, "no achievements found")

    def test_pickle_afresh(self):
        "pickling of new instances succeeds"
        repo = Repository()
        pickle.loads(pickle.dumps(repo))

    def test_pickle(self):
        "pickling must retain all properties"
        repo = Repository()
        repo.commit(MockRevision())
        restored = pickle.loads(pickle.dumps(repo))
        self.assertEquals(restored.achievements, repo.achievements)
        self.assertEquals(restored.history, repo.history)

    def test_clean_author(self):
        "author cleansing strips off emails"
        clean = Repository().clean_author
        self.assertEquals(clean("John"), "John")
        self.assertEquals(clean("John Doe"), "John Doe")
        # email is discarded by default
        self.assertEquals(clean("John Doe <jdoe@john.doe>"), "John Doe")

    def test_clean_weird(self):
        "weird domains do not make author cleansing trip"
        clean = Repository().clean_author
        # becomes ("John (none)", "john@doe.") when parsed naively
        self.assertEquals(clean("John <john@doe.(none)>"), "John")

    def test_aliases(self):
        "aliases apply by priority"
        repo = Repository()
        clean = repo.clean_author
        aliases = {
            "John <mail@john.doe>": "john", # complete originating address
            "mail@john.doe": "Mr Doe", # only the email
            "John": "Jack", # only the username
        } # in that order of priority
        with repo(aliases):
            self.assertEquals(clean("John <mail@john.doe>"), "john")
            self.assertEquals(clean("Jack <mail@john.doe>"), "Mr Doe")
            self.assertEquals(clean("John <no@e.mail>"), "Jack")
        # aliases do not apply outside of context
        self.assertEquals(clean("John"), "John")

    def test_history(self):
        "achievements are tracked"
        repo = Repository()
        repo.commit(MockRevision())
        self.failIf(repo.visited) # only populated by Repository.walk
        self.assert_("John Doe" in repo.achievements)
        self.assert_("John Doe" in repo.history[0])
