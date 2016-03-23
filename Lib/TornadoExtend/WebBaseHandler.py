# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from Lib.TornadoExtend.BaseSyncHandler import BaseSyncHandler
from Lib.Tools.JsonExtend import JsonExtend
from tornado.web import _time_independent_equals
from tornado.escape import utf8

class WebBaseSyncHandler(BaseSyncHandler):

    def check_xsrf_cookie(self):
        token = self.get_xsrf()
        if not token:
            self.on_response_fail(self.http_response_code_fail, "'_xsrf' argument missing from POST")
            return
        _, token, _ = self._decode_xsrf_token(token)
        _, expected_token, _ = self._get_raw_xsrf_token()
        if not _time_independent_equals(utf8(token), utf8(expected_token)):
            self.on_response_fail(self.http_response_code_fail, "XSRF cookie does not match POST argument")
