# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
import gene_tools
gene_tools.init_path()
import json
from Model.InsuranceCompany import InsuranceCompany
from Lib.DaSheng.DaShengManager import DaShengInsurance
from Lib import Tools

    #得到大圣来了支持的汽车品牌
def get_policy_company_list():
    dasheng = DaShengInsurance()

    params = dict(
        service = 'get_policy_company_list',
        partner = dasheng.partner
    )

    ret = dasheng.http_post(params)
    print(ret.text)
    response = json.loads(ret.text)
    error_code = response.get('error_code')
    result_list = response.get('response',None)
    InsuranceCompany.init(result_list)
    if error_code:
        return dasheng.mantainence_code_message(error_code)
    else:
        return 'success'

if __name__ == '__main__':
    get_policy_company_list()
