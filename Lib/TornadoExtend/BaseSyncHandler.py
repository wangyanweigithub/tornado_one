# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import tornado.web
from Lib.TornadoExtend import HttpResponseCode
from Lib.Tools.JsonExtend import JsonExtend

class BaseSyncHandler(tornado.web.RequestHandler):

    response_params = {}
    jsoncallback = None
    http_response_code_success = 200
    http_response_code_fail = 400
    http_response_code_access_token_expired = 401


    def process_argument(self,args):
        if isinstance(args,list):
            if len(args) == 1:
                return self.process_argument(args[0])
            ret = []
            for arg in args:
                ret.append(self.process_argument(arg))
        else:
            return args.decode()

    def base_get_arguments(self):
        result = {}
        for key,value in self.request.arguments.items():
            result[key] = self.process_argument(value)
        return result


    def get(self, *args, **kwargs):
        self.before_on_request("GET",self.request.path,self.base_get_arguments())

    def post(self, *args, **kwargs):
        self.before_on_request("POST",self.request.path,self.base_get_arguments())

    def before_on_request(self,method,path,argument):
        self.response_params = {}
        self.jsoncallback = argument.get('jsoncallback',None)
        real_arguments = self.real_arguments_decode(method,argument)
        self.response_params_save_from_request(real_arguments)
        self.on_request(method,path,real_arguments)

    def real_arguments_decode(self,method,arguments):
        return arguments

    def response_params_save_from_request(self,arguments):
        pass

    def add_response_param(self,key,value):
        self.response_params[key] = value

    def on_request(self,method,path,arguments):
        raise 'need override'

    def build_response(self,**ret):
        result = {}
        result.update(self.response_params)
        result.update(ret)
        return result

    def on_response(self,content):
        if self.jsoncallback:
            self.write(self.jsoncallback + "(" + content + ")")
            self.finsh()
        else:
            self.set_header("Content-Type","application/json; charset=utf-8")
            print('返回结果是:',JsonExtend.to_json(content))
            self.write(JsonExtend.to_json(content))
            self.finish()

    def remote_ip(self):
        return self.request.remote_ip

    def request_path(self):
        return self.request.path

    def agent_from(self):
        agent = self.request.headers['User-Agent']
        return agent

    def on_response_no_finsh(self,content):
        if self.jsoncallback:
            self.write(self.jsoncallback + "(" + content + ")")
        else:
            self.set_header("Content-Type","application/json; charset=utf-8")
            self.write(JsonExtend.to_json(content))

    def on_response_customize(self, **data):
        self.on_response(self.build_response(**data))

    def  on_response_success(self,value=None):
        content = dict(code=HttpResponseCode.success,value=value)
        self.on_response(self.build_response(**content))

    def on_response_fail(self,code,message):
        content = dict(code=code,message=message)
        self.on_response(self.build_response(**content))

    def get_xsrf(self):
        token = (self.get_argument("_xsrf", None) or
                 self.request.headers.get("X-Xsrftoken") or
                 self.request.headers.get("X-Csrftoken"))
        return token

    def get_files(self):
        files = self.request.files
        return files


