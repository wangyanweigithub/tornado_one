# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import requests

class HttpCore(object):

    base_url = None
    debug = False
    timeout = 120

    def __init__(self,base_url=None,debug=False):
        self.base_url = base_url
        self.debug = debug

    def url_process(self,url):
        whole_url = None
        if self.base_url is None:
            whole_url = url
        elif url is None:
            whole_url = self.base_url

        else:
            whole_url = self.base_url + url

        if self.debug:
            print(whole_url)
        return whole_url

    def get(self,path,params,headers=None):
        ret = requests.get(self.url_process(path), params=params, timeout=self.timeout, headers=headers)
        return ret.text

    def post(self, path, params, headers=None, files=None):
        ret = requests.post(self.url_process(path), params=params, headers=headers, files=files, timeout=self.timeout)
        return ret.text

