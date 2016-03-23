# -*- coding: utf-8 -*-
__anthor__ = 'wangyanwei'

import json
from datetime import datetime
from bson import ObjectId

class JsonExtend(object):

    @classmethod
    def process_pop_keys(cls,data,pop_keys=[]):

        if isinstance(data,dict):
            for k in pop_keys:
                data.pop(k,None)
            for k,v in data.items():
                data[k] = cls.process_pop_keys(v,pop_keys)
            return data
        elif isinstance(data,list) or isinstance(data,tuple):
            ret = [cls.process_pop_keys(x,pop_keys) for x in data]
            if isinstance(data,tuple):
                ret = tuple(ret)
            return ret
        else:
            return data

    @classmethod
    def to_json_string(cls,data):
        date_format='%Y-%m-%d %H:%M:%S'
        data = cls.process_pop_keys(data)
        def porcess_son_to_json(obj,date_format=date_format):
            if isinstance(obj,datetime):
                return obj.strftime(date_format)
            if isinstance(obj,ObjectId):
                return str(obj)
            else:
                raise (obj + 'is not Json serializable')
        return json.dumps(data,default=porcess_son_to_json,ensure_ascii=False)

    @classmethod
    def to_json(cls,data):
        return cls.to_json_string(data)

    @classmethod
    def mongoengine_query_to_list(cls,data):
        ret = []
        for item in data:
            ret.append(item.to_mongo())
        return ret