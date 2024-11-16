import jwt
from booking.models.resources import Users
from datetime import datetime, timedelta
from flask import (
    Blueprint, request, jsonify, request, current_app, make_response
)
import logging
from pprint import pformat

bp = Blueprint('logout', __name__, url_prefix='/logout')

logger = logging.getLogger(__name__)


@bp.route('/', methods=('POST',))
def logout():
    """Logout: non implementata completamente."""
    # Provo a fare logout creando un token non valido
    # ma è una soluzione parziale, non c'è modo (semplice) di dire
    # che un jwt non sia più valido se non è scaduto.
    token = jwt.encode({
        'sub': '',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=-999)},
        current_app.config['SECRET_KEY'])
    logger.debug("token: " + token)
    response = make_response({
        'id': '',
        'token': token })
    response.set_cookie("Authorization", token)
    logger.debug(response)
    return response
