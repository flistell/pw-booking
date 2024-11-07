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
    data = request.get_json()
    email = data.get('email')
    user = Users().find(mail_address=email)
    logger.debug(pformat(user))
    if not user or not user.authenticate(password=data['password']):
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    token = jwt.encode({
        'sub': user.get('mail_address'),
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
    logger.debug("token: " + token)
    response = make_response({
        'id': user.get('id'),
        'username': user.get('username'),
        'common_name': user.get('common_name'),
        'family_name': user.get('family_name'),
        'mail_address': user.get('mail_address'),
        'token': token })
    response.set_cookie("Authorization", token)
    logger.debug(response)
    return response
