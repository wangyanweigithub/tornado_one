# -*- coding: utf-8 -*-
from Lib.Sms.SmsBase import SmsBase, SmsSendReponse


class SmsJianzhou(SmsBase):

    def __init__(self):
        super().__init__()
        self.base_url = 'http://www.jianzhou.sh.cn/JianzhouSMSWSServer/http/'
        self.username = ''
        self.password = ''

    def url_process(self, method):
        return self.base_url + method

    def send(self, phone_list=[], content='', signature=''):
        method = 'sendBatchMessage'
        params = dict(
            account=self.username,
            password=self.password,
            destmobile=';'.join(phone_list),
            msgText=content+signature
        )
        # return self.send_result_process('1234')
        return self.send_result_process(self.http_post(self.url_process(method), params))

    def send_result_process(self, response_text):
        rsp = SmsSendReponse()
        code = 0
        try:
            code = int(response_text)
        except:
            code = 0
        if code > 0:
            rsp.set_status(SmsSendReponse.out_success, response_text)
        elif response_text == '-1':
            rsp.set_status(SmsSendReponse.out_fail_no_money)
        elif response_text == '-2':
            rsp.set_status(SmsSendReponse.out_fail_account_error)
        elif response_text == '-3':
            rsp.set_status(SmsSendReponse.out_fail_connect_serve_error)
        elif response_text == '-4':
            rsp.set_status(SmsSendReponse.out_fail_out_of_time)
        elif response_text == '-5':
            rsp.set_status(SmsSendReponse.out_fail_other_net_ip)
        elif response_text == '-10':
            rsp.set_status(SmsSendReponse.out_fail_timely_out_of_time)
        elif response_text == '-11':
            rsp.set_status(SmsSendReponse.out_fail_dest_number_in_black_list)
        elif response_text == '-12':
            rsp.set_status(SmsSendReponse.out_fail_content_forbidden_words)
        elif response_text == '-20':
            rsp.set_status(SmsSendReponse.out_fail_speeding_submitted)
        else:
            rsp.set_status(SmsSendReponse.out_fail_other)
        return rsp
