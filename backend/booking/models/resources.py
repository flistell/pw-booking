import logging
import pprint
from pprint import pformat
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

# Booking statues
NEW = 'NEW'
BOOKED = 'BOOKED'      # Booked, waiting for payment
CONFIRMED = 'CONFIRMED'   # Payment confirmed
CANCELLED = 'CANCELLED' 
ERROR = 'ERROR' 


@resource
class User(ResourceBase):
    _tablename = "userprofile"

    def authenticate(self, password=None):
        if not password:
            return None
        if password == self._data.get('password', None):
            return True
        return False


@collection
class Users(CollectionBase):
    _tablename = "userprofile"
    _kind = User


@resource
class Booking(ResourceBase):
    _pkey = 'id'
    _tablename = 'booking'
    _booking_statuses = [ NEW, BOOKED, CONFIRMED, CANCELLED, ERROR]
    
    def _booking_status(self, new_status=None):
        if new_status and new_status in self._booking_statuses:
            self._data['booking_status'] = new_status
        return self._data.get('booking_status', None)
    
    def _check_parameters(self, **kwargs):
        logger.debug(type(self).__name__ + f"._check_parameters({kwargs})")
        args_keys = kwargs.keys()
        missing = set()
        for required_attr in ['user_id', 'booked_item_id', 'booking_end', 'booking_start']:
            if required_attr not in args_keys:
                missing.add(required_attr)
        if len(missing) > 0:
            raise ValueError("Missing parameters: " + repr(missing))

    def _check_user(self, **kwargs):
        logger.debug(type(self).__name__ + f"._check_user({kwargs})")
        users = Users()
        if not users.has(kwargs['user_id']):
            raise ValueError(f"User '{kwargs['user_id']}' not registered.")
    
    def _check_item(self, **kwargs):
        logger.debug(type(self).__name__ + f".check_item({kwargs})")
        items = Items()
        if not items.has(kwargs['booked_item_id']):
            raise ValueError(f"Item '{kwargs['booked_item_id']}' not in catalog.")

    def _check_booking_conflict(self, **kwargs):
        logger.debug(type(self).__name__ + f"._check_booking_conflict({kwargs})")
        sql_booking_conflict = f'''
        select * from {self._tablename} 
        where 
            booked_item_id = {kwargs['booked_item_id']} and (
                booking_start <= '{kwargs['booking_end']}' 
                or booking_end >= '{kwargs['booking_start']}'
            )
        '''
        logger.debug(f"sql_booking_conflict: '{sql_booking_conflict}'")
        count = self._db.execute(sql_booking_conflict).fetchone()
        if count:
            logger.warning(
                f"Specified data is already booked: " + pprint.pformat(count))
            raise ValueError(
                f"Invalid booking range. Resource {kwargs['booked_item_id']} already booked.")

    def save(self):
        logger.debug(type(self).__name__ + ".create()")
        self._check_parameters(**self._data)
        self._check_user(**self._data)
        self._check_item(**self._data)
        self._check_booking_conflict(**self._data)
        if not self._booking_status():
            self._booking_status(BOOKED)
        
        sql_insert = f'''
        INSERT INTO {self._tablename}
            (user_id, booked_item_id, booking_start, booking_end, booking_status )
        VALUES
            (:user_id, :booked_item_id, :booking_start, :booking_end, :booking_status)
        '''
        logger.debug(f"sql_insert: '{sql_insert}'")
        cur = self._db.execute(sql_insert, self._data)
        self._db.commit()
        self._id = cur.lastrowid
        cur.close()
        logger.debug(f"insert new row with id: '{self._id}'")
        return self._id

    def _confirm(self):
        logger.debug(type(self).__name__ + ".confirm()")
        logger.debug("Booking object: " + pformat(self._data))
        if self._booking_status() != BOOKED:
            raise ValueError(f"Transaction is in incopatible state. Expected BOOKED, found {self._booking_status()}")
        self._data['booking_status'] = CONFIRMED
        ret = self._update_internal(booking_status=CONFIRMED)
        if ret.get('rowcount', 0) != 1:
            self._booking_status(BOOKED)
            raise RuntimeError("Something wen wrong while updating booking status.") 
        ret = {
            'id': self._id,
            'booking_status': self._data['booking_status']
        }
        return ret

    def update(self, **kwargs):
        logger.debug(type(self).__name__ + ".update(**kwargs)")
        return self._confirm();

    def _update_internal(self, **kwargs):
        logger.debug(type(self).__name__ + "._update_internal(**kwargs)")
        params_list = [] 
        for p, v in kwargs.items():
            params_list.append(f"{p} = '{v}'")
        params = ','.join(params_list)
        logger.debug(params)
        
        sql_update = f'''
            UPDATE {self._tablename} 
            SET {params}
            WHERE id = {self._id}
        '''
        logger.debug(f"sql_update: {sql_update}")
        cur = self._db.execute(sql_update, self._data)
        self._db.commit()
        cur.close()
        ret = {
            'rowcount': cur.rowcount,
        }
        logger.debug(f"updated '{cur.rowcount}' rows.")
        return ret

    def _update_all(self):
        logger.debug(type(self).__name__ + ".update_all()")

        sql_update = f'''
        UPDATE {self._tablename} 
        SET
            user_id = :user_id,
            booked_item_id =  :booked_item_id,
            booking_start = :booking_start,
            booking_end = :booking_end,
            booking_status = :booking_status,
            delivery_address_id = :deivery_address_id
        WEHERE id = :id
        '''
        logger.debug(f"sql_update: '{sql_update}'")
        cur = self._db.execute(sql_update, self._data)
        self._db.commit()
        cur.close()
        ret = {
            'rowcount': cur.rowcount,
        }
        logger.debug(f"updated '{cur.rowcount}' rows.")
        return ret


@collection
class Bookings(CollectionBase):
    _tablename = "booking"
    _kind = Booking


@resource
class Item(ResourceBase):
    _pkey = 'id'
    _tablename = 'catalog'
    _extra_operations = [ 'is_available' ]
    _query = "select *,c.id AS id FROM catalog c INNER JOIN location l on c.item_location_id = l.id WHERE c.id = {value}"
    
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

        
