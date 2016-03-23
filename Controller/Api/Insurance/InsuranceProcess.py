# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
from Controller.Main.BaseProcess import BaseProcess
from Lib.TornadoExtend import HttpResponseCode
from Model.InsuranceCompany import InsuranceCompany
from Lib.DaSheng.DaShengManager import DaShengInsurance
from Model.OrderForInsurance import OrderForInsurance
from Lib.Tools.JsonExtend import JsonExtend
from Model.InsuranceResult import InsuranceResult

class InsuranceProcess(BaseProcess):

    def get_insurance_company_list(self):
        params = self.get_params()
        access_token =  params.get('access_token',None)
        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token 错误或已过期')

        ret = InsuranceCompany.get_baoxian_brand_list()
        return self.on_response_success(ret)

    def insurance_query(self):
        params = self.get_params()
        access_token = params.get('access_token',None)
        company_id = params.get('company_id',None)
        policy_no = params.get('policy_no',None)
        identify_no = params.get('identify_no',None)
        remark = params.get('remark','')

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token 错误或已过期')

        if company_id is None or policy_no is None or identify_no is None:
            return self.on_response_fail(HttpResponseCode.fail,'缺少必要参数')

        order = OrderForInsurance.generate_order(access.member_id,company_id,policy_no,identify_no,remark)

        result = DaShengInsurance().query_insurance(order)
        if isinstance(result,str):
            return self.on_response_fail(HttpResponseCode.fail,result)

        # ret = JsonExtend.to_json(result.to_mongo())
        # params = dict(ResultInsurance=result.insurance,ResultClaim=result.claim)
        # ret = dict(html='/Common/InsuranceResult.html',params=params)
        return self.on_response_success()

    def insurance_record_list(self):
        params = self.get_params()
        access_token = params.get('access_token',None)

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token 错误或已过期')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'没有这个用户, 请检查')

        _order_list = OrderForInsurance.objects(member_id=member.id).all()
        order_list = JsonExtend.mongoengine_query_to_list(_order_list)
        return self.on_response_success(order_list)

    #保险订单基本信息
    def insurance_order_detail(self):
        params = self.get_params()
        access_token = params.get('access_token',None)
        order_id = params.get('order_id',None)

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token 错误或已过期')

        order = InsuranceResult.get_result_by_order_id(order_id)
        params = dict(insurance=order.insurance)
        ret = dict(html='Common/InsuranceResult.html',params=params)
        return ret

    #保险理赔信息
    def payment_of_claims_info(self):
        params = self.get_params()
        access_token = params.get('access_token',None)
        order_id = params.get('order_id',None)

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token 错误或已过期')

        order = InsuranceResult.get_result_by_order_id(order_id)
        params = dict(claim=order.claim)
        ret = dict(html='Common/Claim.html',params=params)
        return ret