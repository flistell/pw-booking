from booking.views.resources import bp
from booking.models import registered_resources
from booking.models import registered_collections
from flask import jsonify, request
import logging
import pprint

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@bp.route('/', methods=['GET'])
def list_resources():
    list = [c.lower() for c in registered_collections]
    return jsonify(list)
    

@bp.route('/<resource>', methods=['GET'])
def get_all(resource):
    args = request.args.to_dict()
    logger.debug(f"GET {resource} {args}")
    if resource not in registered_collections:
        return "Resource not found", 404
    obj = registered_collections[resource]()
    if not args:
        return jsonify(obj.get_all())
    result = obj.filter(**args)
    return jsonify(result)


@bp.route('/<resource>/<id>', methods=['GET'])
def get_by_id(resource, id):
    args = request.args.to_dict()
    logger.debug(f"GET {resource}/{id} '{args}'")
    if resource not in registered_collections:
        return "Resource not found", 404
    collection = registered_collections[resource]()
    obj = collection.get(id)
    if args:
        func = obj.get_operation(next(iter(args)))
        logger.debug(func)
        if not func:
            return 'Operation not supported!', 400
        result = func(**args)
    else: 
        result = obj.serialize()
    return jsonify(result)


@bp.route('/<resource>', methods=['POST'])
def create(resource):
    logger.debug(f"POST {resource}")
    if resource not in registered_resources:
        return "Resource not found", 404
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!', 400
    data = request.json
    logger.debug(pprint.pformat(data))
    obj = registered_resources[resource]()
    try:
        id = obj.save(**data)
    except Exception as e:
        return str(e), 403
    return jsonify({'id': id})

