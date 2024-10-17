from booking.views.resources import bp
from booking.models import classes
from flask import jsonify, request
import logging
import pprint
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@bp.route('/', methods=['GET'])
def list_resources():
    list = [c.lower() for c in classes ]
    return jsonify(list)
    

@bp.route('/<resource>/<name>', methods=['GET'])
def resources(resource, name):
    logger.debug(f"GET {resource}/{name}")
    logger.debug("classes: " + pprint.pformat(classes))
    if resource not in classes:
        return "Resource not found", 404
    o = classes[resource]()
    o.get(name)
    return jsonify(o.serialize())


@bp.route('/<resource>', methods=['GET'])
def get_all(resource):
    logger.debug(f"GET {resource}")
    if resource not in classes:
        return "Resource not found", 404
    o = classes[resource]()
    return jsonify(o.get_all())
    

@bp.route('/<resource>', methods=['POST'])
def put(resource):
    logger.debug(f"POST {resource}")
    if resource not in classes:
        return "Resource not found", 404
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!', 400
    data = request.json
    logger.debug(pprint.pformat(data))
    o = classes[resource]()
    try:
        id = o.put(**data)
    except Exception as e:
        return str(e), 403
    return jsonify({'id': id})
    
