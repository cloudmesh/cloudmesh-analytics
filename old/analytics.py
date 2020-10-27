from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.analytics.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.run.background import run

from cloudmesh.analytics import cms_autoapi

import json
import requests
import os
import subprocess
import signal


class AnalyticsCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_analytics(self, args, arguments):
        """
        ::

            Usage:
                analytics codegen sklearn linearmodel [--class_name=VALUE] [--port=PORT]
                analytics server start [--cloud=CLOUD]
                analytics server start detached [--cloud=CLOUD]
                analytics server stop [--cloud=CLOUD]
                analytics file upload [--filename=FILENAME]
                analytics file list
                analytics file read [--filename=FILENAME]
                analytics LinearRegression[--fit_intercept=VALUE] [--normalize=VALUE] [--copy_X=VALUE] [--n_jobs=VALUE] 
                analytics LinearRegression fit [--X=VALUE]  [--y=VALUE]  [--sample_weight=VALUE] 
                analytics LinearRegression get_params [--deep=VALUE] 
                analytics LinearRegression predict [--X=VALUE] 
                analytics LinearRegression score [--X=VALUE]  [--y=VALUE]  [--sample_weight=VALUE] 
                

            This command manages the cloudmesh analytics server on the given cloud.
            If the cloud is not spified it is run on localhost

            Options:
                --cloud=CLOUD  The name of the cloud as specified in the
                                cloudmesh.yaml file

        """
        setting_path = os.path.join(
            (os.path.dirname(__file__)), 'command_setting.json')

        port = arguments["--port"] or 8000

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
                      '--cloud=' + arguments['--cloud']],
                stdout=False)

            with open(setting_path, 'r') as settings:
                settings = json.load(settings)

            settings['server_id'] = p.pid

            with open(setting_path, 'w') as new_settings:
                json.dump(settings, new_settings)

        # Configure current working server
        if arguments.server and arguments.start and not arguments.detached and \
            arguments['--cloud']:
            settings = None
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)

            settings['cwd.cloud'] = arguments['--cloud']

            with open(setting_path, 'w') as new_settings:
                json.dump(settings, new_settings)

            from cloudmesh.analytics.build import server
            server.run_app()
        else:
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)
                # ip = os.path.join(settings['cloud'][settings['cwd.cloud']]['ip'])
                ip = os.path.join(settings['cloud']["localhost"]['ip'])
                print(run_command(arguments, ip))

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

    if arguments.file and arguments.upload and arguments['--filename']:
        url = 'http://' + root_url + '/file/upload'
        files = {'file': open(arguments['--filename'], 'rb')}
        r = requests.post(url, files=files)
        return r.text

    if arguments.file and arguments.list:
        url = 'http://' + root_url + '/file/list'
        r = requests.get(url)
        return r.text

    if arguments.file and arguments.read and arguments['--filename']:
        url = 'http://' + root_url + '/file/read/' + arguments['--filename']
        r = requests.get(url)
        return r.text
