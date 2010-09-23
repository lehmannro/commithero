from anyvc import repository
from collections import deque
import operator

def run(repo, state, synonyms):
    """Examine a repository for new commits."""
    visited = state.visited
    repo = repository.open(repo)
    head = repo.get_default_head()
    if head.id in state.visited:
        return # no commits since last run

    # fetch all unvisited revisions
    queue = deque([head]) # traverse from HEAD
    revisions = deque() # strictly a subset of `visited`
    while queue:
        revision = queue.pop() # goes depth-first
        revisions.append(revision)
        visited.add(revision.id)
        queue.extend(parent for parent in revision.parents
                     if parent.id not in visited)

    # now commit all new revisions in order
    with state(synonyms):
        for revision in sorted(revisions, key=operator.attrgetter('time')):
            state.commit(revision)
