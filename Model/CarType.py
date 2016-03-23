# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from mongoengine import *
import setting

connect(setting.database_name)

class CarType(Document):
    #车辆类型的序号
    value = StringField(required=True)
    #车辆类型
    type = StringField(required=True)

    @classmethod
    def get_all_car_type(cls):
        return cls.objects().all()