# -*- coding: utf-8 -*-
from mongoengine import *
from Model import Sex
from setting import database_name

connect(database_name)

class AdminMember(Document):

    #用户名
    username = StringField(required=True)
    #手机号码
    mobile_phone = StringField(required=False, default=None)
    #md5过后的密码
    password_md5 = StringField(required=True)

    #optional
    #姓名
    name = StringField(required=False)
    #电子邮件
    mail = StringField(required=False)
    #性别
    sex = IntField(required=False, default=Sex.unknow)
    #身份证号
    id_card = StringField(required=False)

    #other
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
