# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from datetime import datetime
from Controller.Main.BaseProcess import BaseProcess
from Lib.TornadoExtend import HttpResponseCode
from Model.AuthCode import AuthCode,AuthCodeType
from Lib.Tools.JsonExtend import JsonExtend
from Model.Member import Member
from Model.AuthCode import AuthCode,AuthCodeType

class MemberProcess(BaseProcess):
    #注册用户
    def create_member(self):
        params = self.get_params()
        mobile_phone = params.get('mobile_phone', None)
        password_md5 = params.get('password_md5', None)
        device_token = params.get('device_token', None)
        auth_code = params.get('auth_code',None)
        source_from_description = params.get('source_from_description', None)

        if mobile_phone is None or password_md5 is None:
            self.on_response_fail(HttpResponseCode.fail,'缺少必要参数')

        verify_code = AuthCode.verify_code(mobile_phone,AuthCodeType.register,auth_code)
        if not verify_code:
            return self.on_response_fail(HttpResponseCode.fail, '验证码错误或已过期,请重新获取')
        AuthCode.used_code(mobile_phone,AuthCodeType.register,auth_code)


        member = self.get_member_with_mobile_phone(mobile_phone)
        if member:
            if member.disabled:
                return self.on_response_fail(HttpResponseCode.fail, '账户已被禁用, 无法注册, 请联系管理员')
            else:
                return self.on_response_fail(HttpResponseCode.fail, '账户已存在, 请更换一个手机号码.')
        else:
            member = Member()
            member.mobile_phone = mobile_phone
            member.password_md5 = password_md5
            member.create_time = datetime.now()
            member.last_login_time = member.create_time
            member.save()

        access = self.generate_access(member, device_token, source_from_description, update=False)
        userinfo = dict(
            member=JsonExtend.to_json(member.to_mongo()),
            access=JsonExtend.to_json(access.to_mongo())
        )
        return self.on_response_success(userinfo)

    #登录
    def login(self):
        params = self.get_params()
        mobile_phone = params.get('mobile_phone', None)
        authcode = params.get('authcode', None)
        password_md5 = params.get('password_md5', None)
        device_token = params.get('device_token', None)
        source_from_description = params.get('source_from_description', None)

        if mobile_phone is None:
            return self.on_response_fail(HttpResponseCode.fail, '缺少必要参数')

        member = self.get_member_with_mobile_phone(mobile_phone)
        if member:
            if authcode is not None:
                if AuthCode.verify_code(mobile_phone, AuthCodeType.login, authcode) is False:
                    return self.on_response_fail(HttpResponseCode.fail, '验证码不正确或已过期, 请检查')
                AuthCode.used_code(mobile_phone, AuthCodeType.login, authcode)
            elif password_md5 is not None:
                if password_md5 != member.password_md5:
                    return self.on_response_fail(HttpResponseCode.fail,'密码错误')
            else:
                return self.on_response_fail(HttpResponseCode.fail,'缺少必要参数')

            access = self.generate_access(member, device_token, source_from_description, update=True)
            userinfo = dict(access_token=access.access_token,money=member.money,mobile_phone=member.mobile_phone)
            return self.on_response_success(userinfo)
        else:
            member = Member()
            member.mobile_phone = mobile_phone
            access = self.generate_access(member, device_token, source_from_description, update=False)
            userinfo = dict(access_token=access.access_token,money=member.money,mobile_phone=member.mobile_phone)
            return self.on_response_success(userinfo)

    #更改用户password、pay_password、mobile_phone信息
    def change_userinfo(self):
        params = self.get_params()
        access_token = params.get('access_token', None)
        password_md5 = params.get('password_md5', None)
        key = params.get('key', None)
        value = params.get('value', None)

        support_key = ['password_md5','pay_password_md5','mobile_phone']

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token不正确或已过期, 请检查')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'没有这个用户, 请检查')
        if password_md5 != member.password_md5:
            return self.on_response_fail(HttpResponseCode.fail,'密码不正确, 请检查')

        if key in support_key:
            try:
                setattr(member,key,value)
                member.save()
            except Exception as e:
                print('更改用户信息出错',e)
        else:
            return self.on_response_fail(HttpResponseCode.fail,'不能修改账户的'+key+'信息')

    #用户中心
    def personal_center(self):
        params = self.get_params()
        access_token = params.get('access_token', None)
        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token不正确或已过期, 请检查')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'用户不正确, 请检查')

        mobile = member.mobile_phone[:3] + '*'*4 + member.mobile_phone[-4:]
        ret = dict(mobile_phone=mobile,money=member.money)
        return self.on_response_success(ret)

    #忘记密码
    def forget_password(self):
        params = self.get_params()
        code_type = params.get('code_type', None)
        mobile_phone = params.get('mobile_phone', None)
        auth_code = params.get('auth_code', None)
        password_md5 = params.get('password_md5',None)

        if code_type is None or mobile_phone is None or auth_code is None or password_md5 is None:
            return self.on_response_fail(HttpResponseCode.fail,'缺少必要参数')

        if AuthCode.verify_code(mobile_phone, code_type, auth_code) is False:
            return self.on_response_fail(HttpResponseCode.fail, '验证码不正确或已经失效, 请重新输入')
        AuthCode.used_code(mobile_phone, code_type, auth_code)

        member = self.get_member_with_mobile_phone(mobile_phone)
        member.password_md5 = password_md5
        member.save()
        return self.on_response_success()



