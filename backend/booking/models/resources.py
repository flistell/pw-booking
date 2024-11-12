import logging
import pprint
from pprint import pformat
import datetime
import json
from . import CollectionBase
from . import ResourceBase
from . import resource

logger = logging.getLogger(__name__)

@resource
class User(ResourceBase):
    _tablename = "userprofile"

    def authenticate(self, password=None):
        if not password:
            return None
        if password == self._data.get('password', None):
            return True
        return False

    def can_access(self, resource: ResourceBase) -> bool:
        pass
        

@resource
class Users(CollectionBase):
    _tablename = "userprofile"
    _kind = User

@resource
class Item(ResourceBase):
    _pkey = 'id'
    _tablename = 'catalog'
    _extra_operations = [ 'availability' ]
    _query = '''SELECT 
        c.id AS id,
        c.item_type,
        c.item_details,
        l.country,
        l.region,
        l.city,
        l.state,
        l.address_line1,
        l.address_line2,
        l.zip,
        u.username AS owner
        FROM catalog c 
        INNER JOIN location l ON c.item_location_id = l.id 
        INNER JOIN userprofile u ON c.item_owner_id = u.id
        WHERE c.id = {value}'''
    
    def availability(self, interval_from, interval_to, but=None):
        query = f"""
        SELECT 
            booking_start, booking_end 
        FROM booking 
        WHERE 
            booked_item_id = {self.get_id()}
            AND
            booking_status != 'CANCELLED'
            AND
            booking_start > {interval_from}
            AND
            bookind_end < {interval_to}
        """
        if but:
            query = query + f" AND id != {but}"
        cur = self._db.execute(query)
        results = cur.fetchall()
        logger.debug(f"result: '{results}'")
        response = {
            'available': [],
            'unavailable': []
        }
        for r in results:
            logger.debug(pformat(r))
        return {}


    def _format(self, data):
        # sovrascrive il metodo di default per riformattare item_details
        # qui c'è una doppia conversione:
        # - in tabella item_details è un JSON
        # - viene letto dal rowfactory come string
        # - qui lo convertiamo da stringa json a dict
        # - la view flask lo ri-converte in JSON con jsonify()
        data['item_details'] = json.loads(data['item_details'])
        return data


@resource
class Items(CollectionBase):
    _tablename = "catalog"
    _kind = Item
    _query = "select *,c.id AS id FROM catalog c INNER JOIN location l on c.item_location_id = l.id ORDER BY l.city"
   
    def _jsonify(self, data):
        # sovrascrive il metodo di default per riformattare item_details
        # qui c'è una doppia conversione:
        # - in tabella item_details è un JSON
        # - viene letto dal rowfactory come string
        # - qui lo convertiamo da stringa json a dict
        # - la view flask lo ri-converte in JSON con jsonify()
        logger.debug(type(data))
        if isinstance(data, list):
            for row in data:
                row['item_details'] = json.loads(row['item_details'] )
        elif isinstance(data, dict):
            data['item_details'] = json.loads(data['item_details'] )
        return data 
    
    def get_all(self):
        return self._jsonify(super().get_all())
    
    def filter(self, **kwargs):
        logger.debug("args: " + pprint.pformat(kwargs))
        query_where_list = set()
        for p, v in kwargs.items():
            if p.startswith('item_details.'):
                p = p.replace('item_details.', '')
                query_where_list.add(
                    f"json_extract(json(item_details), '$.{p}') LIKE '{v}'")
            if p in self._columns:
                query_where_list.add(f"{p} LIKE '{v}'")

        search_query = 'SELECT * FROM catalog WHERE ' + \
            ' AND '.join(query_where_list)

        logger.debug("query: " + search_query)
        cursor = self._db.execute(search_query)
        resultset = cursor.fetchall()
        logger.debug(pprint.pformat(resultset))
        return self._jsonify(resultset)

        
