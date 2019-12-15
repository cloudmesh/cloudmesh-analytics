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
                analytics codegen sklearn MODEL --service=SERVICE
                    [--port=PORT]
                    [--dir=DIR]
                    [--host=HOST]
                analytics server start --service=SERVICE
                    [--cloud=CLOUD]
                    [--dir=DIR]
                    [--detached]
                analytics server stop [--service=SERVICE] [--cloud=CLOUD]
                analytics file upload PARAMETERS...
                analytics file list
                analytics file read PARAMETERS...
                analytics run SERVICE PARAMETERS...
                analytics SERVICE

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

                --class_name=NAME   The name of the service (should than not just
                                    be name?)

            Arguments:

                SERVICE  the name of the service
                PARAMETERS  the PARAMETERS to be send toy the service

        """

        map_parameters(arguments,
                       'service',
                       'host',
                       'dir',
                       'cloud',
                       'port')

        # pprint(arguments)

        def find_server_parameters():
            """
            finds parameters from the commandline arguments. This includes
            any string with an = sign any string without.

            TODO: FIX:

            There is alos an undocumented hardcoded configuration json file
            which should actually be a yaml file and should be able to be passed
            as a parameter or placed into the buld dir.

            :return: parameters, flgs, ip
            """
            commands = arguments.PARAMETERS
            parameters = []
            flag = []
            for command in commands:
                if '=' in command:
                    parameters.append(command)
                else:
                    flag.append(command)
            #
            # I DO NOT KNOW WHAT THE NEXT STUFF IS?
            #
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)
                ip = os.path.join(settings['cloud']["localhost"]['ip'])

            return parameters, flag, ip

        setting_path = os.path.join(
            (os.path.dirname(__file__)), 'command_setting.json')

        port = arguments.port or str(8000)

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
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)

            print('killing the server')
            server_pid = settings['server_id']
            os.kill(server_pid, signal.SIGKILL)
            settings['server_id'] = ""

            with open(setting_path, 'w') as new_settings:
                json.dump(settings, new_settings)

        elif arguments.run and arguments.SERVICE:
            parameters, flag, ip = find_server_parameters()
            res = Request.run(flag[0], flag[1:], parameters, command, ip)
            print(res)

        elif arguments.file and arguments.upload:
            parameters, flag, ip = find_server_parameters()
            res = Request.file_upload(parameters, ip)
            print(res)

        elif arguments.file and arguments.list:
            parameters, flag, ip = find_server_parameters()

            res = Request.file_list(parameters, ip)
            print(res)

        elif arguments.file and arguments.read:
            parameters, flag, ip = find_server_parameters()
            res = Request.file_upload(parameters, ip)
            print(res)


        elif arguments.server and arguments.start and arguments.detached and \
            arguments.cloud:
            p = subprocess.Popen(
                args=['cms',
                      'analytics',
                      'server',
                      'start',
                      f'--cloud={arguments.cloud}',
                      f'--class_name={arguments.class_name}',
                      f"--port={port}"],
                stdout=False)

            # with open(setting_path, 'r') as settings:
            #    settings = json.load(settings)
            #
            # settings['server_id'] = p.pid
            #
            # with open(setting_path, 'w') as new_settings:
            #    json.dump(settings, new_settings)


        if arguments.server and arguments.start and not arguments.detached and \
            arguments.cloud:
            settings = None

            directory = arguments.dir
            service = arguments.service

            if arguments.cloud in ['local', '127.0.0.1']:

                banner('Manaul')

                print('comamnd to issue the manual')

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
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)
                # ip = os.path.join(settings['cloud'][settings['cwd.cloud']]['ip'])
                ip = os.path.join(settings['cloud']["localhost"]['ip'])
                # print(Request.run(arguments, ip))
                print("needs to be fixed")

        if arguments.SERVICE:
            service = arguments.SERVICE
            parameters, flag, ip = find_server_parameters()
            res = Request.simple_run(service, parameters, ip)
            print(res)

        return ""
