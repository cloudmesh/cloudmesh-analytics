import sys
import os
from flask import jsonify, current_app
import numpy as np
from sklearn.linear_model import LinearRegression
from werkzeug.utils import secure_filename
import pandas as pd
from .file_helpers import *

def read(file_name):
    """
    Read files given a file name
    :param file_name:
    :return: return a json file
    """
    try:
        data = read_csv(file_name)
    except:
        return jsonify({'error_message': 'failed to read'})
    return jsonify({file_name: data.tolist()})

def save(file):
    """
    Save file after securing the file name
    :param file:
    :return:
    """
    filename = secure_filename(file.filename)
    try:
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    except Exception as e:
        return jsonify({'error_message': str(e)})




def upload(file=None):
    ALLOWED_EXTENSIONS = {'csv'}
    if file and allowed(file.filename, ALLOWED_EXTENSIONS):
        save(file)
        return jsonify({'file_name': file.filename}), 200
    else:
        return jsonify({'error_message': 'Wrong file format'}), 400

def list():
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})
