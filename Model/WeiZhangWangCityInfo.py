# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from mongoengine import *
from setting import database_name

connect(database_name)

class WeiZhangWangCityInfo(Document):

    #城市序号
    c_id = IntField(required=True)
    #城市名字
    c_name = StringField(required=True)
    id_360 = IntField(required=False)
    id_csy = IntField(required=False)
    #省和市的缩写
    jh_city_code = StringField(required=True)
    province_id_csy = IntField(required=False)
    c_pcode = IntField(required=False)
    #省
    p_name = StringField(required=True)
    #省缩写
    p_short_name = StringField(required=True)
    #车牌的首字母
    c_short_name = StringField(required=True)
    engineno = IntField(required=False)
    classno = IntField(required=False)
    registno = IntField(required=False)
