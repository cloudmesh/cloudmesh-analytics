import json
import requests

class Request(object):

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

