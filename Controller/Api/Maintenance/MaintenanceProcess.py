# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
import json
from datetime import datetime
from Controller.Main.BaseProcess import BaseProcess
from Model.CarBrand import CarBrand
from Lib.TornadoExtend import HttpResponseCode
from Lib.DaSheng.DaShengManager import DaShengMaintenance
from Model.OrderForMaintenance import OrderForMaintenance
from Lib.Tools.UploadFileProcess import UploadFileProcess
from Lib.Tools.JsonExtend import JsonExtend
from Model.MaintenaceResult import MaintenaceResult

class MaintenanceProcess(BaseProcess):

    #获取汽车品牌列表
    def get_brand_list(self):
        params = self.get_params()
        access_token = params.get('access_token', None)

        if access_token is None:
            return self.on_response_fail(HttpResponseCode.fail, '缺少必要参数')

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.access_token_expired, '您的 access_token 不存在或已过期, 请重新登录')

        car_brand_list = CarBrand.get_brand_list()
        return self.on_response_success(car_brand_list)

    #提交保养查询订单
    def submit_maintenance_order(self):
        params = self.get_params()
        brand_id = params.get('brand_id',None)
        remarks = params.get('remarks',None)
        access_token = params.get('access_token',None)

        if brand_id and remarks and access_token is None:
            return self.on_response_fail(HttpResponseCode.fail,'缺少必要参数')

        access = self.get_access_with_access_token(access_token)

        #上传图片
        date = datetime.today().strftime('%Y/%m/%d')
        params = dict(method='upload',path='/cars/' + date + '/')
        up_files = self.make_files(self.files)
        if up_files is None:
            self.on_response_fail(HttpResponseCode.fail,'请上传证件照')

        ret = UploadFileProcess.do_post('image', UploadFileProcess.buildup_arguments(params), files=up_files)
        img_url = json.loads(ret).get('value',None)

        order = OrderForMaintenance.generate_order(access.member_id,brand_id,img_url[0])
        ret = DaShengMaintenance().query_mantainence(order)
        if ret.get('result',None):
            return self.on_response_success()
        else:
            return self.on_response_fail(HttpResponseCode.fail,ret['message'])

    #返回保养查询结果列表
    def get_maintenance_list(self):
        params = self.get_params()
        access_token = params.get('access_token',None)
        status = params.get('status',None)
        remarks = params.get('remarks',None)
        brand = params.get('brand',None)

        if access_token is None:
            return self.on_response_fail(HttpResponseCode.fail, '缺少必要参数')

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.access_token_expire, '您的 access_token 不存在或已过期, 请重新登录')

        member = self.get_member_with_member_id(access.member_id)

        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'没有这个用户, 请检查')

        if status is not None:
            _order_list = OrderForMaintenance.objects(member_id=member.id,status=status).all()
        elif remarks is not None:
            _order_list = OrderForMaintenance.objects(member_id=member.id,remark=remarks).all()
        elif brand is not None:
            _order_list = OrderForMaintenance.objects(member_id=member.id,brand_title=brand).all()
        else:
            _order_list = OrderForMaintenance.objects(member_id=member.id).all()
        order_list = JsonExtend.mongoengine_query_to_list(_order_list)
        return self.on_response_success(order_list)

    #保养查询成功详情
    def maintenance_record_detail(self):
        params = self.get_params()
        order_id = params.get('order_id',None)
        access_token = params.get('access_token',None)

        if access_token is None:
            return self.on_response_fail(HttpResponseCode.fail, '缺少必要参数')

        access = self.get_access_with_access_token(access_token)
        if access is None:
            return self.on_response_fail(HttpResponseCode.access_token_expire, '您的 access_token 不存在或已过期, 请重新登录')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return self.on_response_fail(HttpResponseCode.fail,'没有这个用户, 请检查')

        order = OrderForMaintenance.objects(id=order_id).first()
        if order is None:
            return self.on_response_fail(HttpResponseCode.fail,'这个用户没有保养订单')

        print('order is is ',order.id,'order_id is ',order_id)
        _result = MaintenaceResult.objects(order_id=order_id).first()
        if _result is None:
            return self.on_response_success('这个订单结果还未生成，请稍后查询')
        result = dict(_result.to_mongo())
        return self.on_response_success(result)