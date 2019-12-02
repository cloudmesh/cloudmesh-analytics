"""To create a flask app

The method definition to create a flask app by call ing the create_app function
    Example:
        create_app(test_config)
"""
import os
import connexion
import sys

def create_app(config=None):
    """To create a flask app

    Args:
        config: A dictionary contains the configurations for the flask app

    Return:
        A flask app object
    """
    c_app = connexion.App(__name__, specification_dir=".")
    c_app.add_api('analytics.yaml')
    c_app.app.config.from_mapping(
        SECRET_KEY='dev',
        #TODO: The os.getcwd is changed. the default path need fix
        UPLOAD_FOLDER='.'
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
    return c_app.app

if __name__ == "__main__":
    create_app().run(host='0.0.0.0',port=8000)