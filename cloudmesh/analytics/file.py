"""File operations
The module include file operations
"""

import sys
import os
from flask import jsonify, current_app
import numpy as np
from sklearn.linear_model import LinearRegression
from werkzeug.utils import secure_filename
import pandas as pd
from .file_helpers import *

def read(file_name):
    """Read files given a file name.

    Args:
        file_names: The input data source.
    Return:
        Return a json response.
    """
    try:
        data = read_csv(file_name)
    except:
        return jsonify({'error_message': 'failed to read'})
    return jsonify({file_name: data.tolist()})

def upload(file=None):
    """Upload files to the server
    Args:
        file: A file stream

    Return:
        Return the file name if it success

    Attention:
        Only support the csv format now.

    Raises:
        Raise an error message if the file format is not supported
    """
    ALLOWED_EXTENSIONS = {'csv'}
    if file and allowed(file.filename, ALLOWED_EXTENSIONS):
        save(file)
        return jsonify({'file_name': file.filename}), 200
    else:
        return jsonify({'error_message': 'Wrong file format'}), 400

def list():
    """List all uploaded files"""
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})
