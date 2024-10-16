from booking.views.resources import bp
from booking.models import classes
from flask import jsonify, request
import logging
import pprint

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@bp.route('/<resource>/<name>', methods=['GET'])
def resources(resource, name):
    logger.debug(f"{resource}/{name}")
    logger.debug("classes: " + pprint.pformat(classes))
    if resource not in classes:
        return "Resource not found", 404
    o = classes[resource]()
    o.get(name)
    return jsonify(o.serialize())

