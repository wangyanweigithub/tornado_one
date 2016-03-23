# -*- coding: utf-8 -*-
from Lib.Sms.SmsJianzhou import SmsJianzhou

class SmsManager(object):

    def __init__(self, sms_base=SmsJianzhou, debug=False):
        super().__init__()
        self.sms_base = sms_base
        self.debug = debug

    def send(self, phone_list=[], content='', signature=''):
        self.sms_base().send(phone_list=phone_list, content=content, signature=signature)

