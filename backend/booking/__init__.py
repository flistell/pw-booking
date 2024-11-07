import os
from flask import Flask, request
from flask_cors import CORS
from rich.logging import RichHandler
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d %(module)s.%(funcName)s() - %(message)s',
    handlers=[RichHandler()]
    )


DBFILE = '/home/fl118890/Workspace/code/pegaso-labs/project-work/pw-booking/db/booking.sqlite'

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(DBFILE)
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    cors = CORS(app, resources={
        r"/resources/*": {"origins": "*"},
        r"/resources/*/*": {"origins": "*"},
        r"/catalog/*": {"origins": "*"},
        r"/ping/*": {"origins": "*"},
        r"/login/*": {"origins": "*"},
        r"/payment/*": {"origins": "*"},
        })
    
    @app.route('/ping', methods=['GET', 'POST'])
    def ping():
        logging.debug("/ping")
        logging.debug(request.headers)
        h_dict = dict()
        for k,v  in request.headers.items():
            h_dict[k] = v
        payload = ""
        if request.is_json:
            payload = request.get_json()
        else:
            payload = repr(request.get_data())
        response = {
            'request_headers': h_dict,
            'request_cookies': request.cookies,
            'request_payload': payload
        }
        return response


    from . import db
    db.init_app(app)
    
    import booking.views.resources as resources
    app.register_blueprint(resources.bp)
    
    import booking.views.catalog as catalog
    app.register_blueprint(catalog.bp)

    import booking.views.login as login
    app.register_blueprint(login.bp)

    import booking.views.payment as payment
    app.register_blueprint(payment.bp)

    return app