import inspect
import sys
import pprint
import sklearn.linear_model
import numpy as np
import json

from numpydoc import docscrape
from sklearn.linear_model import LinearRegression


def get_public_members(obj):
    """

    Attention:
        The type of members
            1. public
                1. properties -- How to deal with properties? #TODO
                2. functions -- only functions should be exposed
            2. private
    :param obj:
    :return:
    """
    def isprivate(name):
        if name[0] == '_':
            return True
        else:
            return False

    public_members = {}
    for k, v in inspect.getmembers(obj):
        if not isprivate(k):
            public_members[k] = v
    return  public_members

def get_parameters(doc):
    r = docscrape.NumpyDocString(doc)
    paras = {}
    for p in r['Parameters']:
        paras[p.name]=str(p.type).split(' ')[0].split(',')[0]
    return paras

def get_signatures(class_names):
    """

        Warnings:
            1. Orderdict: The order is not important if you specified the parameters names
            2. filtering the fucntions that are not public
    """
    res = {}
    for i, class_name in enumerate(class_names):
        try:
            res[i] = {class_name: {}}
            doc = inspect.getdoc(getattr(sklearn.linear_model, class_name))
            res[i][class_name]['constructor'] = get_parameters(doc)
            for member_name, f in get_public_members(getattr(sklearn.linear_model, class_name)).items():
                res[i][class_name][member_name] = {}
                if inspect.isfunction(f):
                    doc = inspect.getdoc(f)
                    res[i][class_name][member_name] = get_parameters(doc)
                else:
                    res[i][class_name][member_name] = f
        except ValueError:
            pass
    return res