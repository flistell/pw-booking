import jwt
from booking.models.resources import Users
from datetime import datetime, timedelta
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, request, current_app
)
import logging
from pprint import pformat

bp = Blueprint('login', __name__, url_prefix='/login')

logger = logging.getLogger(__name__)


@bp.route('/jwt', methods=('POST',))
def login_jwt():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
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
    return jsonify({
        'id': user.get('id'),
        'username': user.get('username'),
        'common_name': user.get('common_name'),
        'family_name': user.get('family_name'),
        'mail_address': user.get('mail_address'),
        'token': token })


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
