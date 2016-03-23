# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from mongoengine import *
import setting

connect(setting.database_name)

class MaintenaceResult(Document):

    #通知时间
    notify_time = DateTimeField(required=True)
    #通知类型
    notify_type = StringField(required=True)
    #通知校验 ID
    notify_id = StringField(required=True)
    #合作伙伴订单号
    order_id = StringField(required=True)
    #签名方式
    sign_type = StringField(required=True)
    #签名
    sign = StringField(required=True)

    #业务参数
    #最后到店时间
    last_time_to_shop = DateTimeField(required=False)
    #公里数
    total_mileage = IntField(required=False)
    #事故次数
    number_of_accidents = IntField(required=False)
    #车型品牌 ID
    car_brand_id = StringField(required=True)
    #车型品牌名称
    car_brand = StringField(required=True)
    #结果描述
    result_description = StringField(required=True)
    #结果图片
    result_images = StringField(required=False)
    #查询结果
    result_status = StringField(required=True)
    #订单创建时间
    gmt_create = DateTimeField(required=False)
    #订单完成时间
    gmt_finish = DateTimeField(required=False)