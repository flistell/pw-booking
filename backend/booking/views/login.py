import jwt
from booking.models.resources import Users
from datetime import datetime, timedelta
from flask import (
    Blueprint, request, jsonify, request, current_app, make_response
)
import logging
from pprint import pformat

bp = Blueprint('login', __name__, url_prefix='/login')

logger = logging.getLogger(__name__)


@bp.route('/jwt', methods=('POST',))
def login_jwt():
    data = request.get_json()
    email = data.get('email')
    user = Users().find(mail_address=email)
    logger.debug(pformat(user))
    if not user or not user.authenticate(password=data['password']):
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    exp =  datetime.utcnow() + timedelta(hours=8)
    token = jwt.encode({
        'sub': user.get('mail_address'),
        'iat': datetime.utcnow(),
        'exp': exp
        },
        key=current_app.config.get('SECRET_KEY'),
        algorithm=current_app.config.get('JWT_ALG')
    )
    logger.debug("token: " + token)
    response = make_response({
        'id': user.get('id'),
        'username': user.get('username'),
        'common_name': user.get('common_name'),
        'family_name': user.get('family_name'),
        'mail_address': user.get('mail_address'),
        'token': token })
    response.set_cookie("Authorization", value=token, domain="localhost")
    logger.debug("response:" + repr(response))
    return response


@bp.route('/authenticate', methods=('POST',))
def login_simple():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = Users().find(mail_address=email)
    logger.debug(pformat(user))
    if not user or not user.authenticate(password=data['password']):
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401
    return jsonify({'authenticated': True})

