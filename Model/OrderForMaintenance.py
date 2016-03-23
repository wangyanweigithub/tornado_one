# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *
from Model.CarBrand import CarBrand
from Model import OrderStatus
import setting

connect(setting.database_name)

class OrderForMaintenance(Document):

    #用户id
    member_id = ObjectIdField(required=True)
    #车辆品牌id
    brand_id = StringField(required=True)
    #车辆品牌
    brand_title = StringField(required=True)
    #上传image类型，如果是上传图片则为‘url’，如果是vin，则等于‘vin’
    image_type = StringField(required=True,default='url')
    #上传行驶证或车辆铭牌照片
    id_image_url = StringField(required=True)
    #订单状态
    status = IntField(default=OrderStatus.querying)
    #发动机号
    engine_number = StringField(required=False)
    #订单创建时间
    create_time = DateTimeField(required=True)
    #备注信息
    remark = StringField()
    #大圣来了异步返回的保养查询结果
    result = ObjectIdField(required=False)

    @classmethod
    def generate_order(cls, member_id, brand_id, id_image_url):
        order = OrderForMaintenance()
        order.member_id = member_id
        order.brand_id = brand_id
        brand = CarBrand.get_brand(brand_id)
        order.brand_title = brand.brand_name
        order.id_image_url = id_image_url
        order.status = OrderStatus.querying
        order.create_time = datetime.now()
        order.save()
        return order