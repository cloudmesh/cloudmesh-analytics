from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.analytics.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.run.background import run

from cloudmesh.analytics import cms_autoapi

import json
import subprocess
import requests
import os

LOCAL_UPLOAD_FOLDER = "D:/IUBLife/2019Fall/cloudM/cloudmesh-analytics/tests/test_uploaded_files"

class AnalyticsCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_analytics(self, args, arguments):
        """
        ::

            Usage:
                analytics codegen sklearn linearmodel [--class_name=VALUE] [--port=PORT]
                analytics server start [--cloud=CLOUD]
                analytics server stop [--cloud=CLOUD]
                analytics file upload [--filename=FILENAME]
                analytics file list
                analytics file read [--filename=FILENAME]
                analytics LogisticRegression[--penalty=VALUE] [--dual=VALUE] [--tol=VALUE] [--C=VALUE] [--fit_intercept=VALUE] [--intercept_scaling=VALUE] [--class_weight=VALUE] [--random_state=VALUE] [--solver=VALUE] [--max_iter=VALUE] [--multi_class=VALUE] [--verbose=VALUE] [--warm_start=VALUE] [--n_jobs=VALUE] [--l1_ratio=VALUE] 
                analytics LogisticRegression decision_function [--X=VALUE] 
                analytics LogisticRegression densify
                analytics LogisticRegression fit [--X=VALUE]  [--y=VALUE]  [--sample_weight=VALUE] 
                analytics logisticRegression get_params [--deep=VALUE]
                analytics LogisticRegression predict [--X=VALUE] 
                analytics LogisticRegression predict_log_proba [--X=VALUE] 
                analytics LogisticRegression predict_proba [--X=VALUE] 
                analytics LogisticRegression score [--X=VALUE]  [--y=VALUE]  [--sample_weight=VALUE] 
                analytics LogisticRegression sparsify
                analytics LogisticRegression get_properties [--name=VALUE] 
                

            This command manages the cloudmesh analytics server on the given cloud.
            If the cloud is not spified it is run on localhost

            Options:
                --cloud=CLOUD  The name of the cloud as specified in the
                                cloudmesh.yaml file

        """
        VERBOSE(arguments)

        setting_path = os.path.join(
            (os.path.dirname(__file__)), 'command_setting.json')

        if arguments.codegen:
            cms_autoapi.main_generate(arguments['--class_name'], int(arguments['--port']))

        # Configure current working server
        if arguments.server and arguments.start and arguments['--cloud']:
            settings = None
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)

            settings['cwd.cloud'] = arguments['--cloud']

            with open(setting_path, 'w') as new_settings:
                json.dump(settings, new_settings)

            # from cloudmesh.analytics.build import server
            # server.run_app()
            subprocess.run(['sh', 'docker_build_run_commands.sh'])

        else:
            with open(setting_path, 'r') as settings:
                settings = json.load(settings)
                # ip = os.path.join(settings['cloud'][settings['cwd.cloud']]['ip'])
                ip = os.path.join(settings['cloud']["localhost"]['ip'])
                print(run_command(arguments, ip))

        return ""

def run_command(arguments, root_url):
    
    if arguments.LogisticRegression and arguments.decision_function and ( arguments['--X'] or  True):
        url = 'http://' + root_url + '/LogisticRegression_decision_function'
        payload = {'paras': {}}
        
        if arguments['--X'] is not None:
            try:
                payload['paras']['X']= json.loads(arguments['--X'])
            except:
                payload['paras']['X']= arguments['--X']
        
        r = requests.post(url, json=payload)
        return r.text
    
    if arguments.LogisticRegression and arguments.densify and ( True):
        url = 'http://' + root_url + '/LogisticRegression_densify'
        payload = {'paras': {}}
        
        r = requests.post(url, json=payload)
        return r.text
    
    if arguments.LogisticRegression and arguments.fit and ( arguments['--X'] or  arguments['--y'] or  arguments['--sample_weight'] or  True):
        url = 'http://' + root_url + '/LogisticRegression_fit'
        payload = {'paras': {}}
        
        if arguments['--X'] is not None:
            try:
                payload['paras']['X']= json.loads(arguments['--X'])
            except:
                payload['paras']['X']= arguments['--X']
        
        if arguments['--y'] is not None:
            try:
                payload['paras']['y']= json.loads(arguments['--y'])
            except:
                payload['paras']['y']= arguments['--y']
        
        if arguments['--sample_weight'] is not None:
            try:
                payload['paras']['sample_weight']= json.loads(arguments['--sample_weight'])
            except:
                payload['paras']['sample_weight']= arguments['--sample_weight']
        
        r = requests.post(url, json=payload)
        return r.text
    
    if arguments.LogisticRegression and arguments.get_params and ( arguments['--deep'] or  True):
        url = 'http://' + root_url + '/LogisticRegression_get_params'
        payload = {'paras': {}}
        
        if arguments['--deep'] is not None:
            try:
                payload['paras']['deep']= json.loads(arguments['--deep'])
            except:
                payload['paras']['deep']= arguments['--deep']
        
        r = requests.post(url, json=payload)
        return r.text
    
    if arguments.LogisticRegression and arguments.predict and ( arguments['--X'] or  True):
        url = 'http://' + root_url + '/LogisticRegression_predict'
        payload = {'paras': {}}
        
        if arguments['--X'] is not None:
            try:
                payload['paras']['X']= json.loads(arguments['--X'])
            except:
                payload['paras']['X']= arguments['--X']
        
        r = requests.post(url, json=payload)
        return r.text
    
    if arguments.LogisticRegression and arguments.predict_log_proba and ( arguments['--X'] or  True):
        url = 'http://' + root_url + '/LogisticRegression_predict_log_proba'
        payload = {'paras': {}}
        
        if arguments['--X'] is not None:
            try:
                payload['paras']['X']= json.loads(arguments['--X'])
            except:
                payload['paras']['X']= arguments['--X']
        
        r = requests.post(url, json=payload)
        return r.text
    
    if arguments.LogisticRegression and arguments.predict_proba and ( arguments['--X'] or  True):
        url = 'http://' + root_url + '/LogisticRegression_predict_proba'
        payload = {'paras': {}}
        
        if arguments['--X'] is not None:
            try:
                payload['paras']['X']= json.loads(arguments['--X'])
            except:
                payload['paras']['X']= arguments['--X']
        
        r = requests.post(url, json=payload)
        return r.text
    
    if arguments.LogisticRegression and arguments.score and ( arguments['--X'] or  arguments['--y'] or  arguments['--sample_weight'] or  True):
        url = 'http://' + root_url + '/LogisticRegression_score'
        payload = {'paras': {}}
        
        if arguments['--X'] is not None:
            try:
                payload['paras']['X']= json.loads(arguments['--X'])
            except:
                payload['paras']['X']= arguments['--X']
        
        if arguments['--y'] is not None:
            try:
                payload['paras']['y']= json.loads(arguments['--y'])
            except:
                payload['paras']['y']= arguments['--y']
        
        if arguments['--sample_weight'] is not None:
            try:
                payload['paras']['sample_weight']= json.loads(arguments['--sample_weight'])
            except:
                payload['paras']['sample_weight']= arguments['--sample_weight']
        
        r = requests.post(url, json=payload)
        return r.text
    
    if arguments.LogisticRegression and arguments.sparsify and ( True):
        url = 'http://' + root_url + '/LogisticRegression_sparsify'
        payload = {'paras': {}}
        
        r = requests.post(url, json=payload)
        return r.text
    
    if arguments.LogisticRegression and arguments.get_properties and ( arguments['--name'] or  True):
        url = 'http://' + root_url + '/LogisticRegression_get_properties'
        payload = {'paras': {}}
        
        if arguments['--name'] is not None:
            try:
                payload['paras']['name']= json.loads(arguments['--name'])
            except:
                payload['paras']['name']= arguments['--name']
        
        r = requests.post(url, json=payload)
        return r.text
    
    if arguments.LogisticRegression and ( arguments['--penalty'] or  arguments['--dual'] or  arguments['--tol'] or  arguments['--C'] or  arguments['--fit_intercept'] or  arguments['--intercept_scaling'] or  arguments['--class_weight'] or  arguments['--random_state'] or  arguments['--solver'] or  arguments['--max_iter'] or  arguments['--multi_class'] or  arguments['--verbose'] or  arguments['--warm_start'] or  arguments['--n_jobs'] or  arguments['--l1_ratio'] or  True):
        url = 'http://'+ root_url + '/LogisticRegression_constructor'
        payload = {'paras': {}}
        
        if arguments['--penalty'] is not None:
            payload['paras']['penalty'] = json.loads(arguments['--penalty'])
        
        if arguments['--dual'] is not None:
            payload['paras']['dual'] = json.loads(arguments['--dual'])
        
        if arguments['--tol'] is not None:
            payload['paras']['tol'] = json.loads(arguments['--tol'])
        
        if arguments['--C'] is not None:
            payload['paras']['C'] = json.loads(arguments['--C'])
        
        if arguments['--fit_intercept'] is not None:
            payload['paras']['fit_intercept'] = json.loads(arguments['--fit_intercept'])
        
        if arguments['--intercept_scaling'] is not None:
            payload['paras']['intercept_scaling'] = json.loads(arguments['--intercept_scaling'])
        
        if arguments['--class_weight'] is not None:
            payload['paras']['class_weight'] = json.loads(arguments['--class_weight'])
        
        if arguments['--random_state'] is not None:
            payload['paras']['random_state'] = json.loads(arguments['--random_state'])
        
        if arguments['--solver'] is not None:
            payload['paras']['solver'] = json.loads(arguments['--solver'])
        
        if arguments['--max_iter'] is not None:
            payload['paras']['max_iter'] = json.loads(arguments['--max_iter'])
        
        if arguments['--multi_class'] is not None:
            payload['paras']['multi_class'] = json.loads(arguments['--multi_class'])
        
        if arguments['--verbose'] is not None:
            payload['paras']['verbose'] = json.loads(arguments['--verbose'])
        
        if arguments['--warm_start'] is not None:
            payload['paras']['warm_start'] = json.loads(arguments['--warm_start'])
        
        if arguments['--n_jobs'] is not None:
            payload['paras']['n_jobs'] = json.loads(arguments['--n_jobs'])
        
        if arguments['--l1_ratio'] is not None:
            payload['paras']['l1_ratio'] = json.loads(arguments['--l1_ratio'])
        
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