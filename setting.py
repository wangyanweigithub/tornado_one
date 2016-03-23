# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
import os
import sys

database_host = '127.0.0.1'
database_port = 27017
database_name = 'carmirror'

server_host = '0.0.0.0'
project_path = os.path.dirname(__file__)
verifycode_img = 'http://203.195.161.213:11811/assets/VerifyCodeImg/VerifyCode.jpg'
# notify_url = 'http://www.zhaochejing.com/dasheng'
notify_url = 'http://203.195.161.213:11811/dasheng'
# verifycode_img = 'http://192.168.0.101:11811/assets/VerifyCodeImg/VerifyCode.jpg'
env = {
    "debug": False,
    # "xsrf_cookies": True,
    "cookie_secret": 'MDA4ZDFhZDQtYmY0Yi0xMWU1LWE2MWMtYWNiYzMyN2NhOTIx',
    "static_url_prefix": '/assets/',
    "static_path": os.path.join(project_path, "Web/Assets"),
    "template_path": os.path.join(project_path, "Web/Views"),
}
