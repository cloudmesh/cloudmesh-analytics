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
        setting_path = os.path.join(
            (os.path.dirname(__file__)), 'command_setting.json')

        port = arguments["--port"] or str(8000)

        if arguments.manual:
            manual(arguments.SERVICE)
            return ""

        if arguments.codegen:
            cms_autoapi.main_generate(arguments['--class_name'], port)

        if arguments.server and arguments.stop:
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)

            print('killing the server')
            server_pid = settings['server_id']
            os.kill(server_pid, signal.SIGKILL)
            settings['server_id'] = ""

            with open(setting_path, 'w') as new_settings:
                json.dump(settings, new_settings)

        if arguments.server and arguments.start and arguments.detached and \
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

        if arguments.run and arguments.SERVICE:
            parameters, flag, ip = set_up_parameters()
            res = run_command_2(flag[0], flag[1:], parameters, "run", root_url=ip)
            print(res)

        if arguments.file and arguments.upload:
            parameters, flag, ip = set_up_parameters()
            res = run_command_2('', flag, parameters, "upload", root_url=ip)
            print(res)

        elif arguments.file and arguments.list:
            parameters, flag, ip = set_up_parameters()
            res = run_command_2('', flag, parameters, "list", root_url=ip)
            print(res)

        elif arguments.file and arguments.read:
            parameters, flag, ip = set_up_parameters()
            res = run_command_2('', flag, parameters, "read", root_url=ip)
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


def run_command(arguments, root_url):
    if arguments.LinearRegression and arguments.fit and (
        arguments['--X'] or arguments['--y'] or arguments[
        '--sample_weight'] or True):
        url = 'http://' + root_url + '/LinearRegression_fit'
        payload = {'paras': {}}

        if arguments['--X'] is not None:
            try:
                payload['paras']['X'] = json.loads(arguments['--X'])
            except:
                payload['paras']['X'] = arguments['--X']

        if arguments['--y'] is not None:
            try:
                payload['paras']['y'] = json.loads(arguments['--y'])
            except:
                payload['paras']['y'] = arguments['--y']

        if arguments['--sample_weight'] is not None:
            try:
                payload['paras']['sample_weight'] = json.loads(
                    arguments['--sample_weight'])
            except:
                payload['paras']['sample_weight'] = arguments['--sample_weight']

        r = requests.post(url, json=payload)
        return r.text

    if arguments.LinearRegression and arguments.get_params and (
        arguments['--deep'] or True):
        url = 'http://' + root_url + '/LinearRegression_get_params'
        payload = {'paras': {}}

        if arguments['--deep'] is not None:
            try:
                payload['paras']['deep'] = json.loads(arguments['--deep'])
            except:
                payload['paras']['deep'] = arguments['--deep']

        r = requests.post(url, json=payload)
        return r.text

    if arguments.LinearRegression and arguments.predict and (
        arguments['--X'] or True):
        url = 'http://' + root_url + '/LinearRegression_predict'
        payload = {'paras': {}}

        if arguments['--X'] is not None:
            try:
                payload['paras']['X'] = json.loads(arguments['--X'])
            except:
                payload['paras']['X'] = arguments['--X']

        r = requests.post(url, json=payload)
        return r.text

    if arguments.LinearRegression and arguments.score and (
        arguments['--X'] or arguments['--y'] or arguments[
        '--sample_weight'] or True):
        url = 'http://' + root_url + '/LinearRegression_score'
        payload = {'paras': {}}

        if arguments['--X'] is not None:
            try:
                payload['paras']['X'] = json.loads(arguments['--X'])
            except:
                payload['paras']['X'] = arguments['--X']

        if arguments['--y'] is not None:
            try:
                payload['paras']['y'] = json.loads(arguments['--y'])
            except:
                payload['paras']['y'] = arguments['--y']

        if arguments['--sample_weight'] is not None:
            try:
                payload['paras']['sample_weight'] = json.loads(
                    arguments['--sample_weight'])
            except:
                payload['paras']['sample_weight'] = arguments['--sample_weight']

        r = requests.post(url, json=payload)
        return r.text

    if arguments.LinearRegression and (
        arguments['--fit_intercept'] or arguments['--normalize'] or arguments[
        '--copy_X'] or arguments['--n_jobs'] or True):
        url = 'http://' + root_url + '/LinearRegression_constructor'
        payload = {'paras': {}}

        if arguments['--fit_intercept'] is not None:
            payload['paras']['fit_intercept'] = json.loads(
                arguments['--fit_intercept'])

        if arguments['--normalize'] is not None:
            payload['paras']['normalize'] = json.loads(arguments['--normalize'])

        if arguments['--copy_X'] is not None:
            payload['paras']['copy_X'] = json.loads(arguments['--copy_X'])

        if arguments['--n_jobs'] is not None:
            payload['paras']['n_jobs'] = json.loads(arguments['--n_jobs'])

        r = requests.post(url, json=payload)
        return r.text

    """
    if arguments.file and arguments.upload and arguments['filename']:
        url = 'http://' + root_url + '/file/upload'
        files = {'file': open(arguments['filename'], 'rb')}
        r = requests.post(url, files=files)
        return r.text

    if arguments.file and arguments.list:
        url = 'http://' + root_url + '/file/list'
        r = requests.get(url)
        return r.text

    if arguments.file and arguments.read and arguments['filename']:
        url = 'http://' + root_url + '/file/read/' + arguments['filename']
        r = requests.get(url)
        return r.text
    """


def run_command_2(service, flag, parameters, command, root_url):
    print(service)
    print(parameters)
    print(flag)

    data = {}
    for parameter in parameters:
        attribute, value = parameter.split("=")
        try:
            data[attribute] = json.loads(value)
        except:
            data[attribute] = value

    if command == "run":
        id = flag[0]
        url = f'http://{root_url}/{service}_{id}'
        print('url:',url)
        payload = {
            'paras': data
        }
        r = requests.post(url, json=payload)
        return r.text
    elif command == "simple_run":
        # url = f'http://{root_url}/{service}_constructor'
        url = f'http://{root_url}/{service}/constructor'
        print('url:',url)
        payload = {
            'paras': data
        }
        r = requests.post(url, json=payload)
        return r.text
    elif command == 'upload':
        url = f'http://{root_url}/file/upload'
        files = {'file': open(data['filename'], 'rb')}
        r = requests.post(url, files=files)
        return r.text

    elif command == 'list':
        url = f'http://{root_url}/file/list'
        r = requests.get(url)
        return r.text

    elif command == 'read':
        print('data:',data)
        filename = data["filename"]
        url = f'http://{root_url}/file/read/{filename}'
        r = requests.get(url)
        return r.text
    else:
        print('Error: Not Support')
