import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

classes = {}

def register(c):
    classes[c.__name__.lower()] = c
    return c


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


from . import resources
from . import catalog