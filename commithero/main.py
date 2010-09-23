from . import application
from .state import RepositoryState
from py.path import local as path
import pickle
import optparse
import itertools

parser = optparse.OptionParser()
parser.add_option("-c", "--cache", metavar="FILE",
    help="resume with data collected in FILE",
    default=".commithero",
)
parser.add_option("-t", "--table",
    help="display achievements by user (default: chronological)",
    action='store_true',
)
parser.add_option("-a", "--all",
    help="display all achievements (default: those new in this run)",
    action='store_true',
)
parser.add_option("-u", "--user", metavar="AUTHOR",
    help="limit achievements to those unlocked by AUTHOR",
)

def main(args=None):
    options, args = parser.parse_args(args)
    assert len(args) == 1, "only expected one repository"
    assert not (options.all and options.table), "-t and -a are exclusive"
    wd = path(args[0])

    # load data from previous runs, if any
    cachefile = wd / options.cache
    state = RepositoryState()
    if cachefile.check():
        state = pickle.load(cachefile.open('rb'))
    previous = len(state.history)

    application.run(wd, state)

    if options.table:
        for user, achievements in state.achievements.iteritems():
            if options.user in (None, user):
                print "%s's achievements:" % user
                for title, desc, commit in achievements:
                    print " * %s - %s. (r%s)" % (title, desc, commit)
    else:
        if options.all:
            history = state.history
        else:
            history = itertools.islice(state.history, previous, None)
        for date, user, (title, desc), commit in history:
            if options.user in (None, user):
                print "[%s] %s unlocked: %s - %s." % (date, user, title, desc)
    # write back
    cachefile.write(pickle.dumps(state), 'wb')
