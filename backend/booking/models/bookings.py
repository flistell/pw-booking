import logging
import pprint
import json
from pprint import pformat
from . import CollectionBase
from . import ResourceBase
from . import protected_resource
from booking.models.resources import User, Users, Item, Items


logger = logging.getLogger("Model")

# Booking statuses
NEW = 'NEW'
BOOKED = 'BOOKED'      # Booked, waiting for payment
CONFIRMED = 'CONFIRMED'   # Payment confirmed
CANCELLED = 'CANCELLED'
ERROR = 'ERROR'


@protected_resource
class Booking(ResourceBase):
    _pkey = 'id'
    _tablename = 'booking'
    _booking_statuses = [NEW, BOOKED, CONFIRMED, CANCELLED, ERROR]

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
            raise ValueError(
                f"Item '{kwargs['booked_item_id']}' not in catalog.")

    def _check_booking_conflict(self, **kwargs):
        logger.debug(type(self).__name__ +
                     f"._check_booking_conflict({kwargs})")
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
        logger.debug(type(self).__name__ + ".save()")
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
            raise ValueError(
                f"Transaction is in incopatible state. Expected BOOKED, found {self._booking_status()}")
        self._data['booking_status'] = CONFIRMED
        ret = self._update_internal(booking_status=CONFIRMED)
        if ret.get('rowcount', 0) != 1:
            self._booking_status(BOOKED)
            raise RuntimeError(
                "Something went wrong while updating booking status.")
        ret = {
            'id': self._id,
            'booking_status': self._data['booking_status']
        }
        self._sync_obj()
        return ret

    def _update_dates(self, **kwargs):
        logger.debug(type(self).__name__ + "._update_dates()")
        logger.debug(pformat(kwargs))
        if not 'booking_start' or not 'booking_end':
            msg = 'booking_start and booking_end are required.'
            logger.error(msg)
            raise ValueError(msg)
        if self._booking_status() == CANCELLED:
            msg = 'Cannot change a cancelled booking.'
            logger.error(msg)
            raise RuntimeError(msg)
        result = self._update_internal(booking_start=kwargs['booking_start'], booking_end=kwargs['booking_end'])
        if result.get('rowcount', 0) != 1:
            self._booking_status(BOOKED)
            raise RuntimeError(
                "Something went wrong while updating booking status.")
        ret = {
            'id': self.get_id(),
            'op': 'UPDATE_BOOKING_DATES',
            'result': 'SUCCESS'
        }
        self._sync_obj()
        return ret

    def update(self, **kwargs):
        logger.debug(type(self).__name__ + ".update(**kwargs)")
        if 'booking_status' in kwargs:
            return self._confirm()
        if 'booking_start' and 'booking_end' in kwargs:
            return self._update_dates(**kwargs)
        raise ValueError("Missing parameters for operation")

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

    def delete(self):
        logger.debug(type(self).__name__ + f".delete()")
        return self._cancel()

    def _cancel(self):
        logger.debug(type(self).__name__ + ".cancel(**kwargs)")
        booking_status_old = self._booking_status()
        self._data['booking_status'] = CANCELLED
        ret_internal = self._update_internal(booking_status=CANCELLED)
        if ret_internal.get('rowcount', 0) != 1:
            self._booking_status(booking_status_old)
            raise RuntimeError(
                "Something went wrong while updating booking status.")
        ret = {
            'id': self._id,
            'user': self._data.get('user_id'),
            'booking_status': self._data['booking_status'],
        }
        return ret


@protected_resource
class Bookings(CollectionBase):
    _tablename = "booking"
    _kind = Booking
    _user_fkey = 'user_id'
    _query_filter = "SELECT * FROM {tablename}"

    _query_filter = """SELECT 
       b.id AS id,
       b.user_id AS user_id,
       b.created,
       b.booked_item_id,
       b.booking_start,
       b.booking_end,
       b.booking_status,
       b.user_id,
       u.username,
       c.item_details
       FROM booking b 
       INNER JOIN userprofile u ON b.user_id = u.id 
       INNER JOIN catalog c ON b.booked_item_id = c.id"""

    def _format(self, data):
        for d in data:
            if 'item_details' in d:
                d['item_details'] = json.loads(d['item_details'])
        return data
