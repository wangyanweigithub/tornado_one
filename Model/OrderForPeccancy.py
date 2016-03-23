# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from datetime import datetime
from mongoengine import *
from Model import OrderStatus
import setting

connect(setting.database_name)

class PeccancyItem(EmbeddedDocument):
    #省缩写
    province = StringField(required=True)
    #城市缩写
    city = StringField(required=True)
    #时间
    date  = DateTimeField(required=True)
    #地点
    area = StringField(required=True)
    #违章行为
    act = StringField(required=True)
    #扣分
    fen = IntField(required=True)
    #罚款
    money = IntField(required=True)
    #是否处理，暂时不用
    handle = IntField(required=True,default=0)



class OrderForPeccancy(Document):
    #用户id
    member_id = ObjectIdField(required=True)
    #车牌号
    license_plate = StringField(required=True)
    #车架号
    vin = StringField(required=True)
    #发动机号，可不填
    enginenumber = StringField(required=True)
    #车辆类型序号
    car_type_value = StringField(required=True)
    #线路类型
    type = IntField(required=True)
    create_time = DateTimeField(default=datetime.now(),required=True)
    weizhang = ListField(EmbeddedDocumentField('PeccancyItem'),default=None)
    status = IntField(required=True,default=OrderStatus.querying)
    remark = StringField(required=False)

    @classmethod
    def generate_order(cls,params):
        order = cls()
        order.member_id = params['member_id']
        order.license_plate = params['license_plate']
        order.vin = params['vin']
        order.enginenumber = params['enginenumber']
        order.car_type_value = params['car_type_value']
        order.type = params['type']
        order.save()
        return order

    @classmethod
    def get_order_list_by_member(cls,member_id):
        order = cls.objects(member_id=member_id).all()
        return order

    @classmethod
    def get_order_by_id(cls,id):
        order = cls.objects(id=id).first()
        return order

