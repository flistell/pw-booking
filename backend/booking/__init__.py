import os
from flask import Flask
from flask_cors import CORS
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


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

    return app