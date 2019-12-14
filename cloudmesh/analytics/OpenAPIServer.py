"""To create a flask app

The method definition to create a flask app by call ing the create_app function
    Example:
        create_app(test_config)
"""
import os
import connexion
import sys
import textwrap
from cloudmesh.common.util import writefile

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
            key = "dev")
        server.run()

    In case you like to specify a program that contains such a server you can
    use

        server = OpenAPIServer(
            host = "127.0.0.1",
            path = ".",
            spec = "server.yaml",
            key = "dev")
        server.write("server.py")


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
        """
        Creates the server while using the config file. In addition some
        configuration parameters are used that are defined at instantiation time.

        :param config: parameters passed to the flas server

        :return: a flas server
        """

        # ensure the file folder exists
        try:
            os.makedirs(self.path)
        except OSError:
            pass

        # Setup the server
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
        """
        Starts the server

        """
        self.create_app().run(host=self.host, port=self.port)


    def __str__(self):
        """
        returns the Server as a python program string
        :return:
        """

        program = textwrap.dedent(
            f"""
            from cloudmesh.analytics.OpenAPIServer import OpenAPIServer
    
            server = OpenAPIServer(
                host = f"{self.host}",
                path = f"{self.path}",
                spec = f"{self.spec}",
                key = f"{self.key}")
            server.app()

            """)
        return program


    def write(self, filename):
        """
        Writes a python program into the filename that contains the server
        details. This fil can be started and will run an OpenAPI server

        :param filename:
        :return:
        """
        content = self.__str__()
        writefile(filename, content)


