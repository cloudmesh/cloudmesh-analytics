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
    """
    Read files given a file name.

    :param file_name: The input data source.
    :return: a json response.
    """
    try:
        data = read_csv(file_name)
    except:
        return jsonify({'error_message': 'failed to read'})
    return jsonify({file_name: data.tolist()})

def upload(file=None):
    """
    Upload cvs files to the server

    Raise an error message if the file format is not supported


    :param file: A file stream

    :return: the file name if it success
    """
    ALLOWED_EXTENSIONS = {'csv'}
    if file and allowed(file.filename, ALLOWED_EXTENSIONS):
        save(file)
        return jsonify({'file_name': file.filename}), 200
    else:
        return jsonify({'error_message': 'Wrong file format'}), 400

def list():
    """
    List all uploaded files
    """
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})


def read_csv(file_name):
    """

    Read csv using panda. The source path is relative and set when initializing
    flask app.

    :param file_name: The file name to read
    :return: A numpy array
    """
    data = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                    f"{file_name}.csv", ),
                       header=None)
    return data.values

def allowed(file_name, allowed_extentions):
    """
    The allowed file extensions

    :param file_name: The file name to check
    :param allowed_extentions: The allowed file extensions
    :return: Return true or false
    """
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in allowed_extentions

def save(file):
    """
    Save file after securing the file name

    :param file: the input data source
    :return: a json response
    """
    filename = secure_filename(file.filename)
    try:
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    except Exception as e:
        return jsonify({'error_message': str(e)})