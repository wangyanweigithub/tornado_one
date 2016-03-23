# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import rsa
class AlipyPay(object):

    partner = ''
    service = 'mobile.securitypay.pay'
    _input_charset = 'utf-8'
    sign_type = 'RSA'
    notify_url = ''
    # #客户端号，可空
    rn_check = 'T'
    # #卖家支付宝帐号
    seller_id = ''



    def build_params(self,out_trade_no,subject,payment_type,
                     total_fee,body,rn_check,extern_token,out_context,appenv=None,goods_type='1',it_b_pay='30m'):

        params = dict(
            service = self.service,
            partner =self.partner,
            _input_charset =self._input_charset,
            sign_type = self.sign_type,
            notify_url = self.notify_url,
            app_id = self.app_id,
            seller_id = self.seller_id,
            #客户端来源
            appenv = appenv,
            out_trade_no = out_trade_no,
            subject = subject,
            payment_type = payment_type,
            total_fee = total_fee,
            body = body,
            goods_type = goods_type,
            rn_check = self.rn_check,
            it_b_pay = it_b_pay,
            extern_token = extern_token,
            out_context = out_context
        )

