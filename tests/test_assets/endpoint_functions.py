from sklearn.linear_model import LinearRegression
import os
import numpy as np


def load_obj(path):
    return np.load(path, allow_pickle=True).item()


def save_obj(obj, class_name):
    np.save(os.path.join('./cm/cloudmesh-analytics/tests/test_assets/', str(class_name) + '_constructor'),
            obj, allow_pickle=True)
    return


def LinearRegression_constructor(body):
    init = body['init']
    res = LinearRegression(**init)
    save_obj(res, 'LinearRegression')
    return res



def LinearRegression_fit(body):
    obj =load_obj(os.path.join('./cm/cloudmesh-analytics/tests/test_assets/', 'LinearRegression_constructor.npy'))
    
    res = obj.fit(**body['paras'])
    
    save_obj(obj, 'LinearRegression')
    return res

def LinearRegression_get_params(body):
    obj =load_obj(os.path.join('./cm/cloudmesh-analytics/tests/test_assets/', 'LinearRegression_constructor.npy'))
    
    res = obj.get_params(**body['paras'])
    
    save_obj(obj, 'LinearRegression')
    return res

def LinearRegression_predict(body):
    obj =load_obj(os.path.join('./cm/cloudmesh-analytics/tests/test_assets/', 'LinearRegression_constructor.npy'))
    
    res = obj.predict(**body['paras'])
    
    save_obj(obj, 'LinearRegression')
    return res

def LinearRegression_score(body):
    obj =load_obj(os.path.join('./cm/cloudmesh-analytics/tests/test_assets/', 'LinearRegression_constructor.npy'))
    
    res = obj.score(**body['paras'])
    
    save_obj(obj, 'LinearRegression')
    return res

def LinearRegression___properties__(body):
    obj =load_obj(os.path.join('./cm/cloudmesh-analytics/tests/test_assets/', 'LinearRegression_constructor.npy'))
    
    res = getattr(obj,body['attr'])
    
    save_obj(obj, 'LinearRegression')
    return res


X = [[1, 1], [1, 2], [2, 2], [2, 3]]
y = list(np.dot(X, np.array([1, 2])))

body = {
    'init': {},
    'paras': {
        'X': X,
        'y': y
    }
}

p_body = {
    'paras': {'X': [[3, 5]]}
}


a_body = {
    'attr':'coef_'
}

print(LinearRegression_constructor(body))
print(LinearRegression_fit(body))
print(LinearRegression_predict(p_body))
print(LinearRegression_score(body))
print(LinearRegression___properties__(a_body))