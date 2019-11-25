"""File operations
The module include file operations
"""

import sys
import os
from flask import jsonify, current_app
import numpy as np
from werkzeug.utils import secure_filename
import pandas as pd

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