import json
import requests

def run_command(arguments, root_url):
    if arguments.LinearRegression and ( arguments.fit_intercept or  arguments.normalize or  arguments.copy_X or  arguments.n_jobs or  True):
        url = root_url + '/LinearRegression'
        payload = {'paras': {}}
        
        if arguments.fit_intercept is not None:
            payload['fit_intercept']= arguments.fit_intercept
        
        if arguments.normalize is not None:
            payload['normalize']= arguments.normalize
        
        if arguments.copy_X is not None:
            payload['copy_X']= arguments.copy_X
        
        if arguments.n_jobs is not None:
            payload['n_jobs']= arguments.n_jobs
        
        r = requests.post(root_url, data=json.dumps(payload))
        return r.text
    
    
    if arguments.LinearRegression and ( arguments.X or  arguments.y or  arguments.sample_weight or True):
        url = root_url + '/LinearRegression' + '/fit'
        payload = {'paras': {}}
        
        if arguments.fit is not None:
            payload['fit']= arguments.fit
        
        if arguments.fit is not None:
            payload['fit']= arguments.fit
        
        if arguments.fit is not None:
            payload['fit']= arguments.fit
        
        r = requests.post(url, data=json.dumps(payload))
        return r.text
    
    if arguments.LinearRegression and ( arguments.deep or True):
        url = root_url + '/LinearRegression' + '/get_params'
        payload = {'paras': {}}
        
        if arguments.get_params is not None:
            payload['get_params']= arguments.get_params
        
        r = requests.post(url, data=json.dumps(payload))
        return r.text
    
    if arguments.LinearRegression and ( arguments.X or True):
        url = root_url + '/LinearRegression' + '/predict'
        payload = {'paras': {}}
        
        if arguments.predict is not None:
            payload['predict']= arguments.predict
        
        r = requests.post(url, data=json.dumps(payload))
        return r.text
    
    if arguments.LinearRegression and ( arguments.X or  arguments.y or  arguments.sample_weight or True):
        url = root_url + '/LinearRegression' + '/score'
        payload = {'paras': {}}
        
        if arguments.score is not None:
            payload['score']= arguments.score
        
        if arguments.score is not None:
            payload['score']= arguments.score
        
        if arguments.score is not None:
            payload['score']= arguments.score
        
        r = requests.post(url, data=json.dumps(payload))
        return r.text
    
    if arguments.LinearRegression and ( arguments.property or True):
        url = root_url + '/LinearRegression' + '/get_property'
        payload = {'paras': {}}
        
        if arguments.get_property is not None:
            payload['get_property']= arguments.get_property
        
        r = requests.post(url, data=json.dumps(payload))
        return r.text
    

     