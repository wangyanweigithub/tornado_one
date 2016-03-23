# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
import setting
from datetime import datetime
from mongoengine import *

connect(setting.database_name)

class MemberAdvice(Document):
    #用户id
    member_id = ObjectIdField(required=True)
    #建议内容
    content = StringField(required=True)
    #建议时间
    date = DateTimeField(required=True,default=datetime.now())
    #联系方式
    contactinformation = StringField(required=False)
    #建议是否处理
    status = IntField(required=True,default=0)
