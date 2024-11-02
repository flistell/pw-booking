import os
from flask import Flask
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
        r"/catalog/*": {"origins": "*"},
        r"/ping/*": {"origins": "*"},
        r"/login/*": {"origins": "*"}
        })
    
    @app.route('/ping')
    def ping():
        return 'pong!'


    from . import db
    db.init_app(app)
    
    import booking.views.resources as resources
    app.register_blueprint(resources.bp)
    
    import booking.views.catalog as catalog
    app.register_blueprint(catalog.bp)

    import booking.views.login as login
    app.register_blueprint(login.bp)

    return app