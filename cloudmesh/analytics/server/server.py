"""To create a flask app

The method definition to create a flask app by call ing the create_app function
    Example:
        create_app(test_config)
"""

import os
import connexion
import sys
from . import db

def create_app(config=None):
    """To create a flask app

    Args:
        config: A dictionary contains the configurations for the flask app

    Return:
        A flask app object
    """
    c_app = connexion.App(__name__, specification_dir="../..")
    c_app.add_api('analytics.yaml')
    c_app.app.config.from_mapping(
        SECRET_KEY='dev',
        #TODO: Instance path requires fix
        DATABASE=os.path.join(c_app.app.instance_path, 'ai_service.sqlite'),
        #TODO: The os.getcwd is changed. the default path need fix
        UPLOAD_FOLDER='../files'
    )

    if config is None:
        # load the instance config, if it exists, when not testing
        c_app.app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        c_app.app.config.from_mapping(config)

    # ensure the instance folder exists
    try:
        os.makedirs(c_app.app.instance_path)
    except OSError:
        pass

    # ensure the file folder exists
    try:
        os.makedirs(c_app.app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    # a simple page that says hello
    @c_app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Register init-db an so on.
    db.init_app(c_app.app)

    return c_app.app