from __future__ import print_function
from cloudmesh.shell.command import command, map_parameters
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand, readfile, banner
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.run.background import run
from cloudmesh.analytics.Request import Request
from cloudmesh.analytics.sklearn.manual import sklearn
from cloudmesh.common.Shell import Shell

import importlib

from cloudmesh.analytics.sklearn.manual import manual

from cloudmesh.common.util import writefile
from cloudmesh.analytics import cms_autoapi
import textwrap
import json
import requests
import os
import sys
from pathlib import Path
import subprocess
import signal
from pprint import pprint

sys.path.append(".")


class AnalyticsCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_analytics(self, args, arguments):
        """
        ::

            Usage:
                analytics help FUNCTION
                analytics manual SERVICE
                analytics codegen function FILENAME --service=NAME
                    [--dir=DIR]
                    [--port=PORT]
                    [--host=HOST]
                analytics codegen sklearn MODEL --service=NAME
                    [--port=PORT]
                    [--dir=DIR]
                    [--host=HOST]
                analytics server start --service=NAME
                    [--cloud=CLOUD]
                    [--dir=DIR]
                    [--detached]
                analytics server stop [--service=NAME] [--cloud=CLOUD]
                analytics file upload PARAMETERS...
                analytics file list
                analytics file read PARAMETERS...
                analytics run SERVICE PARAMETERS...
                analytics SERVICE [--cloud=CLOUD] [--port=PORT] [-v]

            This command manages the cloudmesh analytics server on the given cloud.
            If the cloud is not spified it is run on localhost

            Options:
                --cloud=CLOUD  The name of the cloud as specified in the
                                cloudmesh.yaml file

                --dir=DIR      The directory in which the service is to be
                               placed [default=./build]

                --port=PORT    The port of the service [default=8000]

                --host=HOST    The hostname to run this server on
                               [default=127.0.0.1]

                --service=NAME   The name of the service (should than not just
                                    be name?)

            Arguments:

                SERVICE  the name of the service
                PARAMETERS  the PARAMETERS to be send toy the service

            Description:

               http://127.0.0.1:8000/cloudmesh/LinearRegression/ui/
        """

        map_parameters(arguments,
                       'detached',
                       'service',
                       'host',
                       'dir',
                       'cloud',
                       'port',
                       'v')

        port = arguments.port or str(8000)
        ip = f"{arguments.cloud}:{arguments.port}"

        # pprint(arguments)


        def find_server_parameters():
            """
            finds parameters from the commandline arguments. This includes
            any string with an = sign any string without.

            :return: parameters, flags
            """
            commands = arguments.PARAMETERS
            parameters = []
            flag = []
            for command in commands:
                if '=' in command:
                    parameters.append(command)
                else:
                    flag.append(command)

            return parameters, flag


        if arguments.codegen and arguments.function and arguments.FILENAME:

            filename = arguments.FILENAME
            name = arguments.NAME
            module_name = filename.replace(".py", "").replace("/", ".")

            module = importlib.import_module(module_name)
            f = getattr(module, name)
            print(f"from {module_name} import {name}")
            print(f.__doc__)
            print(f.__annotations__)

            return ""

        elif arguments.help:
            function = arguments.FUNCTION
            module, function = function.rsplit(".", 1)
            sklearn.get_help(module, function)
            return ""

        elif arguments.manual:
            print(manual(arguments.SERVICE))
            return ""

        elif arguments.codegen and arguments.sklearn:

            banner("Generate the Cloudmesh OpenAPI Server")

            service = arguments.service
            directory = arguments.dir
            host = arguments.host

            print("  Service:  ", service)
            print("  Directory:", directory)
            print("  Host:     ", host)
            print("  Port:     ", port)
            print()

            cms_autoapi.main_generate(service,
                                      directory,
                                      port)

        elif arguments.server and arguments.stop:
            print('killing the server')
            # os.kill(server_pid, signal.SIGKILL)
            raise NotImplementedError

        elif arguments.run and arguments.SERVICE:
            parameters, flag = find_server_parameters()
            res = Request.run(flag[0], flag[1:], parameters, command, ip)
            print(res)
            return ""


        elif arguments.file and arguments.upload:
            parameters, flag = find_server_parameters()
            res = Request.file_upload(parameters, ip)
            print(res)
            return ""


        elif arguments.file and arguments.list:
            parameters, flag = find_server_parameters()

            res = Request.file_list(parameters, ip)
            print(res)
            return ""


        elif arguments.file and arguments.read:
            parameters, flag = find_server_parameters()
            res = Request.file_upload(parameters, ip)
            print(res)
            return ""

        elif arguments.server and arguments.start and arguments.cloud:

            pprint (arguments)

            service = arguments.service
            directory = arguments.dir

            print("  Service:  ", service)
            print("  Directory:", directory)
            print("  Cloud:    ", arguments.cloud)
            print()

            banner('Manaul')

            print('comamnd to issue the manual')

            print()

            if arguments.detached:

                print ("DETACHED")

                command = [f"python",
                           f"{service}_server.py"]

                pprint(command)

                directory = Path(f"{directory}/{service}").resolve()

                print (directory)

                try:
                    p = subprocess.Popen(args=command, stdout=False, cwd=directory)


                    banner (f"Pid: {p.pid}")

                except Exception as e:
                    if "Address already in use":
                        print()
                        Console.error("The address is already in use")
                        print()

                        name = f"{service}"
                        pid = Shell.get_pid(name)
                        print(pid, name)

                        if pid is not None:
                            Console.error(f"There is also a server running on pid {pid}")

                # with open(setting_path, 'r') as settings:
                #    settings = json.load(settings)
                #
                # settings['server_id'] = p.pid
                #
                # with open(setting_path, 'w') as new_settings:
                #    json.dump(settings, new_settings)

                return ""

            else:

                settings = None

                if arguments.cloud in ['local', '127.0.0.1']:

                    banner('OpenAPI Manual')

                    print('  The Online manaul is available at ')
                    print()
                    print (f"  http://127.0.0.1:{port}/cloudmesh/{service}/ui")
                    print()


                banner(f'Start the Server {service}')

                which = Shell.which("python")
                version = Shell.execute("python", ["--version"])

                command = f'cd {directory}/{service}; python {service}_server.py'
                print()
                print ("  Python :", version, which)
                print ("  Command:", command)
                os.system(command)

            return ""
        else:
            # print(Request.run(arguments, ip))
            print("needs to be fixed")

        if arguments.SERVICE:

            service = arguments.SERVICE
            parameters, flag = find_server_parameters()

            host = arguments.cloud or "127.0.0.1"
            port = arguments.port or 8000

            ip = f"{host}:{port}"

            res = Request.constructor(service, ip, verbose=arguments["-v"])
            print(res)

        return ""
