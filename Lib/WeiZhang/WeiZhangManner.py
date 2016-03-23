# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from Lib.WeiZhang.Head import HeaderType,HeaderFactory
from Lib.WeiZhang.WeiZhangWang import WeiZhangWang

class WeiZhangItem(object):
    typeA = 100
    typeB = 200
    typeC = 300

class WeiZhangManner(object):
    obj = ''

    def __init__(self,type):
        self.obj = self.return_obj(type)

    def return_obj(self,type):

        if type == WeiZhangItem.typeA:
            return WeiZhangWang()

        if type == WeiZhangItem.typeB:
            pass

        if type == WeiZhangItem.typeC:
            pass

    def run(self,params):
        return self.obj.run(params)

    def verify_code_get_result(self,post_verify_code_url,code,post_verify_code_cookie):
        return self.obj.verify_code_get_result(post_verify_code_url,code,post_verify_code_cookie)

