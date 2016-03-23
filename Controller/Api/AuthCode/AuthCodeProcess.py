# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from Model.AuthCode import AuthCode
from Lib.Sms.SmsManager import SmsManager
from Lib.TornadoExtend import HttpResponseCode
from Controller.Main.BaseProcess import BaseProcess

class AuthCodeProcess(BaseProcess):

    def get_authcode(self):
        params = self.get_params()
        code_type = params.get('authcode_type', None)
        mobile_phone = params.get('mobile_phone', None)

        if mobile_phone is None or type is None:
            return self.on_response_fail(HttpResponseCode.fail, '缺少必要参数')

        ac = AuthCode.generate_code(mobile_phone, code_type)
        content = '您本次的验证码是' + '(' + ac.value + ')' + ', 有效期为30分钟'
        SmsManager().send(phone_list=[ac.mobile_phone], content=content, signature='【商富金融】')
        return self.on_response_success(dict(auth_code=ac.value))

    def chek_authcode(self):
        params = self.get_params()
        code_type = params.get('code_type', None)
        mobile_phone = params.get('mobile_phone', None)
        auth_code = params.get('auth_code', None)

        if AuthCode.verify_code(mobile_phone, code_type, auth_code) is False:
            return self.on_response_fail(HttpResponseCode.fail, '验证码不正确或已经失效, 请重新输入')
        AuthCode.used_code(mobile_phone, code_type, auth_code)
        return self.on_response_success()


