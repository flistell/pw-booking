from booking.views.resources import bp
from booking.models import registered_resources
from booking.models import registered_collections
from booking.models import protected_collections
from booking.models.resources import Users, User
from flask import jsonify, request, make_response
import logging  
from pprint import pformat
from booking.security import validate_token

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
    obj = None
    if resource in protected_collections:
        try:
            user_id = validate_token(request)
            logger.debug("Found authenticated user: " + repr(user_id))
            obj = protected_collections[resource]()
            # Istruisco la baking class per filtrare i risultati 
            # usando l'utente autenticato
            result = obj.filter(user=user_id, **args)
        except RuntimeError as e:
            logger.error(e)
            return jsonify({
                'message': repr(e),
                'authenticated': False
            }), 401
    elif resource in registered_collections:
        obj = registered_collections[resource]()
        if args:
            result = obj.filter(**args)
        else:
            result = obj.get_all()
    else:
        return f"Resource '{resource}' not found.", 404
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
        func = obj.operation(next(iter(args)))
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
    if resource not in registered_collections:
        return "Resource not found", 404
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!', 400
    data = request.json
    logger.debug(pformat(data))
    collection = registered_collections[resource]()
    try:
        obj = collection.new_element(data=data)
        logger.debug(pformat(obj))
        logger.debug(pformat(obj.serialize()))
        obj_id = obj.save()
    except Exception as e:
        return str(e), 403
    return jsonify({
            'kind': collection.kind(),
            'id': obj_id})


@bp.route('/<resource>/<id>', methods=['PUT'])
def update(resource, id):
    logger.debug(f"PUT {resource}/{id}")
    if resource not in registered_collections:
        return "Resource not found", 404
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!', 400
    data = request.json
    logger.debug(pformat(data))
    if 'id' not in data:
        return jsonify({}), 500
    collection = registered_collections[resource]()
    logger.debug(collection)
    obj = collection.get(id)
    try:
        obj.update(**data)
    except Exception as e:
        return str(e), 409
    return jsonify({})
