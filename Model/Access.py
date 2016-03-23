# -*- coding: utf-8 -*-

from mongoengine import *
from Lib.TornadoExtend import AccessSource
from setting import database_name

connect(database_name)

class AccessType(object):

    member = 1
    admin_member = 2

class Access(Document):

    #Access 记录的 Member 类型
    member_type = IntField(required=True)
    #记录的 Member ID
    member_id = ObjectIdField(required=True)
    #登录授权凭证
    access_token = StringField(required=True)
    #请求来源
    source_from = IntField(required=True, default=AccessSource.mobile)
    #请求来源说明
    source_from_description = StringField(required=False)
    #设备推送唯一标识
    device_token = StringField(required=False)
    #创建时间
    create_time = DateTimeField(required=True)
    #更新时间
    update_time = DateTimeField(required=True)
    #来源 ip
    from_ip = StringField(required=True)
    #来源 ip 请求次数
    visit_ip_count = IntField(required=True, default=0)
    #客户端标识
    agent_from = StringField(required=False)
    #是否删除
    deleted = IntField(required=True, default=0)
