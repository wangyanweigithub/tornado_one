# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import random
import datetime
from mongoengine import *
import setting

connect(setting.database_name)

class AuthCodeType(object):

        #登录
        login = 100
        #充值
        transaction = 200
        #提现验证码
        withdraw = 300
        #注册
        register = 400
        #忘记密码
        forget_password = 500

class AuthCode(Document):

    #手机号码
    mobile_phone = IntField(required=True)
    #验证码类型
    code_type = IntField(required=True)
    #验证码
    value = StringField(required=True)
    #是否已使用，0未使用，1已使用
    status = IntField(required=True)
    #创建时间
    create_time = DateTimeField(required=True)
    #有效期，单位分钟
    invalid_minute = IntField(required=True,default=30)

    @staticmethod
    def generate_code(mobile_phone,code_type,invalid_minute=30):
        code = str(random.randint(100000,999999))
        has = AuthCode.objects(value=code,status=0).first()
        if has:
            return AuthCode.generate_code(mobile_phone,code_type)
        ac = AuthCode()
        ac.mobile_phone = mobile_phone
        ac.code_type = code_type
        ac.value = code
        ac.status = 0
        ac.create_time = datetime.datetime.now()
        ac.invalid_minute = invalid_minute
        ac.save()
        return ac

    @staticmethod
    def verify_code(mobile_phone,code_type,code):
        has = AuthCode.objects(mobile_phone=mobile_phone, value=code, code_type=code_type, status=0).first()
        if has:
            now = datetime.datetime.now()
            effective_period = has.invalid_minute * 60
            if now < has.create_time + datetime.timedelta(seconds=effective_period):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def used_code(mobile_phone, code_type, code):
        ac = AuthCode.objects(mobile_phone=mobile_phone, code_type=code_type, value=code, status=0).first()
        ac.status = 1
        ac.save()
