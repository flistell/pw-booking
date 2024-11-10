import logging  
from flask import jsonify, request, make_response
from pprint import pformat
from booking.views.resources import bp
from booking.models import protected_resources, registered_resources
from booking.models.resources import Users, User
from booking.security import validate_token

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@bp.route('/', methods=['GET'])
def list_resources():
    list = [c.lower() for c in registered_resources]
    return jsonify(list)
  

@bp.route('/<resource>', methods=['GET'])
def get_all(resource):
    args = request.args.to_dict()
    logger.debug(f"GET {resource} {args}")
    collection = None
    if resource in protected_resources:
        try:
            user_obj = validate_token(request)
            logger.debug("Found authenticated user: " + repr(user_obj))
            collection = protected_resources[resource]()
            # Istruisco la baking class per filtrare i risultati 
            # usando l'utente autenticato
            result = collection.filter(user=user_obj.get_id(), **args)
        except RuntimeError as e:
            logger.error(e)
            return jsonify({
                'message': repr(e),
                'authenticated': False
            }), 403
    elif resource in registered_resources:
        collection = registered_resources[resource]()
        if args:
            result = collection.filter(**args)
        else:
            result = collection.get_all()
    else:
        return f"Resource '{resource}' not found.", 404
    return jsonify(result)


@bp.route('/<resource>/<id>', methods=['GET'])
def get_by_id(resource, id):
    args = request.args.to_dict()
    logger.debug(f"GET {resource}/{id} '{args}'")
    if resource not in registered_resources:
        return "Resource not found", 404
    collection = registered_resources[resource]()
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
    if resource not in registered_resources:
        return "Resource not found", 404
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!', 400
    data = request.json
    logger.debug(pformat(data))
    collection = registered_resources[resource]()
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
    if resource not in registered_resources:
        return "Resource not found", 404
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!', 400
    data = request.json
    logger.debug(pformat(data))
    if 'id' not in data:
        return jsonify({}), 500
    collection = registered_resources[resource]()
    logger.debug(collection)
    obj = collection.get(id)
    try:
        obj.update(**data)
    except Exception as e:
        return str(e), 409
    return jsonify({})


@bp.route('/<resource>/<int:id>', methods=['DELETE'])
def delete(resource, id):
    logger.debug(f"DELETE {resource}/{id}")
    if resource not in registered_resources:
        return "Resource not found", 404
    collection = registered_resources[resource]()
    obj = collection.get(id)
    logger.debug(collection)
    if resource in protected_resources:
        try:
            user_obj = validate_token(request)
            logger.debug("Found authenticated user: " + repr(user_obj))
        except RuntimeError as e:
            logger.error(e)
            return jsonify({
                'message': repr(e),
                'authenticated': False
            }), 403 
        if not obj.owned_by(user_obj.get_id()):
            return jsonify({
                'message': f"User {user_obj.get_id()} can't DELETE resource {id}."
            }), 403
    try:
        obj.delete()
    except Exception as e:
        logger.exception(e)
        return str(e), 500
    return jsonify({})


