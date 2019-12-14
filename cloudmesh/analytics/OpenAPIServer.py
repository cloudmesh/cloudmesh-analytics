"""To create a flask app

The method definition to create a flask app by call ing the create_app function
    Example:
        create_app(test_config)
"""
import os
import connexion
import sys


class OpenAPIServer:
    """
    This is a Conveneinet method to create an OpenAPI server with
    upload ability of files.

    Uasage

        from cloudmesh.analytics.OpenAPIServer import OpenAPIServer

        server = OpenAPIServer(
            host = "127.0.0.1",
            path = ".",
            spec = "server.yaml",
            key = 'dev')
        server.run()


    """

    def __init__(self,
                 host="127.0.0.1",
                 path=".",
                 spec="server.yaml",
                 key='dev'):

        self.path = path
        self.spec = spec
        self.key = key
        self.host = host
        sys.path.append(path)

    def create_app(self, config=None):
        """To create a flask app

        Args:
            config: A dictionary contains the configurations for the flask app

        Return:
            A flask app object
        """

        # ensure the file folder exists
        try:
            os.makedirs(self.path)
        except OSError:
            pass

        _app = connexion.App(__name__, specification_dir=self.path)
        _app.add_api(self.spec)
        _app.app.config.from_mapping(
            SECRET_KEY=self.key,
            #TODO: The os.getcwd is changed. the default path need fix
            UPLOAD_FOLDER=self.path
        )

        if config is None:
            # load the instance config, if it exists, when not testing
            _app.app.config.from_pyfile('config.py', silent=True)
        else:
            # load the test config if passed in
            _app.app.config.from_mapping(config)

        return _app.app

    def app(self):
        self.create_app().run(host=self.host, port=self.port)



