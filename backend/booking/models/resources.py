from booking import db
from . import register
import logging
import pprint
import uuid
from . import _dict_factory
import datetime

logger = logging.getLogger("Model")
logger.setLevel(logging.DEBUG)


class Resource():
    _db = None
    _tablename = 'dual'

    def __init__(self):
        logger.debug(type(self).__name__ + ".__init__")
        self._db = db.get_db()
        self._db.row_factory = _dict_factory


    def __call__(self, *args, **kwds):
        logger.debug("args: " + repr(args))
        logger.debug("kwds: " + repr(kwds))
        pass

    def get_all(self):
        logger.debug(type(self).__name__ + ".get_all();")
        rows = self._db.execute(
            f"SELECT * FROM {self._tablename}"
        ).fetchall()
        return rows
        
    def get(self, key, value):
        query = f"SELECT * FOMR f{self._tablename} WHERE f{key} = f{value}"
        logger.debug(f"query = '{query}'")
        resultset = self._db.execute(query).fetchone()
        logger.debug("result = " + pprint.pprint(resultset))
        return resultset
        
    def serialize(self):
        import json
        return json.dumps(self)


@register
class User(Resource):
    _table_name = "userprofile"
    
    def get(self, username):
        self.username = username
        self._db = db.get_db()
        user_row = self._db.execute(
            'SELECT * FROM userprofile u WHERE u.username = ?', (username,)
        ).fetchone()
        if user_row is not None:
            logger.debug(pprint.pformat(user_row))
            self.id = user_row['id']
            self.password = user_row['password'] 
            self.common_name = user_row['common_name']
            self.family_name = user_row['family_name']
            self.mail_address = user_row['mail_address']
            self.tax_id = user_row['tax_id']
            self.payment_method = user_row['payment_method']

    def serialize(self):
        return {
            'id': self.id,
            'username': self.password,
            'common_name': self.common_name,
            'family_name': self.family_name,
            'mail_address': self.mail_address,
            'tax_id': self.tax_id,
            'payment_method': self.payment_method
        }
        
@register
class Booking(Resource):
    _tablename = "booking"
    
    def put(self, **kwargs):
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
