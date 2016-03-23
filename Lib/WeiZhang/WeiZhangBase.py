# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import requests
import xmltodict
import re
from Model.CarType import CarType

class WeiZhangBase(object):

    def get_car_type_from_value(self,value):
        car_type = CarType.objects(value=value).first()
        return car_type

    def build_params(self,**kwargs):
        raise 'need override'

    def http_post(self,url,params,headers=None,cookies=None):

        ret = requests.post(url,data=params,headers=headers,cookies=cookies)
        ret.encoding = 'UTF-8'
        return ret

    def http_get(self,url,headers,cookies=None):

        ret = requests.get(url,headers=headers,cookies=cookies)
        ret.encoding = 'utf-8'
        return ret

    def parse_xml(self,params):

        ret = xmltodict.parse(params)
        return dict(ret)

    def run(self,params):
        raise 'need override'






