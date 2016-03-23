# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from mongoengine import *
from setting import database_name

connect(database_name)


class CarBrand(Document):

    #品牌id由大圣来了给出
    brand_id = IntField(required=True)
    #车辆品牌名称
    brand_name = StringField(required=True)
    #查询对应需要的money
    brand_price = IntField(required=True)
    #品牌首字母
    brand_letter = StringField(required=True)
    #提示信息
    brand_tips = StringField(required=False)
    #用大圣来了是否需要提供发动机号
    is_need_engine_number = StringField(required=True)
    #是否暂时不可用
    is_pause = StringField(required=True)
    #是否是子品牌
    is_child = BooleanField(default=False)
    #子品牌列表
    child_list = ListField(ObjectIdField(), default=None)

    @classmethod
    def remove_brand(cls,_id):
        cb = cls.objects(id=_id).first()
        cb.delete()

    @classmethod
    def get_brand(cls,_id):
        cb = cls.objects(brand_id=_id).first()
        return cb

    @classmethod
    def get_brand_from_objectid(cls,_id):
        cb = cls.objects(id=_id).first()
        return cb

    @classmethod
    def get_brand_list(cls):
        cb_list = cls.objects(is_child=False).all()
        _cb_list = []
        for cb in cb_list:
            _cb = dict(cb.to_mongo())
            if cb.child_list is not None:
                _tt = []
                for child in cb.child_list:
                    _child = cls.get_brand_from_objectid(child)
                    _tt.append(dict(_child.to_mongo()))
                _cb['child_list'] = _tt
            _cb_list.append(_cb)

        return _cb_list

    @classmethod
    def init(cls,result_list):
        CarBrand.drop_collection()

        for source_car_brand in result_list:
            brand_id = source_car_brand.get('brand_id', None)
            brand_name = source_car_brand.get('brand_name', None)
            brand_price = source_car_brand.get('brand_price', None)
            brand_letter = source_car_brand.get('brand_letter', None)
            brand_tips = source_car_brand.get('brand_tips', None)
            is_need_engine_number = source_car_brand.get('is_need_engine_number', None)
            is_pause = source_car_brand.get('is_pause', None)
            sub_list = source_car_brand.get('sub_list', None)

            cb = CarBrand()
            cb.brand_id = brand_id
            cb.brand_name = brand_name
            cb.brand_price = brand_price
            cb.brand_letter = brand_letter
            cb.brand_tips = brand_tips
            cb.is_need_engine_number = is_need_engine_number
            cb.is_pause = is_pause

            cb.save()

            t = []
            for child in sub_list:
                sub_brand_id = source_car_brand.get('brand_id', None)
                sub_brand_name = source_car_brand.get('brand_name', None)
                sub_brand_price = source_car_brand.get('brand_price', None)
                sub_brand_letter = source_car_brand.get('brand_letter', None)
                sub_brand_tips = source_car_brand.get('brand_tips', None)
                sub_is_need_engine_number = source_car_brand.get('is_need_engine_number', None)
                sub_is_pause = source_car_brand.get('is_pause', None)
                sub_cb = CarBrand()
                sub_cb.is_child = True
                sub_cb.brand_id = sub_brand_id
                sub_cb.brand_name = sub_brand_name
                sub_cb.brand_price = sub_brand_price
                sub_cb.brand_letter = sub_brand_letter
                sub_cb.brand_tips = sub_brand_tips
                sub_cb.is_need_engine_number = sub_is_need_engine_number
                sub_cb.is_pause = sub_is_pause
                sub_cb.save()
                t.append(sub_cb.id)

            if len(sub_list) > 0:
                cb.child_list = t
                cb.save()