from . import application
from .state import RepositoryState
from py.path import local as path
import pickle
import optparse

parser = optparse.OptionParser()
parser.add_option("-c", "--cache", metavar="file",
    help="resume with data collected in FILE",
    default=".commithero",
)
parser.add_option("-t", "--table",
    help="display achievements by user (default: chronological)",
    action='store_true',
)
parser.add_option("-u", "--user", metavar="author",
    help="limit achievements to those unlocked by AUTHOR",
)

def main(args=None):
    options, args = parser.parse_args(args)
    assert len(args) == 1, "only expected one repository"

    # load data from previous runs, if any
    cachefile = path(options.cache)
    initial = RepositoryState()
    if cachefile.check():
        initial = pickle.load(cachefile.open('rb'))
    previous = len(initial.history)

    state = application.run(path(args[0]), state=initial)

    if options.table:
        for user, achievements in state.achievements.iteritems():
            if options.user in (None, user):
                print "%s's achievements:" % user
                for title, desc, commit in achievements:
                    print " * %s - %s. (r%s)" % (title, desc, commit)
    else:
        for date, user, (title, desc), commit in state.history:
            if options.user in (None, user):
                print "[%s] %s unlocked: %s - %s." % (date, user, title, desc)
    # write back
    cachefile.write(pickle.dumps(state), 'wb')
