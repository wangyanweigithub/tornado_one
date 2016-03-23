# -*- coding: utf-8 -*-
__author__ = 'renpan'
import requests


class SmsSendReponse(object):
    out_success = 200
    out_fail_no_money = 401
    out_fail_account_error = 402
    out_fail_connect_serve_error = 403
    out_fail_out_of_time = 404
    out_fail_other_net_ip = 405
    out_fail_timely_out_of_time = 406 #定时超时
    out_fail_dest_number_in_black_list = 407
    out_fail_content_forbidden_words = 408
    out_fail_speeding_submitted = 409 #超速提交
    out_fail_other = 410 #

    @staticmethod
    def get_error_string(code):
        ret = '未知错误，请重试'
        if code == SmsSendReponse.out_fail_no_money:
            ret = '余额不足'
        elif code == SmsSendReponse.out_fail_account_error:
            ret = '账户或者密码错误'
        elif code == SmsSendReponse.out_fail_connect_serve_error:
            ret = '连接服务器失败'
        elif code == SmsSendReponse.out_fail_out_of_time:
            ret = '超时'
        elif code == SmsSendReponse.out_fail_other_net_ip:
            ret = '其他错误，可能网络或者ip错误'
        elif code == SmsSendReponse.out_fail_timely_out_of_time:
            ret = '超过最大定时时间限制'
        elif code == SmsSendReponse.out_fail_dest_number_in_black_list:
            ret = '目标号码在黑名单'
        elif code == SmsSendReponse.out_fail_content_forbidden_words:
            ret = '内容包含违禁词'
        elif code == SmsSendReponse.out_fail_speeding_submitted:
            ret = '超速提交'
        elif code == SmsSendReponse.out_fail_other:
            ret = '其他错误，请重试'
        return ret

    def set_status(self, response_code, msg_id=None):
        self.response_code = response_code
        self.msg_id = msg_id

    def get_status(self):
        return (self.response_code, self.msg_id)


class SmsBase(object):

    def __init__(self):
        super().__init__()
        self.timeout = 120

    def http_post(self, url='', params={}, headers=None):
        ret = requests.post(url, data=params, timeout=self.timeout, headers=headers)
        return ret.text

    def http_get(self, url='', params={}, headers=None):
        ret = requests.get(url, params=params, timeout=self.timeout, headers=headers)
        return ret.text

    def send(self, phone_list=[], content='', signature=''):
        raise Exception('You must overwrite the function')
