from functools import wraps
import jwt
from flask import jsonify, request, current_app
import logging
logger = logging.getLogger(__name__)


def protected(f):
    @wraps(f)
    def _validate_token(*args, **kwargs):
        auth_cookie = request.cookies.get('Authorization', '')
        logger.debug("auth_cookie" + str(auth_cookie))
        
        if len(auth_cookie) != 2:
            return jsonify({
                'message': 'Invalid token.',
                'authenticated': False
            }, 401)
        try:
            token = auth_cookie[1]
            decoded = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            sub = decoded.get('sub')
            logger.debug("Token Subject: " + sub)
            user = Users.find(mail_address=sub)
            if not user:
                raise RuntimeError("User not found")
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({
                'message': 'Expired token.',
                'authenticated': False
            })
        except (jwt.InvalidTokenError, Exception) as e:
            logger.error(e)
            return jsonify({
                'message': 'Invalid token.',
                'authenticated': False
            }, 401)

