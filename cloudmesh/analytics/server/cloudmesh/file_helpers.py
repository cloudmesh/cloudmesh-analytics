"""
This module includes the helper functions for the help.py in order to characterize the endpoint functions
"""
import os
from flask import current_app
import numpy as np
from sklearn.linear_model import LinearRegression
from werkzeug.utils import secure_filename
import pandas as pd

def read_csv(file_name):
    """
    Read csv using panda. The source path is relative and set when initializing flask app.
    :param file_name:
    :return:
    """
    data = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name + '.csv', ), header=None)
    return data.values

def allowed(file_name, allowed_extentions):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in allowed_extentions
