# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
from mongoengine import *
import setting

connect(setting.database_name)

class Version(Document):
    #版本信息
    version = StringField(required=True)
    #版本更新时间
    date = DateTimeField(required=True)
    #备注
    remark = StringField(required=True)
    #是否是最新版本，status是1的版本是最新版本
    status = IntField(required=True,default=0)
    #SDK地址
    url = StringField(required=True,default='')
    @classmethod
    def get_latest_version(cls):
        obj = cls.objects(status=1).first()
        return obj