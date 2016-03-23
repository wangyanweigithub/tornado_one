# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from mongoengine import *
from datetime import datetime
from Model.CarBrand import CarBrand
from setting import database_name

connect(database_name)

class TransactionRecordType:
    #银行卡充值
    credit_card = 100
    #支付宝充值
    alipy = 200
    #微信充值
    wechat = 300
    #查保险消费
    insurance = 400
    #查保养消费
    mantenace = 500
    #查违章消费
    peccancy = 600

class TransactionRecordStatus(object):
    #待支付
    waiting = 100
    #成功
    success = 200
    #失败
    fail = 300

class Method_Payment(object):
    #账户余额支付
    account = 100
    #银行卡支付
    credit_card = 200
    #支付宝支付
    alipy = 300
    #微信支付
    wechat = 400

class TransactionRecord(Document):
    #会员 id
    member_id = ObjectIdField(required=True)
    #交易记录类型
    type = IntField(required=True)
    #交易标题
    title = StringField(required=True)
    #金额
    money = FloatField(required=True, default=0)
    #支付方式
    method_payment = IntField(required=True,default=Method_Payment.account)
    #交易描述
    description = StringField(required=False, default='')
    #交易备注
    remark = StringField(required=False, default='')
    #交易状态
    status = IntField(required=True, default=TransactionRecordStatus.waiting)
    #当支付失败后说明原因使用
    reason = StringField(required=False, default='')
    #创建时间
    create_time = DateTimeField(required=True)

    #保养查询记录
    @classmethod
    def generate_mantaince_order(cls,member_id,brand_id):
        obj = cls()
        obj.member_id = member_id
        obj.type = TransactionRecordType.mantenace
        brand_obj = CarBrand.get_brand(brand_id)
        obj.title = '消费  ' + brand_obj.brand_name
        obj.money = brand_obj.brand_price
        obj.status = TransactionRecordStatus.waiting
        obj.create_time = datetime.now()
        obj.save()

    #充值记录
    @classmethod
    def recharge(cls,member_id,money,transactionrecordtype):
        obj = cls()
        obj.member_id = member_id
        obj.type = transactionrecordtype
        obj.title = '充值'
        obj.money = money
        obj.status = TransactionRecordStatus.waiting
        obj.create_time = datetime.now()
        obj.save()