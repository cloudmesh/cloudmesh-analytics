import os
from flask import jsonify, current_app
import numpy as np
from sklearn.linear_model import LinearRegression
from werkzeug.utils import secure_filename
from .file_helpers import *

def linear_regression(file_name, body):
    """
    Linear regression operation on two dimension data. The input format should be a list of pairs, e.g. [[1, 2], [3, 4]...]
    :param file_name: the data source
    :param body: the request body
    :return:
    """
    # Extract parameters from the request body
    paras = body['paras']
    #TODO: Data format is not correct
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

