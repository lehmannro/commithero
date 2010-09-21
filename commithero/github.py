"""
Github Post-Receive Hooks

"""

from anyvc.common.repository import Revision
import json
import BaseHTTPServer
from datetime import datetime

class JSONRevision(Revision):
    """Adapt a Github Post-Receive Hook payload to an anyvc revision.

    They look like this::

       {
       "id": "41a212ee83ca127e3c8cf465891ab7216a705f59",
       "url": "http://github.com/defunkt/github/commit/41a2...",
       "author": {
           "email": "chris@ozmm.org",
           "name": "Chris Wanstrath"
       },
       "message": "okay i give in",
       "timestamp": "2008-02-15T14:57:17-08:00",
       "added": ["filepath.rb"]
       }

    """
    def __init__(self, data):
        self.id = data['id']
        self.author = data['author']['name']
        self.time = datetime.strptime(data['timestamp'],
                                      "%Y-%m-%dT%H:%M:%S%z")
        self.parents = ["bogus"] #XXX Revision objects
        self.message = data["message"]
        changed = set(data.get('added', []) + data.get('removed', [])
                      + data.get('modified', []))
        self.get_changed_files = lambda self: changed

def post_receive_hook(payload):
    data = json.loads(payload)
    cachefile = path(options.cache)
    if cachefile.check():
        initial = pickle.load(cachefile.open('rb'))
    state = application.run(path(args[0]), state=initial)
    cachefile.write(pickle.dumps(state), 'wb')
    commits = set()
    for commit in data['commits']:
        if commit not in state.visited:
            commits.add(JSONRevision(commit))

    for commit in sorted(commits, key=operator.attrgetter('time')):
        pass

class Ping(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        post_receive_hook(self.rfile.read())

def serve():
    import sys; sys.argv = ['']
    BaseHTTPServer.test(HandlerClass = Ping)
