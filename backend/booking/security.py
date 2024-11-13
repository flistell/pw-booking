import jwt
from flask import jsonify, current_app
import logging
from booking.models.resources import Users, User

logger = logging.getLogger(__name__)


def validate_token(request):
    auth_cookie = request.cookies.get('Authorization', '')
    if not auth_cookie:
        logger.error('Missing Authorization cookie.')
        raise ValueError('Missing Authorization cookie.')
    logger.debug("auth_cookie: " + str(auth_cookie))
    try:
        token = auth_cookie
        decoded = jwt.decode(
            token, 
            key=current_app.config.get('SECRET_KEY'),
            algorithms=current_app.config.get('JWT_ALG')
        )
        logger.debug("Decoded JWT:" + repr(decoded))
        sub = decoded.get('sub')
        logger.debug("Token Subject: " + sub)
        user = Users().find(mail_address=sub)
        if not user:
            raise RuntimeError("User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise RuntimeError('Expired token.')
    except (jwt.InvalidTokenError, Exception) as e:
        logger.error(e)
        raise RuntimeError('Invalid token.')

