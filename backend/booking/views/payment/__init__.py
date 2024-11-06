from flask import (
    Blueprint, request
)
import time
import random
import logging
from pprint import pformat

logger = logging.getLogger(__name__)

bp = Blueprint('payment', __name__, url_prefix = '/payment')

seed = random.seed()

@bp.route('/', methods=('POST',))
def login_jwt():
    data = request.get_json()
    logger.debug("Payment data:" + pformat(data) )
    delay = random.randrange(1500, 3500)
    time.sleep(delay / 1000)
    return { 
            'status': 'accepted',
            'time': f'{delay/1000}'
    }
    
