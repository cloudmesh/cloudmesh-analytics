from sklearn.linear_model import LinearRegression
import os
import numpy as np
import file
from flask import jsonify

def load_obj(path):
    return np.load(path, allow_pickle=True).item()


def save_obj(obj, class_name):
    np.save(os.path.join('.', str(class_name) + '_constructor'),
            obj, allow_pickle=True)
    return


def LinearRegression_constructor(body):
    try:
        paras = body['paras']
        res = LinearRegression(**paras)
        save_obj(res, 'LinearRegression')
    except Exception as e:
        return jsonify({'Error': str(e)})
    return jsonify({'return': 'successfully constructed'})



def LinearRegression_fit(body):
    if 'X' in body['paras'].keys() and isinstance(body['paras']['X'], str):
        file_name = body['paras']['X']
        body['paras']['X'] = file.read_csv(file_name)

    if 'y' in body['paras'].keys() and isinstance(body['paras']['y'], str):
        file_name = body['paras']['y']
        body['paras']['y'] = file.read_csv(file_name)

    try:
        obj =load_obj(os.path.join('.', 'LinearRegression_constructor.npy'))
        res = obj.fit(**body['paras'])
        save_obj(obj, 'LinearRegression')
    except Exception as e:
        return jsonify({'Error': str(e)})

    return jsonify({'return': str(res)})

def LinearRegression_get_params(body):
    if 'X' in body['paras'].keys() and isinstance(body['paras']['X'], str):
        file_name = body['paras']['X']
        body['paras']['X'] = file.read_csv(file_name)

    if 'y' in body['paras'].keys() and isinstance(body['paras']['y'], str):
        file_name = body['paras']['y']
        body['paras']['y'] = file.read_csv(file_name)

    try:
        obj =load_obj(os.path.join('.', 'LinearRegression_constructor.npy'))
        res = obj.get_params(**body['paras'])
        save_obj(obj, 'LinearRegression')
    except Exception as e:
        return jsonify({'Error': str(e)})

    return jsonify({'return': str(res)})

def LinearRegression_predict(body):
    if 'X' in body['paras'].keys() and isinstance(body['paras']['X'], str):
        file_name = body['paras']['X']
        body['paras']['X'] = file.read_csv(file_name)

    if 'y' in body['paras'].keys() and isinstance(body['paras']['y'], str):
        file_name = body['paras']['y']
        body['paras']['y'] = file.read_csv(file_name)

    try:
        obj =load_obj(os.path.join('.', 'LinearRegression_constructor.npy'))
        res = obj.predict(**body['paras'])
        save_obj(obj, 'LinearRegression')
    except Exception as e:
        return jsonify({'Error': str(e)})

    return jsonify({'return': str(res)})

def LinearRegression_score(body):
    if 'X' in body['paras'].keys() and isinstance(body['paras']['X'], str):
        file_name = body['paras']['X']
        body['paras']['X'] = file.read_csv(file_name)

    if 'y' in body['paras'].keys() and isinstance(body['paras']['y'], str):
        file_name = body['paras']['y']
        body['paras']['y'] = file.read_csv(file_name)

    try:
        obj =load_obj(os.path.join('.', 'LinearRegression_constructor.npy'))
        res = obj.score(**body['paras'])
        save_obj(obj, 'LinearRegression')
    except Exception as e:
        return jsonify({'Error': str(e)})

    return jsonify({'return': str(res)})