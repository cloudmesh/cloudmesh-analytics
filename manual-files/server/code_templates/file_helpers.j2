"""
The helper function isolates non-endpoint function from the file module
"""
import os
from flask import current_app
import numpy as np
from sklearn.linear_model import LinearRegression
from werkzeug.utils import secure_filename
import pandas as pd

def read_csv(file_name):
    """Read csv using panda. The source path is relative and set when initializing flask app.

    Args:
        file_name: The file name to read

    Return:
        A numpy array
    """
    data = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name + '.csv', ), header=None)
    return data.values

def allowed(file_name, allowed_extentions):
    """The allowed file extensions

    Args:
        file_name: The file name to check
        allowed_extensions: The allowed file extensions

    Return:
        Return true or false
    """
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in allowed_extentions

def save(file):
    """ Save file after securing the file name

    Args:
        file: the input data source

    Return:
        Return a json response
    """
    filename = secure_filename(file.filename)
    try:
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    except Exception as e:
        return jsonify({'error_message': str(e)})