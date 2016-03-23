from datetime import datetime
from mongoengine import *
from Model import OrderStatus
from Model.InsuranceCompany import InsuranceCompany
import setting

connect(setting.database_name)

class OrderForInsurance(Document):

    #客户id
    member_id = ObjectIdField(required=True)
    #保险公司id
    company_id = StringField()
    #保险公司名称
    company_title = StringField()
    #保单号
    policy_no = StringField(required=True)
    #身份证号
    identify_no = StringField(required=True)
    #某些需要验证码的保险公司，最新版不需要
    verify_code = StringField()
    # 查询状态
    status = IntField(required=True, default=OrderStatus.querying)
    # 订单创建日期
    create_time = DateTimeField(required=True)
    # 备注
    remark = StringField()
    #有无理赔 0没有理赔，1有理赔
    claim_status = IntField(required=True,default=0)

    @classmethod
    def find_one_with_id(cls, _id):
        orderForInsurance = OrderForInsurance.objects(ObjectId=_id).first()
        return orderForInsurance

    @classmethod
    def generate_order(cls, member_id,  company_id, policy_no, identify_no,remark):
        order = OrderForInsurance()
        baoxian = InsuranceCompany.objects(company_id=company_id).first()
        order.member_id = member_id
        order.company_id = company_id
        order.company_title = baoxian.title
        order.policy_no = policy_no
        order.identify_no = identify_no
        order.status = OrderStatus.querying
        order.create_time = datetime.now()
        order.remark = remark
        order.save()
        return order

