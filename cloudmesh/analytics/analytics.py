"""The analytic functions
The module include analytic functions, and are also the endpoints of the flask app. Those functions are referred by the
OpenAPI specification by operationIDs
"""

import os
from flask import jsonify, current_app
import numpy as np
from sklearn.linear_model import LinearRegression
from werkzeug.utils import secure_filename
from .file_helpers import *

def linear_regression(file_name, body):
    """Linear regression.

    Args:

        file_name (str): The file name that has the input data.
        body (dict): The request body, which is a dictionary mapped by the connexion.
    Return:
        Return an json objects.

    Warning:
        The input format should be specified
    """
    # Extract parameters from the request body

    paras = body['paras']

    try:
        data = read_csv(file_name)
        X = data[:,:-1]
        Y = data[:,-1]
        reg = LinearRegression(**paras).fit(X, Y)
        return jsonify({'coefficient':reg.coef_.tolist() })
    except Exception as e:
        return jsonify({'error': str(e)})

def pca():
    return jsonify({"output": 'run_pca_success'})

