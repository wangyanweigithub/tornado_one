# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from Lib.WeiZhang.WeiZhangManner import WeiZhangManner,WeiZhangItem
from Lib.DaSheng.DaShengManager import DaShengMaintenance,DaShengInsurance
from Controller.Api.Insurance import InsuranceProcess
from Model.InsuranceResult import InsuranceResult
from Model.OrderForPeccancy import OrderForPeccancy
from Controller.Main.BaseProcess import BaseProcess

#违章查询测试
def test_peccancy():

    _params = dict(
        # province = '福建',
        # city='三明',
        # license_plate='浙B598B0',           #车牌号
        license_plate='浙B591B6',           #车牌号
        vin = 'LS5A2ABE2DA109330',                   #车架号
        enginenumber = '',          #发动机号，可不填
        car_type_value = '02'         #车辆类型序号
    )
    params = _params.copy()
    params['member_id'] = '56c5350ce083921b3386196f'
    type = WeiZhangItem.typeA
    params['type'] = type
    order = OrderForPeccancy.generate_order(params)
    # params = dict(license_plate=license_plate,vin=vin,enginenumber=enginenumber,car_type_value=car_type_value)
    manager = WeiZhangManner(int(type))
    ret = manager.run(params)
    result = BaseProcess().save_peccancy(ret,order.id)

#保险查询测试
def test_insurance():
    insurance = DaShengInsurance()
    insurance_params = dict(
        company_id = '1',
        policy_no = '124122134',
        identify_no = '310984190807150048',
        remark = 'test'
    )
    for item in insurance_params:
        setattr(insurance,item,insurance_params[item])
    ret = insurance.query_insurance()
    print(ret)

#保养查询测试
def test_maintenance():
    maintenance = DaShengMaintenance()
    maintenance_params = dict(
        car_brand_id = '',
        image_type = '',
        image = '',
        order_id = '',
        engine_number = ''
    )
    for item in maintenance_params:
        setattr(maintenance,item,maintenance_params[item])
    ret = maintenance.query_mantainence()
    print(ret)

if __name__ == '__main__':
    test_peccancy()       #通过
    # test_insurance()      #
    # test_maintenance()      #
