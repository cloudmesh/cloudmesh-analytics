# from sklearn.linear_model import LinearRegression
# import os
# import numpy as np


# def load_obj(path):
#     return np.load(path, allow_pickle=True).item()


# def save_obj(obj, class_name):
#     np.save(os.path.join('.', str(class_name) + '_constructor'),
#             obj, allow_pickle=True)
#     return


# def LinearRegression_constructor(body):
#     init = body['init']
#     res = LinearRegression(**init)
#     save_obj(res, 'LinearRegression')
#     return res



# def LinearRegression_fit(body):
#     obj =load_obj(os.path.join('.', 'LinearRegression_constructor.npy'))
#     res = obj.fit(**body['paras'])
#     save_obj(obj, 'LinearRegression')
#     return res

# def LinearRegression_get_params(body):
#     obj =load_obj(os.path.join('.', 'LinearRegression_constructor.npy'))
#     res = obj.get_params(**body['paras'])
#     save_obj(obj, 'LinearRegression')
#     return res

# def LinearRegression_predict(body):
#     obj =load_obj(os.path.join('.', 'LinearRegression_constructor.npy'))
#     res = obj.predict(**body['paras'])
#     save_obj(obj, 'LinearRegression')
#     return res

# def LinearRegression_score(body):
#     obj =load_obj(os.path.join('.', 'LinearRegression_constructor.npy'))
#     res = obj.score(**body['paras'])
#     save_obj(obj, 'LinearRegression')
#     return res