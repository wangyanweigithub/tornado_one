# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from mongoengine import *
from setting import database_name
from datetime import datetime

connect(database_name)

class Member(Document):

    #手机号码
    mobile_phone = StringField(required=True)
    #密码md5
    password_md5 = StringField(required=True)
    #账户余额
    money = FloatField(required=True,default=0.0)
    #支付密码
    pay_password_md5 = StringField(required=True,default='')

    #创建时间
    create_time = DateTimeField(required=True)
    #最后登录时间
    last_login_time = DateTimeField(required=True)
    #是否被冻结
    disabled = IntField(required=True, default=0)
    #账户状态, 当出现问题的时候用来反馈
    status = StringField(required=False, default='')
    #是否被删除
    deleted = IntField(required=True, default=0)
