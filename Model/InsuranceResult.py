# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from mongoengine import *
import setting

connect(setting.database_name)

class ResultInsurance(EmbeddedDocument):
    #保险查询结果内容
    content = StringField(required=True)
    #保险查询结果项目参数名
    name = StringField(required=False)
    #保险查询结果项目名
    title = StringField(required=True)

class ResultClaim(EmbeddedDocument):
    #保险查询结果内容
    content = StringField(required=True)
    #保险查询结果项目参数名
    name = StringField(required=False)
    #保险查询结果项目名
    title = StringField(required=True)

class InsuranceResult(Document):
    #大圣来了 第三方接口返回结果
    #订单id
    order_id = ObjectIdField(required=True)
    #创建时间
    create_time = DateTimeField(required=True)

    #返回结果
    # 保单内容
    insurance = ListField(EmbeddedDocumentField('ResultInsurance'),default=None)
    # 理赔信息标题
    claim = ListField(EmbeddedDocumentField('ResultClaim'),default=None)
    #保单开始时间
    start_time = StringField(required=True)
    #保单结束时间
    end_time = StringField(required=True)
    #车牌号
    plate_number = StringField(required=True)

    @classmethod
    def get_result_by_order_id(cls,order_id):
        obj = cls.objects(order_id=order_id).first()
        return obj