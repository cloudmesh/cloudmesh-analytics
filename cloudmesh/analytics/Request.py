import json
import requests
import webbrowser

class Request(object):

    @staticmethod
    def _post(url, payload, verbose=False):
        if verbose:
            print("Contacting:", url)
            print("payload:", payload)
        r = requests.post(url, json=payload)
        return r

    @staticmethod
    def ui(service, root_url):
        url = f"{root_url}/{service}"
        print (url)
        open(url, new=0, autoraise=True)

    @staticmethod
    def get_parameters(parameters):
        data = {}
        for parameter in parameters:
            attribute, value = parameter.split("=")
            try:
                data[attribute] = json.loads(value)
            except:
                data[attribute] = value
        return data

    @staticmethod
    def run(service, name, parameters, root_url, verbose=False):
        data = Request.get_parameters(parameters)
        url = f'http://{root_url}/cloudmesh/{service}/{name}'
        payload = {
            'paras': data
        }
        r = Request._post(url, payload=payload, verbose=verbose)
        return r.text

    @staticmethod
    def constructor(service, root_url, verbose=False):
        url = f'http://{root_url}/cloudmesh/{service}/constructor'
        payload = {
            'paras': dict({})
        }
        r = Request._post(url, payload=payload, verbose=verbose)
        return r.text


    @staticmethod
    def simple_run(service, parameters, root_url, verbose=False):
        data = Request.get_parameters(parameters)
        url = f'http://{root_url}/{service}/constructor'
        print('url:', url)
        print ('data:', data)
        payload = {
            'paras': data
        }
        r = Request._post(url, payload=payload, verbose=verbose)
        return r.text

    @staticmethod
    def file_put(root_url, service, filename, verbose=False):

        url = f'http://{root_url}/cloudmesh/{service}/file/put'
        print ("URL", url)
        files = {'file': open(filename, 'rb')}
        r = requests.post(url, files=files)
        return r.text

    @staticmethod
    def file_list(root_url):
        r = requests.get(f'http://{root_url}/file/list')
        return r.text

    @staticmethod
    def file_get(root_url, service, filename):

        url = f'http://{root_url}/cloudmesh/{service}/file/get/{filename}'

        print ("URL", url)

        r = requests.get(url)
        return r.text

