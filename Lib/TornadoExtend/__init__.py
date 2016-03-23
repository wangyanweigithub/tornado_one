# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

class AccessSource(object):
    web = 0
    browser_extension = 10
    wechat = 20
    ios_iphone = 100
    ios_ipod_touch = 101
    ios_ipad = 102
    mobile = 103
    android_phone = 200
    android_pad = 201

class HttpResponseCode(object):
    success = 200
    fail = 400
    access_token_expired = 401