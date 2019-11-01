import os
import connexion
import sys
from . import db

print(os.getcwd())
def create_app(test_config=None):
    # create and configure the app
    c_app = connexion.App(__name__, specification_dir="../..")
    c_app.add_api('analytics.yaml')
    c_app.app.config.from_mapping(
        SECRET_KEY='dev',
        #TODO: Instance path requires fix
        DATABASE=os.path.join(c_app.app.instance_path, 'ai_service.sqlite'),
        #TODO: The os.getcwd is changed. the default path need fix
        UPLOAD_FOLDER='../files'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        c_app.app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        c_app.app.config.from_mapping(test_config)

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



# scp -r /server cc@129.114.111.143:/home/cc
