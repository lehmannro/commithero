from .state import Repository
from anyvc import workdir
from py.path import local as path
from test.test_support import captured_stdout
import pickle
import optparse
import itertools

parser = optparse.OptionParser(usage="[options] [repository]")
parser.add_option("-c", "--cache", metavar="FILE",
    help="resume with data collected in FILE",
    default=".commithero",
)
parser.add_option("-n", "--nocache",
    help="do not consult cache",
    action='store_true',
)
parser.add_option("-p", "--pseudonyms", metavar="FILE",
    help="read pseudonym mappings from FILE",
    default=".names",
)
parser.add_option("-m", "--mercurial",
    help="read pseudonym mappings from .hgchurn",
    action='store_const', dest='pseudonyms', const=".hgchurn",
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
    assert not (options.all and options.table), "-t and -a are exclusive"
    wd = path(args[0] if args else ".")

    repo = Repository()
    # load data from previous runs, if any
    cachefile = wd / options.cache
    if not options.nocache:
        try:
            cache = cachefile.open('rb')
        except IOError:
            pass
        else:
            with cache:
                repo = pickle.load(cache)
    previous = len(repo.history)

    # load aliases from pseudonym file
    aliases = {}
    aliasfile = wd / options.pseudonyms
    try:
        f = aliasfile.open()
    except IOError:
        pass
    else:
        with f:
            for line in f:
                try:
                    alias, actual = line.split('=' in line and '=' or None, 1)
                    aliases[alias.strip()] = actual.strip()
                except ValueError:
                    assert not line.strip(), "malformed alias line: %s" % line

    with captured_stdout(): # anyvc is a little verbose in places
        vcs = workdir.open(wd).repository
        assert vcs, "%s is not a repository" % wd
        with repo(aliases):
            repo.walk(vcs)

    if options.table:
        for user, achievements in repo.achievements.iteritems():
            achievements = sorted(achievements.iteritems(),
                                  key=lambda o: o[1][0])
            if options.user in (None, user):
                print "%s's achievements:" % user
                for (title, desc), (date, commit) in achievements:
                    print " * %s - %s (r%s)" % (title, desc, commit)
    else:
        if options.all:
            history = repo.history
        else:
            history = itertools.islice(repo.history, previous, None)
        for date, user, (title, desc), commit in history:
            if options.user in (None, user):
                print "[%s] %s unlocked: %s - %s" % (date, user, title, desc)
    # write back
    cachefile.write(pickle.dumps(repo), 'wb')

if __name__ == '__main__':
    import sys
    sys.exit(main())
