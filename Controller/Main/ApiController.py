# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import re
import json
from datetime import datetime
from tornado.web import _time_independent_equals,utf8
from Controller.Main.ProcessFactory import ProcessFactory
from Lib.TornadoExtend import AccessSource
from Lib.TornadoExtend.BaseSyncHandler import BaseSyncHandler
from Lib.Tools.Codec import base64_decode,md5
class ApiController(BaseSyncHandler):

    app_key = '8255c0f2e8e6733bc4a2f11fb6a1b7e9'

    def real_arguments_decode(self, method, arguments):
        if len(arguments.keys()) == 0:
            return arguments

        sign_source = arguments.get('sign', None)
        sign = md5(arguments.get('params', None)+arguments.get('time', None) + self.app_key)

        if sign != sign_source:
            return self.on_response_fail(self.http_response_code_fail, 'sign 不匹配')

        params = arguments.get('params', None)
        # new_str = base64_decode(params)
        ff1 = params[:10]
        ff2 = params[10:-10]
        ff3 = params[-10:]
        str_b64 = base64_decode(ff3 + ff2 + ff1)
        new_params = arguments
        new_params['params'] = json.loads(str_b64)
        # print(new_params)
        return new_params

    def response_params_save_from_request(self, arguments):
        self.add_response_param('lang', arguments.get('lang', 'zh_CN'))
        self.add_response_param('time', arguments.get('time', str(datetime.now().strftime('%Y%m%d%H%M%S%f'))))
        self.add_response_param('source', int(arguments.get('source', AccessSource.mobile)))
        self.add_response_param('sign', arguments.get('sign', ''))

    def on_request(self, method, path, arguments):
        params = arguments.get('params', None)

        if params is not None:
            self.on_request_ready(method, path, arguments)
        else:
            self.on_response_fail(self.http_response_code_fail, 'params丢失')

    def is_request_from_web(self):
        path = self.request_path()
        ret = path.find('web')
        if ret == -1:
            return False
        else:
            return True

    def check_xsrf_cookie(self):
        if self.is_request_from_web() is False:
            return

        token = self.get_xsrf()
        if not token:
            self.on_response_fail(self.http_response_code_fail, "'_xsrf' argument missing from POST")
            return
        _, token, _ = self._decode_xsrf_token(token)
        _, expected_token, _ = self._get_raw_xsrf_token()
        if not _time_independent_equals(utf8(token), utf8(expected_token)):
            self.on_response_fail(self.http_response_code_fail, "XSRF cookie does not match POST argument")

    def on_request_ready(self, method, path, arguments):

        # if method == 'GET':
        #     self.on_response_fail(self.http_response_code_fail, '不支持的操作')
        #     return

        ret = re.search('((?<=api/)[0-9a-zA-Z_/]+)', path)
        if ret is None:
            self.on_response_fail(self.http_response_code_fail, '不支持的路径')
            return

        action = ret.group(0)
        # action = re.sub("^web/", "", action)
        # params = arguments
        if arguments is None:
            self.on_response_fail(self.http_response_code_fail, 'params不存在')
            return
        self.process_with_action(method, action, arguments)

    def process_with_action(self, method, action, args):
        # try:
            self.do_action(method, action, args)
        # except Exception as e:
        #     print(e)
        #     self.on_response_fail(self.http_response_code_fail, '不支持的API')

    def do_action(self, method, action, args):
        print('接收到的参数是:',args)
        ProcessClass = ProcessFactory().return_class(action)
        p = ProcessClass(self.application, self, method, self.response_params, self.remote_ip(), self.agent_from(), args, self.request.host, self.get_files())
        ret = p.process()
        if method == 'GET':
            return self.render(ret['html'],params=ret['params'])
        self.on_response(self.build_response(**ret))
