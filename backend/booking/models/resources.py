import logging
import pprint
import datetime
import json
from booking import db
from . import CollectionBase
from . import ResourceBase
from . import resource
from . import collection
from . import _dict_factory

logger = logging.getLogger("Model")
logger.setLevel(logging.DEBUG)


@collection
class Users(CollectionBase):
    _tablename = "userprofile"
    
    # def get(self, username):
    #     self.username = username
    #     self._db = db.get_db()
    #     user_row = self._db.execute(
    #         'SELECT * FROM userprofile u WHERE u.username = ?', (username,)
    #     ).fetchone()
    #     if user_row is not None:
    #         logger.debug(pprint.pformat(user_row))
    #         self.id = user_row['id']
    #         self.password = user_row['password'] 
    #         self.common_name = user_row['common_name']
    #         self.family_name = user_row['family_name']
    #         self.mail_address = user_row['mail_address']
    #         self.tax_id = user_row['tax_id']
    # #         self.payment_method = user_row['payment_method']

    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'username': self.password,
    #         'common_name': self.common_name,
    #         'family_name': self.family_name,
    #         'mail_address': self.mail_address,
    #         'tax_id': self.tax_id,
    #         'payment_method': self.payment_method
    #     }
        
@collection
class Bookings(CollectionBase):
    _tablename = "booking"
    
    def save(self, **kwargs):
        #  TODO: check if car is booked in the same time frame
        sql_booking_conflict = f'''
        select * from booking 
        where 
            booked_item_id = {kwargs['booked_item_id']} and (
                booking_start <= '{kwargs['booking_end']}' 
                or booking_end >= '{kwargs['booking_start']}'
            )
        '''
        logger.debug(f"sql_booking_conflict: '{sql_booking_conflict}'")
        cur = self._db.execute(sql_booking_conflict)
        count = cur.fetchone()
        logger.debug(f"count: '{cur.rowcount}'")
        
        if count:
            logger.warning(f"Specified data is already booked: " + pprint.pformat(count))
            raise ValueError(f"Invalid booking range. Resource {kwargs['booked_item_id']} already booked.")
        
        sql_insert = f'''
        INSERT INTO {self._tablename}
            (user_id, booked_item_id, booking_start, booking_end, booking_status, delivery_address_id)
        VALUES
            (:user_id, :booked_item_id, :booking_start, :booking_end, :booking_status, :delivery_address_id)
        '''
        logger.debug(f"sql_insert: '{sql_insert}'")
        cur = self._db.execute(sql_insert, kwargs)
        self._db.commit()
        cur.close()
        logger.debug(f"insert new row with id: '{cur.lastrowid}'")
        return cur.lastrowid


@resource
class Item(ResourceBase):
    _pkey = 'id'
    _tablename = 'catalog'
    _extra_operations = [ 'is_available' ]
    _query = f"select * FROM catalog c INNER JOIN location l on c.item_location_id = l.id ORDER BY l.city"
    
    def is_available(self, **kwargs):
        query = '''
        SELECT id AS booking_id
        FROM booking 
        WHERE booked_item_id == :item_id
        '''
        cur = self._db.execute(query, {'item_id': self._id})
        result = cur.fetchone()
        logger.debug(f"result: '{result}'")
        available = False
        if not result:
            self._available = True
        return {'id': self._id, 'available': available}

    def _format(self, data):
        # sovrascrive il metodo di default per riformattare item_details
        # qui c'è una doppia conversione:
        # - in tabella item_details è un JSON
        # - viene letto dal rowfactory come string
        # - qui lo convertiamo da stringa json a dict
        # - la view flask lo ri-converte in JSON con jsonify()
        data['item_details'] = json.loads(data['item_details'])
        return data


@collection
class Items(CollectionBase):
    _tablename = "catalog"
    _kind = Item
   
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
    
    def get(self, id):
        obj = Item(id=id)
        return obj
    
    def get_all(self):
        query = f"select * FROM catalog c INNER JOIN location l on c.item_location_id = l.id ORDER BY l.city"
        return self._jsonify(super().get_all(query))
    
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

        
