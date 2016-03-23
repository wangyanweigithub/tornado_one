# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import uuid
import io
from datetime import datetime
from tornado.web import decode_signed_value
from Model.Access import Access,AccessType
from Model.Member import Member
from Model.AdminMember import AdminMember
from Lib.Tools.Codec import md5
from Model import OrderStatus
from Lib.TornadoExtend import HttpResponseCode
from Model.OrderForPeccancy import OrderForPeccancy,PeccancyItem

class BaseProcess(object):

    def __init__(self,application=None,request_handler=None,method=None,response_params=None,remote_ip=None,agent_from=None,args=None,host=None,files=None):
        self.application = application
        self.request_handler = request_handler
        self.method = method
        self.response_params = response_params
        self.remote_ip = remote_ip
        self.agent_from = agent_from
        self.args = args
        self.host = host
        self.files = files

    def process(self):
        params = self.get_params()
        method = params.get('method',None)
        if method is None:
            return self.on_response_fail(HttpResponseCode.fail,'缺少必要参数')
        # try:
        return self.execute_method(method)
        # except Exception as e:
        #     print(e)
        #     return self.on_response_fail(HttpResponseCode.fail,'不支持的方法')

    def execute_method(self,name):
        return getattr(self,name)()

    def get_params(self):
        return self.args.get('params',None)

    def get_response_params(self):
        return self.response_params

    def check_files_is_empty(self):
        if len(self.files.keys()) > 0:
            return True
        else:
            return False

    def on_response_success(self,value=None):
        content = dict(code=HttpResponseCode.success,value=value)
        return content

    def on_response_fail(self,code,message):
        content = dict(code=code,message=message)
        return content

    def encode_access_token(self,access_token):
        return self.request_handler.create_signed_value('access_token',access_token).decode()

    def generate_access(self,member,device_token,source_from_description,update=False):
        if update:
            access = Access.objects(member_id=member.id, deleted=0).first()
            access.update_time = datetime.now()
            access.visit_ip_count += 1
            member.last_login_time = access.update_time
            member.save()
        else:
            access = Access()
            if isinstance(member, Member):
                access.member_type = AccessType.member
            elif isinstance(member, AdminMember):
                access.member_type = AccessType.admin_member
            access.member_id = member.id
            access.create_time = member.create_time
            access.update_time = access.create_time
            access.visit_ip_count = 1

        access.access_token = md5(str(uuid.uuid1()))
        access.source_from = self.response_params.get('source')
        access.source_from_description = source_from_description
        access.device_token = device_token
        access.from_ip = self.remote_ip
        access.agent_from = self.agent_from
        access.save()
        return access

    def get_member_with_mobile_phone(self, mobile_phone):
        member = Member.objects(mobile_phone=mobile_phone, deleted=0).first()
        return member

    def get_member_with_member_id(self, member_id):
        member = Member.objects(id=member_id, deleted=0).first()
        return member

    def get_access_with_access_token(self, access_token):
        access = Access.objects(access_token=access_token, deleted=0).first()
        return access

    def get_admin_member_with_username(self, username):
        admin_member = AdminMember.objects(username=username, deleted=0).first()
        return admin_member

    def get_admin_member_with_member_id(self, admin_member_id):
        admin_member = AdminMember.objects(id=admin_member_id, deleted=0).first()
        return admin_member

    def make_files(self,fiels):
        fiels = fiels.get('files',None)
        if fiels is None:
            return
        ret = []
        # _file = [(file_name, (file_name, open(file_name, mode='rb'), 'image/jpeg'))]
        for file in fiels:
            file_name = file['filename']
            file_body = file['body']
            _file = (file_name,(file_name,io.BytesIO(file_body),'image/jpeg'))
            ret.append(_file)
        return ret

    def check_access_token(self,access_token):
        access = self.get_access_with_access_token(access_token)
        if access is None:
            return dict(value=False,code=HttpResponseCode.access_token_expired,message='access_token 错误或已过期')

        member = self.get_member_with_member_id(access.member_id)
        if member is None:
            return dict(value=False,code=HttpResponseCode.fail,message='没有这个用户或账户已冻结')
        else:
            return dict(value=True,code='',member=member)

    def save_peccancy(self,ret,id):
        if isinstance(ret,tuple):
            ret = ret[0]['xml']
        elif isinstance(ret,dict):
            ret = ret['xml']
        else:
            return dict(message='结果错误')

        querystatus = int(ret['querystatus'])

        order = OrderForPeccancy.get_order_by_id(id)

        if querystatus < 0:
            order.status = OrderStatus.failer
            if querystatus == -50:
                order.remark = '这条线路今日查询次数超出'
            order.save()
            return self.on_response_fail(HttpResponseCode.fail,'查询失败')

        if querystatus == 0:
            order.status = OrderStatus.success
            order.remark = '没有违章'
            order.save()
            return self.on_response_success(dict(message='没有违章'))

        items = ret['weizhang']
        items = items['item']
        # print(items)
        weizhang_list = []
        # print(dir(items))
        for i in items:
            if isinstance(i,str):
                item = PeccancyItem()
                item.province = items[i]['province']
                item.city = items[i]['city']
                item.date = items[i]['date']
                item.area = items[i]['area']
                item.act = items[i]['act']
                item.fen = items[i]['fen']
                item.money = items[i]['money']
                item.handle = items[i]['handled']
                weizhang_list.append(item)
            else:
                item = PeccancyItem()
                item.province = i['province']
                item.city = i['city']
                item.date = i['date']
                item.area = i['area']
                item.act = i['act']
                item.fen = i['fen']
                item.money = i['money']
                item.handle = i['handled']
                weizhang_list.append(item)

        order.weizhang = weizhang_list
        order.status = OrderStatus.success
        order.save()
        return order.to_mongo()




