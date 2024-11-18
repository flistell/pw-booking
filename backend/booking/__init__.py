import os
import logging
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from rich.logging import RichHandler

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d %(module)s.%(funcName)s() - %(message)s',
    handlers=[RichHandler()]
    )


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    app.config.from_mapping(
        SECRET_KEY='dev',
        JWT_ALG='HS256',
        DATABASE=os.path.join(os.environ.get('DBFILE','../db/booking.sqlite')),
        DOMAIN=os.environ.get('COOKIE_DOMAIN', 'localhost')
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
        r"/resources/*": {"origins": ["http://localhost:5173", "http://localhost:8000", "http://socialauto.ddns.net"]},
        r"/resources/*/*": {"origins": ["http://localhost:5173", "http://localhost:8000", "http://socialauto.ddns.net"]},
        r"/catalog/*": {"origins": ["http://localhost:5173", "http://localhost:8000", "http://socialauto.ddns.net"]},
        r"/ping/*": {"origins": ["http://localhost:5173", "http://localhost:8000", "http://socialauto.ddns.net"]},
        r"/login/*": {"origins": ["http://localhost:5173", "http://localhost:8000", "http://socialauto.ddns.net"]},
        },
        supports_credentials=True)
    
    @app.route('/ping', methods=['GET', 'POST'])
    def ping():
        logging.debug("/ping")
        logging.debug(request.headers)
        logging.debug(request.cookies)
        h_dict = dict()
        for k,v  in request.headers.items():
            h_dict[k] = v
        c_dict = dict()
        for k,v in request.cookies.items():
            c_dict[k] = v
        payload = ""
        if request.is_json:
            payload = request.get_json()
        else:
            payload = repr(request.get_data())
        response = {
            'request_headers': h_dict,
            'request_cookies': c_dict,
            'request_payload': payload
        }
        return response

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

    from . import db
    db.init_app(app)
    
    import booking.views.resources as resources
    app.register_blueprint(resources.bp)
    
    #import booking.views.catalog as catalog
    #app.register_blueprint(catalog.bp)

    import booking.views.login as login
    app.register_blueprint(login.bp)

    #import booking.views.payment as payment
    #app.register_blueprint(payment.bp)

    return app
