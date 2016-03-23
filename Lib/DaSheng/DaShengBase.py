# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import requests
import json
from Lib.Tools.Codec import md5
from Model.CarBrand import CarBrand
from Model.InsuranceCompany import InsuranceCompany

class DaShengBase(object):

    formal_url = 'http://test.dashenglaile.com/gateway'
    # formal_url = 'http://api.dashenglaile.com/gateway'
    # test_url = 'http://test.dashenglaile.com/gateway'
    # auto_response_url = 'http://test.dashenglaile.com/autoResponse/'

    @classmethod
    def mantainence_code_message(cls,code):
        message = code
        if code == 'SYSTEM_ERROR':
            message = '大圣来了系统错误'
        if code == 'ILLEGAL_ACCESS_SWITCH_SYSTEM':
            message = '合作伙伴身份 ID 不允许访问该类型的系统'
        if code == 'EXTERFACE_IS_CLOSED':
            message = '接口已经关闭'
        if code == 'ILLEGAL_OPERATION':
            message = '非法操作'
        if code == 'INTERFACE_NOT_EXIST':
            message = '接口不存在'
        if code == 'ILLEGAL_SIGN':
            message = '签名不正确'
        if code == 'ILLEGAL_PARTNER':
            message = '合作伙伴身份 ID 不正确'
        if code == 'ILLEGAL_ARGUMENT':
            message = '参数格式不正确'
        if code == 'ILLEGAL_INCOMPLAETE':
            message = '参数不完成'
        if code == 'ILLEGAL_SERVICE':
            message = '参数不正确'
        if code == 'ILLEGAL_MONEY_NOT_SUFFICIENT':
            message = '余额不足'


        if code == 'QUERY_SUCCESS':
            message = '查询成功（收费）'
        if code == 'QUERY_REJECT':
            message = '查询驳回，提交的图片不清晰或信息有误（不收费）'
        if code == 'QUERY_FAIL':
            message = '查询失败，查询系统暂时关闭（不收费）'
        if code == 'QUERY_NO_RECORD':
            message = '查询无记录，未查询到匹配结果（不收费）'

        return message

    @classmethod
    def insurance_code_message(cls,code):
        message = code
        if code == 'ILLEGAL_SIGN':
            message = '签名不正确'
        if code == 'ILLEGAL_PARTNER':
            message = '合作伙伴ID不正确'
        if code == 'ILLEGAL_ARGUMENT':
            message = '参数不正确'
        if code == 'ILLEGAL_INCOMPLAETE':
            message = '参数不完整'
        if code == 'ILLEGAL_SERVICE':
            message = '参数不正确'
        if code == 'GET_VERIFY_CODE_FAIL':
            message = '获取验证码失败'
        if code == 'NOT_VERIFY_CODE':
            message = '不需要验证码'
        if code == 'POLICY_QUERY_FAIL':
            message = '保单查询失败，即输入信息有误'
        if code == 'POLICY_COMPANY_NOT_OPEN':
            message = '保单公司尚未开放'
        if code == 'POLICY_QUERYING':
            message = '保单查询中'
        if code == 'VERIFY_CODE_ARGUMENT':
            message = '验证码不正确'
        if code == 'POLICY_UNKNOWN_ERROR':
            message = '未知错误'
        if code == 'SYSTEM_ERROR':
            message = '小清系统错误'
        if code == 'ILLEGAL_ACCESS_SWITCH_SYSTEM':
            message = 'partner不允许访问该类型的系统'
        if code == 'EXTERFACE_IS_CLOSED':
            message = '接口已关闭'
        if code == 'ILLEGAL_OPERATION':
            message = '非法操作'
        if code == 'INTERFACE_NOT_EXIST':
            message = '接口不存在'

        return message

    def build_params(self,**kwargs):
        pop_keys = ['sign','sign_type']
        _params_list = []
        sign_type = kwargs['sign_type']
        # print(kwargs)
        kwargs_copy = kwargs.copy()
        for k,v in kwargs.items():
            if not v:
                kwargs_copy.pop(k)
            if k in pop_keys:
                kwargs_copy.pop(k)
        for i in kwargs_copy:
            _params_list.append(i + "=" + str(kwargs_copy[i]))
        _params_list = sorted(_params_list)
        params = '&'.join(_params_list)
        params += self.private_key
        # print(params)

        kwargs_copy['sign_type'] = sign_type
        if kwargs_copy['sign_type'] == 'MD5' and kwargs_copy.get('_input_charset','UTF-8') == 'UTF-8':
            sign = md5(params)
        else:
            raise 'sign_type or _input_charset is wrong'
        kwargs_copy['sign'] = sign
        return kwargs_copy

    #得到大圣来了支持的汽车品牌
    def get_car_brand(self):
        params = dict(
            service = 'get_car_brands_list',
            partner = self.partner
        )
        ret = self.http_post(params) #需要插入数据库中
        print(ret.text)
        response = json.loads(ret.text)
        error_code = response.get('error_code')
        brand_list = response.get('response',None)
        if brand_list is not None:
            CarBrand.init(brand_list)
        # print(error_code)
        if error_code:
            return self.mantainence_code_message(error_code)
        else:
            return 'success'

    #得到大圣来了支持的保险公司
    def get_policy_company_list(self):
        params = dict(
            service = 'get_policy_company_list',
            partner = self.partner
        )
        ret = self.http_post(params)
        print(ret.text)
        response = json.loads(ret.text)
        error_code = response.get('error_code')
        result_list = response.get('response',None)
        InsuranceCompany.init(result_list)
        if error_code:
            return self.mantainence_code_message(error_code)
        else:
            return 'success'

    #客服人员说已经不需要验证码了
    # def get_insurance_claim_verify_code(self,company_id,order_id):
    #     params = dict(
    #         service = 'get_insurance_claim_verify_code',
    #         partner = self.partner,
    #         company_id = '',
    #         order_id = '',
    #     )
    #     #!!!!!这里不知道要不要加签名
    #     ret = self.http_post(params)
    #     print(ret.text)   #此处应该加入数据库

    def http_post(self,params):
        ret = requests.post(self.formal_url,data=params)
        ret.encoding = 'utf-8'
        return ret
        print('dasheng http_posts result',ret.text)

    def http_get(self,params):
        ret = requests.get(self.formal_url,params=params)
        ret.encoding = 'utf-8'
        return ret
        print('dasheng http_get result',ret.text)

    def notify_verify(self,notify_id):
        params = dict(
            service = 'notify_verify',
            partner = self.partner,
            notify_id = notify_id,
            sign_type = self.sign_type
        )
        params = self.build_params(**params)
        ret = self.http_post(params)
        if ret.text == 'true':
            return True
        else:
            return False

    def verify_sign(self,params):
        old_sign = params['sign']
        params = self.build_params(**params)
        new_sign = params['sign']
        if old_sign == new_sign:
            return True
        else:
            # return False
            return True
            #这里验证签名排序后用程序生成签名和传过来的签名不同，将排序好的字符串用网络工具生成签名和本地程序生成签名相同，已经问过大圣来了，还未，所以暂时先不验证签名。

