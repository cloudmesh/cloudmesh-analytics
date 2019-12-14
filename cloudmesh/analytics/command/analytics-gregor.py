from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.run.background import run

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


def manual(service):
    # Type table
    type_table = {
        'matrix': 'array',
        'array': 'array',
        'array-like': 'array',
        'numpy array': 'array',
        'bool': 'boolean',
        'int': 'integer',
        'float': 'number'
    }
    import sklearn.linear_model
    from cloudmesh.analytics.cms_autoapi import SignatureScraper
    # The module to read
    module = sklearn.linear_model
    # The classes to read from the module
    classes = [service]
    # If type table is specified, it will read all classes in the module
    sigs = SignatureScraper().get_signatures(
        module=module,
        classes=classes,
        type_table=type_table)

    template = service
    template += textwrap.dedent('''
            ==========================================
            {% for i, class in all.items()%}
            analytics {{class.class_name}} {%- for p, type in class.constructor.items() %} [{{p}}=VALUE] {% endfor %}
            {%- for m, paras in class.members.items() %}
            analytics {{class.class_name}} {{m}} {%- for p, type in paras.items()%} [{{p}}=VALUE] {% endfor %}
            {%- endfor %}
            {% endfor %}
            
            ''')

    from jinja2 import Environment, BaseLoader

    t = Environment(loader=BaseLoader).from_string(template)
    res = t.render(all=sigs)
    print(res)
    return ""


class Request(object):

    def __init__(self):
        self.flag = None
        self.data = None
        self.service = None
        self.root_url = None
        self.name = None

    def get_parameters(self, parameters):
        data = {}
        for parameter in parameters:
            attribute, value = parameter.split("=")
            try:
                data[attribute] = json.loads(value)
            except:
                data[attribute] = value
        return data

    @staticmethod
    def run(service, flag, parameters, command, root_url):
        data = Request.get_parameters(parameters)
        name = flag[0]
        url = f'http://{root_url}/{service}_{name}'
        payload = {
            'paras': data
        }
        r = requests.post(url, json=payload)
        return r.text

    @staticmethod
    def simple_run(service, parameters, root_url):
        data = Request.get_parameters(parameters)
        url = f'http://{root_url}/{service}/constructor'
        print('url:', url)
        payload = {
            'paras': data
        }
        r = requests.post(url, json=payload)
        return r.text

    @staticmethod
    def file_upload(parameters, root_url):
        data = Request.get_parameters(parameters)
        url = f'http://{root_url}/file/upload'
        files = {'file': open(data['filename'], 'rb')}
        r = requests.post(url, files=files)
        return r.text

    @staticmethod
    def file_list(parameters, root_url):
        data = Request.get_parameters(parameters)
        url = f'http://{root_url}/file/list'
        r = requests.get(url)
        return r.text

    @staticmethod
    def file_read(parameters, root_url):
        data = Request.get_parameters(parameters)
        print('data:', data)
        filename = data["filename"]
        url = f'http://{root_url}/file/read/{filename}'
        r = requests.get(url)
        return r.text

class AnalyticsCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_analytics(self, args, arguments):
        """
        ::

            Usage:
                analytics codegen sklearn linearmodel [--class_name=VALUE] [--port=PORT]
                analytics server start detached [--cloud=CLOUD] [--class_name=VALUE] [--port=PORT]
                analytics server start [--cloud=CLOUD] [--class_name=VALUE] [--port=PORT]
                analytics server stop [--cloud=CLOUD]
                analytics file upload PARAMETERS...
                analytics file list
                analytics file read PARAMETERS...
                analytics manual SERVICE
                analytics run SERVICE PARAMETERS...
                analytics SERVICE

            This command manages the cloudmesh analytics server on the given cloud.
            If the cloud is not spified it is run on localhost

            Options:
                --cloud=CLOUD  The name of the cloud as specified in the
                                cloudmesh.yaml file

        """
        def set_up_parameters():
            commands = arguments.PARAMETERS
            parameters = []
            flag = []
            for command in commands:
                if '=' in command:
                    parameters.append(command)
                else:
                    flag.append(command)
            print(parameters)
            print(flag)
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)
                # ip = os.path.join(settings['cloud'][settings['cwd.cloud']]['ip'])
                ip = os.path.join(settings['cloud']["localhost"]['ip'])
            return parameters, flag, ip


        setting_path = os.path.join(
            (os.path.dirname(__file__)), 'command_setting.json')

        port = arguments["--port"] or str(8000)

        if arguments.manual:
            manual(arguments.SERVICE)
            return ""

        elif arguments.codegen:
            cms_autoapi.main_generate(arguments['--class_name'], port)

        elif arguments.server and arguments.stop:
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)

            print('killing the server')
            server_pid = settings['server_id']
            os.kill(server_pid, signal.SIGKILL)
            settings['server_id'] = ""

            with open(setting_path, 'w') as new_settings:
                json.dump(settings, new_settings)

        elif arguments.server and arguments.start and arguments.detached and \
            arguments['--cloud']:
            p = subprocess.Popen(
                args=['cms', 'analytics', 'server', 'start',
                      '--cloud=' + arguments['--cloud'],
                      '--class_name='+ arguments['--class_name'],
                      "--port=" + port],
                stdout=False)

            with open(setting_path, 'r') as settings:
                settings = json.load(settings)

            settings['server_id'] = p.pid

            with open(setting_path, 'w') as new_settings:
                json.dump(settings, new_settings)

        elif arguments.run and arguments.SERVICE:
            parameters, flag, ip = set_up_parameters()
            res = Request.run(flag[0], flag[1:], parameters, command, ip)
            print(res)

        elif arguments.file and arguments.upload:
            parameters, flag, ip = set_up_parameters()
            res = Request.file_upload(parameters, ip)
            print(res)

        elif arguments.file and arguments.list:
            parameters, flag, ip = set_up_parameters()

            res = Request.file_list(parameters, ip)
            print(res)

        elif arguments.file and arguments.read:
            parameters, flag, ip = set_up_parameters()
            res = Request.file_upload(parameters, ip)
            print(res)

        # Configure current working server
        if arguments.server and arguments.start and not arguments.detached and \
            arguments['--cloud']:
            settings = None

            with open(setting_path, 'r') as settings:
                settings = json.load(settings)

            settings['cwd.cloud'] = arguments['--cloud']

            with open(setting_path, 'w') as new_settings:
                json.dump(settings, new_settings)

            service = arguments['--class_name']

            build_path = Path(os.path.dirname(__file__))/'../build'
            writefile(f'{build_path}/__init__.py', '')


            #p = f'cloudmesh.analytics.build.{service}_server.Server'
            p = f'cloudmesh.analytics.build'


            # m = __import__(p, fromlist=[f'{service}_server.Server'])

            m = __import__(p)
            m = getattr(getattr(m, 'analytics'), 'build')
            # m = getattr(getattr(getattr(m, 'analytics'), 'build'),f'{service}_server')
            pprint(m.__dict__)
            # eval(f'from cloudmesh.analytics.build.{service}_server import run_app')
            # mod = __import__(f'cloudmesh.analytics.build.{service}_server')

            # server.run_app()

            return
        else:
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)
                # ip = os.path.join(settings['cloud'][settings['cwd.cloud']]['ip'])
                ip = os.path.join(settings['cloud']["localhost"]['ip'])
                print(run_command(arguments, ip))

        if arguments.SERVICE:
            print('hello')
            service = arguments.SERVICE
            parameters, flag, ip = set_up_parameters()
            res = run_command_2(service, [], [], 'simple_run',root_url=ip)
            print(res)

        return ""


