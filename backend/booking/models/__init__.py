import logging
import pprint
from pprint import pformat
from booking import db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

registered_resources = {}
registered_collections = {}
protected_resources = {}
protected_collections = {}

### DECORATORS ###

def resource(c):
    registered_resources[c.__name__.lower()] = c
    return c


def collection(c):
    registered_collections[c.__name__.lower()] = c
    return c


def protected_resource(c):
    registered_resources[c.__name__.lower()] = c
    protected_resources[c.__name__.lower()] = c
    return c


def protected_collection(c):
    registered_collections[c.__name__.lower()] = c
    protected_collections[c.__name__.lower()] = c
    return c


### UTILITY FUNCTIONS ###

def _dict_factory(cursor, row, mapper=None):
    # sarebbe meglio avere qui un mapper che formatti in modo particolare
    # alcune righe, as esempio item_details come json
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


### BASE CLASSES ###

class CollectionBase():
    _db = None
    _pkey = 'id'
    _tablename = 'dual'
    _extra_operations = []
    _kind = object
    _query = "SELECT * FROM {tablename}"
    _user_fkey = 'user_id'

    def __init__(self):
        logger.debug(self.__class__.__name__ + ".__init__")
        self._db = db.get_db()
        self._db.row_factory = _dict_factory
        desc = self._db.execute(
            f"pragma table_info('{self._tablename}')").fetchall()
        self._columns = [d['name'] for d in desc]

    def __call__(self, *args, **kwds):
        logger.debug("args: " + repr(args))
        logger.debug("kwds: " + repr(kwds))
        pass

    def get_all(self):
        logger.debug(self.__class__.__name__ + ".get_all();")
        query = self._query.format(tablename=self._tablename)
        rows = self._db.execute(query).fetchall()
        return rows

    def has(self, id):
        logger.debug(f"{self.__class__.__name__}.has({id});")
        query = f"SELECT id FROM {self._tablename} WHERE id = '{id}'"
        result = self._db.execute(query).fetchone()
        if result:
            return True
        return False

    def new_element(self, **kwargs):
        logger.debug(f"{self.__class__.__name__}.new_element())")
        if self._kind:
            return self._kind(**kwargs)

    def kind(self):
        return self.__class__.__name__

    def get(self, value):
        if self._kind:
            return self._kind(id=value)

    def find(self, **kwargs):
        logger.debug(self.__class__.__name__ + f".filter({kwargs});")
        query_prefix = f"SELECT id FROM {self._tablename} WHERE "
        query_where_list = set()
        for p, v in kwargs.items():
            if p in self._columns:
                query_where_list.add(f"{p} = '{v}'")
        query = query_prefix + ' AND '.join(query_where_list)
        logger.debug("query: " + query)
        cursor = self._db.execute(query)
        resultset = cursor.fetchone()
        logger.debug("resultset: " + pformat(resultset))
        result_obj = self._kind(id=resultset.get('id'))
        return result_obj

    def filter(self, **kwargs):
        logger.debug(self.__class__.__name__ + f".filter({kwargs});")
        query = f"SELECT * FROM {self._tablename} WHERE "
        if 'user' in kwargs:
            query = f"{query} {self._user_fkey} = '{kwargs['user']}'"
        query_where_list = set()
        for p, v in kwargs.items():
            if p in self._columns:
                query_where_list.add(f"{p} LIKE '{v}'")
        query = query + ' AND '.join(query_where_list)
        logger.debug("query: " + query)
        cursor = self._db.execute(query)
        resultset = cursor.fetchall()
        logger.debug("resultset: " + pformat(resultset))
        return resultset

    # def add(self, **kwargs):
    #     logger.debug(self.__class__.__name__ + f".add({kwargs});")
    #     return { 'query': query }


class ResourceBase():
    _db = None
    _pkey = 'id'
    _tablename = 'dual'
    _extra_operations = []
    _collection = CollectionBase
    _id = None
    # _query = "SELECT * FROM {self._tablename} WHERE {self._pkey} = {value}"
    _query = "SELECT * FROM {tablename} WHERE {pkey} = {value}"
    _data = dict()  # contains data to/from table

    def __init__(self, id=None, data=dict()):
        logger.debug(self.__class__.__name__ + ".__init__")
        self._db = db.get_db()
        self._db.row_factory = _dict_factory
        desc = self._db.execute(
            f"pragma table_info('{self._tablename}')").fetchall()
        self._columns = [d['name'] for d in desc]
        if id and data:
            raise ValueError(
                "'id' and 'data' argument cannot be used together.")
        if id and not data:  # Read object from table
            query = self._query.format(
                tablename=self._tablename, pkey=self._pkey, value=id)
            self._data = self._format(self._from_table(id, query))
            self._id = self._data[self._pkey]
            logger.debug("Object read from table: " + pformat(self._data))
        if data and not id:  # New object
            for c in data:
                if c in self._columns:
                    self._data[c] = data[c]
            logger.debug("Created new (unsaved) object: " + pformat(self._data))
        logger.debug("Object: " + pformat(self.serialize()))

    def _format(self, data):
        return data

    def _from_table(self, value, query=None):
        logger.debug("query: " + query)
        resultset = self._db.execute(query).fetchone()
        logger.debug("resultset: " + pformat(resultset))
        return resultset

    def serialize(self):
        return self._data

    def operation(self, op_name):
        logger.debug(f"op_name='{op_name}'")
        if op_name in self._extra_operations:
            return getattr(self, op_name)
        else:
            return None

    def save(self, **kwargs):
        raise NotImplementedError

    def update(self, **kwargs):
        raise NotImplementedError

    def get_id(self):
        return self._id

    def get(self, attribute):
        return self._data.get(attribute, None)


CollectionBase._kind = ResourceBase

from . import resources
from . import bookings