import logging
import pprint
from booking import db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


registered_resources = {}
registered_collections = {}

def resource(c):
    registered_resources[c.__name__.lower()] = c
    return c


def collection(c):
    registered_collections[c.__name__.lower()] = c
    return c


def _dict_factory(cursor, row, mapper=None):
    # sarebbe meglio avere qui un mapper che formatti in modo particolare
    # alcune righe, as esempio item_details come json
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class CollectionBase():
    _db = None
    _pkey = 'id'
    _tablename = 'dual'
    _extra_operations = []
    _kind = None

    def __init__(self):
        logger.debug(type(self).__name__ + ".__init__")
        self._db = db.get_db()
        self._db.row_factory = _dict_factory
        desc = self._db.execute(f"pragma table_info('{self._tablename}')").fetchall()
        self._columns = [d['name'] for d in desc]

    def __call__(self, *args, **kwds):
        logger.debug("args: " + repr(args))
        logger.debug("kwds: " + repr(kwds))
        pass

    def get_all(self, query=None):
        logger.debug(type(self).__name__ + ".get_all();")
        if not query:
            query = f"SELECT * FROM {self._tablename}"
        rows = self._db.execute(query).fetchall()
        return rows

    def get(self, value):
        query = f"SELECT * FROM {self._tablename} WHERE {self._pkey} = {value}"
        logger.debug(f"query = '{query}'")
        resultset = self._db.execute(query).fetchone()
        logger.debug("resultset: " + pprint.pformat(resultset))
        return resultset

    def filter(self, **kwargs):
        logger.debug(type(self).__name__ + f".filter({kwargs});")
        query_prefix = f"SELECT * FROM {self._tablename} WHERE "
        query_where_list = set()
        for p,v in kwargs.items():
            if p in self._columns:
                query_where_list.add(f"{p} LIKE '{v}'")
        query = query_prefix + ' AND '.join(query_where_list)
        logger.debug("query: " + query)
        cursor = self._db.execute(query)
        resultset = cursor.fetchall()
        logger.debug("resultset: " + pprint.pformat(resultset))
        return resultset


class ResourceBase():
    _db = None
    _pkey = 'id'
    _tablename = 'dual'
    _extra_operations = []
    _collection = CollectionBase
    _id = None
    
    def __init__(self, id=None, data=dict()):
        logger.debug(type(self).__name__ + ".__init__")
        self._db = db.get_db()
        self._db.row_factory = _dict_factory
        desc = self._db.execute(
            f"pragma table_info('{self._tablename}')").fetchall()
        self._columns = [d['name'] for d in desc]
        if id and data:
            raise ValueError(
                "'id' and 'data' argument cannot be used together.")
        if id and not data:
            data = self._from_table(id)
            self._data = self._format(data)
            self._id = self._data[self._pkey]
        if data and not id:
            self._data = data
        logger.debug("Created object: " + pprint.pformat(self))

    def _format(self, data):
        return data        

    def _from_table(self, value):
        query = f"SELECT * FROM {self._tablename} WHERE {self._pkey} = {value}"
        logger.debug(f"query = '{query}'")
        resultset = self._db.execute(query).fetchone()
        logger.debug("resultset: " + pprint.pformat(resultset))
        return resultset

    def serialize(self):
        return self._data

    def get_operation(self, op_name):
        logger.debug(f"op_name='{op_name}'")
        if op_name in self._extra_operations:
            return getattr(self, op_name)
        else:
            return None


CollectionBase._kind = ResourceBase

from . import resources
from . import catalog