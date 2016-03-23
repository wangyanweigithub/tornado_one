# -*- coding: utf-8 -*-
from mongoengine import *
from setting import database_name

__author__ = 'renpan'

connect(database_name)

class InsuranceCompany(Document):

    company_id = IntField(required=True)
    letter = StringField(required=True)
    #保险品牌名称
    title = StringField(required=True)
    #
    is_finish = IntField(default=0)
    #
    is_need_code = IntField(required=True)

    @classmethod
    def get_baoxian_brand_list(cls):
        bb_list = cls.objects().all()
        _bb_list = []
        for bb in bb_list:
            _bb = dict(bb.to_mongo())
            _bb_list.append(_bb)
        return _bb_list

    @classmethod
    def init(cls,result_list):
        cls.drop_collection()
        for i in result_list:
            company = cls()
            company.company_id = i.get('id',None)
            company.letter = i.get('letter',None)
            company.title = i.get('title',None)
            company.is_finish = i.get('is_finish',None)
            company.is_need_code = i.get('is_need_code',None)
            company.save()
