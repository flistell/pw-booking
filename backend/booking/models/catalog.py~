from booking import db
import logging
import pprint
import json
from . import _dict_factory

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def features(key=None):
    _db = db.get_db()
    _db.row_factory = _dict_factory
    resultset = dict()
    if not key:
        resultset = _db.execute("SELECT distinct(j.KEY) FROM CATALOG c, json_each(item_details) j").fetchall()
    else:
        resultset = _db.execute(f"SELECT * FROM CATALOG c, json_each(item_details, '$.{key})'").fetchall()
    logger.debug(resultset)
    return resultset


def search(**kwargs):
    _db = db.get_db()
    logger.debug("args: " + pprint.pformat(kwargs))
    desc = _db.execute("pragma table_info('catalog')").fetchall()
    columns = [d['name'] for d in desc]
    logger.debug("columns: " + pprint.pformat(columns))

    json_queries = []
    for p,v in kwargs.items():
        if p.startswith('item_detail_'):
            p = p.replace('item_detail_', '')
            json_queries.append(f"json_extract(json(item_details), '$.{p}') LIKE '%{v}%'");
       
    search_query = 'SELECT * FROM catalog WHERE ' + ' AND '.join(json_queries)
  
    logger.debug("query: " + search_query)
    _db.row_factory = _dict_factory
    cursor = _db.execute(search_query)
    resultset = cursor.fetchall()
    logger.debug(pprint.pformat(resultset))
    result = []
    for row in resultset:
        row['item_details'] = json.loads(row['item_details'])
    logger.debug(resultset)  
    return resultset

        