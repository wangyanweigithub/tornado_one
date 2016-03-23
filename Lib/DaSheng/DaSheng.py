# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from datetime import datetime
from Lib.DaSheng.DaShengBase import DaShengBase
import json
import setting
from Model.InsuranceResult import InsuranceResult,ResultInsurance,ResultClaim
from Model.OrderForInsurance import OrderForInsurance

class DaSheng(DaShengBase):

    partner = '7066715120801720'
    private_key = '63ba368e10e96616e15951c1d2012ef2'
    notify_url = setting.notify_url
    sign_type = 'MD5'

    def mantainence_query(self,car_brand_id,image_type,image,order_id,engine_number=None):

        params = dict(
            service = 'create_query_policy_by_partner',
            partner = self.partner,
            _input_charset = 'UTF-8',
            sign_type = 'MD5',
            notify_url = self.notify_url,
            car_brand_id = car_brand_id,
            image_type = image_type,
            image = image,
            order_id = order_id,
            engine_number = engine_number
        )

        params = self.build_params(**params)

        #测试端口，是用get方法，结果是接口不存在，这个接口可能取消了
        # testurl = 'http://test.dashenglaile.com/autoResponse'
        # ret = self.http_get(params)
        # print(ret.text)
        # return

        ret = self.http_post(params)
        print(ret)
        print(ret.text)
        result = json.loads(ret.text)
        if not result.get('error_code',None):
            ret = dict(result=True,message='')
        else:
            message = self.mantainence_code_message(result['error_code'])
            ret = dict(result=False,message=message)
        return ret

        #order.company_id,order.policy_no,order.identify_no,order.remark
    def insurance_query(self,company_id,order_id,policy_no,identify_no,verify_code=None,_input_charset='UTF-8'):

        params = dict(
            service = 'create_query_insurance_claim_by_partner',
            partner = self.partner,
            _input_charset = _input_charset,
            sign_type = self.sign_type,
            company_id = company_id,
            order_id = str(order_id),
            policy_no = policy_no,
            identify_no = identify_no,
            verify_code = verify_code,
        )

        params = self.build_params(**params)
        ret = self.http_post(params)
        result = json.loads(ret.text)
        # print(result)

        err_code = result.get('error_code',None)
        if err_code != '':
            message = self.insurance_code_message(err_code)
            return message

        ret = result['response']

        claim = ret.get('claim',None)
        start_time = ret.get('start_time',None)
        end_time = ret.get('end_time',None)
        insurance = ret.get('insurance',None)
        plate_number = ret.get('plate_number',None)

        insurance_list = []
        claim_list = []
        for i in claim:
            _claim = ResultInsurance()
            _claim.name = i.get('name',None)
            _claim.content = i.get('content',None)
            _claim.title = i.get('title',None)
            claim_list.append(_claim)
        for i in insurance:
            _insurance = ResultInsurance()
            _insurance.name = i.get('name',None)
            _insurance.content = i.get('content',None)
            _insurance.title = i.get('title',None)
            insurance_list.append(_insurance)

        order_for_insurance = OrderForInsurance.objects(id=order_id).first()
        if len(claim_list) > 0:
            order_for_insurance.claim_status = 1
            order_for_insurance.save()
        order = InsuranceResult()
        order.order_id = order_id
        order.create_time = datetime.now()
        order.insurance = insurance_list
        order.claim = claim_list
        order.start_time = start_time
        order.end_time = end_time
        order.plate_number = plate_number
        order.save()
        return order
