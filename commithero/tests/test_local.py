from unittest import TestCase
from commithero.state import Repository
from commithero import achievements
from anyvc import repository
from py.path import local as path

class TestAwards(TestCase):
    def setUp(self): #XXX should be setUpClass
        repo = Repository()
        repo.walk(repository.open(path(".")))
        self.ach = [title for title, desc
                    in repo.achievements["Robert Lehmann"]]

    def test_commits(self):
        one_commit = achievements.commits.Commits.goals[1][0]
        self.assert_(one_commit in self.ach)

        five_commits = achievements.commits.Commits.goals[5][0]
        self.assert_(five_commits in self.ach)

    def test_initial_commit(self):
        first_commit = achievements.meta.FoundingFather.name
        self.assert_(first_commit in self.ach)

if __name__ == '__main__':
    import unittest
    unittest.main()
