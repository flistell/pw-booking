from booking.views.catalog import bp
from booking.models import catalog
from flask import jsonify, request
import logging
import pprint

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@bp.route('/search', methods=['GET'])
def search_catalog():
    args = request.args.to_dict()
    logger.debug("search args: " + pprint.pformat(args))
    result = catalog.search(**args)
    return jsonify(result)

@bp.route('/features/<name>', methods=['GET'])
def features():
    logger.debug("")
    return jsonify(catalog.features())