# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from Lib.WeiZhang.WeiZhangManner import WeiZhangManner
from Controller.Main.BaseProcess import BaseProcess
from Lib.TornadoExtend import HttpResponseCode
from Model.CarType import CarType
from Lib.Tools.JsonExtend import JsonExtend
from Model.OrderForPeccancy import OrderForPeccancy

class PeccancyProcess(BaseProcess):
    #违章查询
    def query(self):
        params = self.get_params()
        access_token = params.get('access_token',None)
        ret = self.check_access_token(access_token)
        if not ret['value']:
            return self.on_response_fail(ret['code'],ret['message'])
        params['member_id'] = ret['member'].id

        license_plate = params.get('license_plate',None)        #车牌号
        vin = params.get('vin',None)                            #车架号
        enginenumber = params.get('enginenumber','')            #发动机号
        car_type_value = params.get('car_type_value',None)      #车辆类型序号
        type = params.get('type',None)                          #调用那个网站，需要有三个网站

        order = OrderForPeccancy.generate_order(params)
        params = dict(license_plate=license_plate,vin=vin,enginenumber=enginenumber,car_type_value=car_type_value)
        manager = WeiZhangManner(int(type))
        ret = manager.run(params)
        if isinstance(ret,tuple):
            result = self.save_peccancy(ret,order.id)
            return self.on_response_success(result)
        ret['order_id'] = order.id
        ret['notice'] = '有验证码，请输入验证码'
        return self.on_response_success(ret)

    def has_verify_code(self):
        params = self.get_params()
        access_token = params.get('access_token', None)
        code = params.get('code', None)
        post_verify_code_url = params.get('post_verify_code_url', None)
        post_verify_code_cookie = params.get('post_verify_code_cookie', None)
        type = params.get('type',None)
        order_id = params.get('order_id',None)

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token不正确或已过期, 请检查')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'用户不正确, 请检查')

        manager = WeiZhangManner(int(type))
        ret = manager.verify_code_get_result(post_verify_code_url,code,post_verify_code_cookie)
        result = self.save_peccancy(ret,order_id)
        return self.on_response_success(result)

    #获取所有城市列表
    def get_all_city_list(self):
        params = self.get_params()
        access_token = params.get('access_token',None)
        ret = self.check_access_token(access_token)
        if not ret['value']:
            return self.on_response_fail(ret['code'],ret['message'])

        city_list = ['津', '冀', '晋', '蒙', '辽', '吉', '黑', '沪', '苏', '浙', '皖', '闽', '赣', '鲁', '豫', '鄂',
                        '湘', '粤', '桂', '琼', '渝', '川', '贵', '云', '藏', '陕', '甘', '青', '宁', '新', '港', '澳', '台']
        return self.on_response_success(city_list)

    #获取所有汽车类型
    def get_car_type_list(self):
        params = self.get_params()
        access_token = params.get('access_token',None)
        ret = self.check_access_token(access_token)
        if not ret['value']:
            return self.on_response_fail(ret['code'],ret['message'])

        _list = CarType.get_all_car_type()
        ret = JsonExtend.mongoengine_query_to_list(_list)
        return self.on_response_success(ret)

    #获取用户所有的违章订单
    def query_order_list(self):
        params = self.get_params()
        access_token = params.get('access_token', None)
        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token不正确或已过期, 请检查')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'用户不正确, 请检查')

        _order_list = OrderForPeccancy.get_order_list_by_member(member.id)
        ret = JsonExtend.mongoengine_query_to_list(_order_list)
        return self.on_response_success(ret)

    #获取用户所有的违章订单的扣分总数和扣款总数
    def query_total_weizhang(self):
        params = self.get_params()
        access_token = params.get('access_token', None)
        order_id = params.get('order_id',None)
        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token不正确或已过期, 请检查')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'用户不正确, 请检查')

        order = OrderForPeccancy.get_order_by_id(order_id)
        # ret = []
        # _order_list = OrderForPeccancy.get_order_list_by_member(member.id)
        # # ret = JsonExtend.mongoengine_query_to_list(_order_list)
        if not order:
            return self.on_response_success()

        fen = money = num = 0
        if order.weizhang:
            for i in order.weizhang:
                fen += i.fen
                money += i.money
                num += 1
        ret = dict(license_plate=order.license_plate,weizhangnum=num,fen=fen,money=money)

        return self.on_response_success(ret)

    #违章查询结果详情
    def query_violation(self):
        params = self.get_params()
        access_token = params.get('access_token', None)
        order_id = params.get('order_id',None)
        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.fail,'access_token不正确或已过期, 请检查')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'用户不正确, 请检查')

        order = OrderForPeccancy.get_order_by_id(order_id)
        ret = order.to_mongo()
        return self.on_response_success(ret)