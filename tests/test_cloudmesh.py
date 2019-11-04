"""
Test the functions in :py:mod:`cloudmesh.analytics.analytics`

    Tip:
        Running the test under the cloudmesh-analytics directory

        ```> ./cloudmesh-analytics$ pytest```

"""

import sys
import os

from cloudmesh.analytics.server.server import create_app
from flask import jsonify
import json
from werkzeug.test import EnvironBuilder
from io import StringIO, BytesIO
import numpy as np
import pytest
import cloudmesh.analytics.analytics as analytics


@pytest.mark.first
class TestFileOperations:
    """Test file operations

    Attention:
        1. The function will be ran first and the files uploaded will be used for other tests

        2. The uploaded file is insulated and saved in the testing_files directory as indicated in
        :py:mod:`tests.conftest`
    """
    def post_file(self,client, path, name):
        """A helper function to make post request

        Args:
            client: The pytest fixture defined in :py:mod:`tests.conftest`
            path: The rest api defined in the yaml file
            name: the file name to post

        Return:
            The data attribute of the flask response object
        """
        f = open(path, 'rb')
        # Simulate post request to upload the file
        response = client.post(path='/cloudmesh-analytics/file/upload',
                               data={'file': (f, name)})
        f.close()
        return response.data

    def test_success_upload(self, client):
        """Test upload. The file will be uploaded in to the current directory named files

        The test sample will use a empty csv file called test upload

        Args:
            client: The pytest fixture defined in :py:mod:`tests.conftest`

        Return:
            The data attribute of the flask response object, which is a binary string that includes a list of uploaded
            file names
        """
        assert self.post_file(client, './tests/test_assets/test_upload.csv','test_upload.csv') \
               == \
               b'{"file_name":"test_upload.csv"}\n'

    def test_success_upload_sample(self, client):
        """Test upload. The file will be uploaded in to the current directory named files

        The test sample will use a empty csv file called test upload

        Args:
            client: The pytest fixture defined in :py:mod:`tests.conftest`

        Return:
            The data attribute of the flask response object, which is a binary string that includes a list of uploaded
            file names
        """
        assert self.post_file(client, './tests/test_assets/sample_matrix.csv','sample_matrix.csv') \
               == \
               b'{"file_name":"sample_matrix.csv"}\n'

    def test_read(self, client):
        """Test read uploaded file using the rest api"""
        response = client.get(path='/cloudmesh-analytics/file/read/sample_matrix')
        assert b'{"sample_matrix":[[1,2],[3,4],[5,6],[7,8],[9,10]]}\n' == response.data


    def test_success_upload_dabetes(self, client):
        """
        Test upload. The file will be uploaded in to the current directory named files
        The test sample will use a empty csv file called test upload

        Args:
            client: The pytest fixture defined in :py:mod:`tests.conftest`

        Return:
            The data attribute of the flask response object, which is a binary string that includes a list of uploaded
            file names
        """
        assert self.post_file(client, './tests/test_assets/diabetes.csv','diabetes.csv') \
               == \
               b'{"file_name":"diabetes.csv"}\n'

    def test_format_error(self, client):
        """The upload will failed due to the txt file format. An error message will return

        Args:
            client: The pytest fixture defined in :py:mod:`tests.conftest`

        Return:
            The data attribute of the flask response object, which is a binary string that includes a list of uploaded
            file names
        """
        assert self.post_file(client, './tests/test_assets/test_upload.csv', 'test_upload.txt') \
               == \
               b'{"error_message":"Wrong file format"}\n'


class TestLinearRegression:

    def test_errors(self, client):
        """Testing error arguments. The exception raised by the sci-kit learn will be returned in the error message

        Args:
            client: The pytest fixture defined in :py:mod:`tests.conftest`

        Return:
            The data attribute of the flask response object, which is a binary string that includes a list of uploaded
            file names

        Note:
            The server will return the error message raised by the sci-kit learn

        """
        response = client.post(path='/cloudmesh-analytics/analytics/linear-regression/test_upload',
                               data=json.dumps({
                                   'file_name': 'test_upload',
                                   'paras':
                                       {
                                           'fit_intercept': True,
                                           'error_para': False,
                                           'n_jobs': 1
                                       }
                               }),
                               content_type='application/json')
        assert b'{"error":"__init__() got an unexpected keyword argument \'error_para\'"}\n' \
               == \
               response.data

    def test_linear_regression(self, client):
        """Testing error arguments. The exception raised by the sci-kit learn will be returned

        The data is taken from the sci-kit learn built in samples.

        Args:
            client: The pytest fixture defined in :py:mod:`tests.conftest`

        Return:
            The data attribute of the flask response object, which is a binary string that includes a list of uploaded
            file names

        Warning:
            Todo: The assertion may be false due to the floating number representaion in different word-size systems

        """
        response = client.post(path='/cloudmesh-analytics/analytics/linear-regression/diabetes',
                               data=json.dumps({
                                   'paras':
                                       {
                                           'fit_intercept': True
                                       }
                               }),
                               content_type='application/json')
        assert b'{"coefficient":[-10.01219781747075,-239.81908936565543,519.8397867901347,324.390427689377' \
               b',-792.1841616283085,476.7458378236647,101.04457032134525,177.06417623225093,751.2793210873953' \
               b',67.62538639104389]}\n' == response.data

def test_run_pca(client):
    response = client.get('/cloudmesh-ai-services/analytics/pca')

    assert response.data == ''

