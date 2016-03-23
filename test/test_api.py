# -*- coding: utf-8 -*-
import calendar
import json
from datetime import datetime, date, timedelta

import requests

from Lib.Tools.Http import HttpCore
from Lib.TornadoExtend import AccessSource
from Lib.Tools.Codec import md5, base64_encode
from Lib.DaSheng import DaSheng

__author__ = 'renpan'

# base_url = 'http://0.0.0.0:13721/api/'
base_url = 'http://image.sfdai.com/api/'
app_id = '7c6081a09ca44ba69747b11db5f8ee65'
app_key = 'sdkfjiuyfssd6f77367826746734'


def buildup_url(method_path):
    p = base_url + method_path
    return p


def process_params(params):
    params['app_id'] = app_id
    str_b64 = base64_encode(json.dumps(params))
    return str_b64


def buildup_arguments(params):
    arguments = {}
    arguments['params'] = process_params(params)
    arguments['lang'] = 'zh_CN'
    arguments['time'] = str(datetime.now().strftime('%Y%m%d%H%M%S%f'))
    arguments['source'] = AccessSource.mobile
    arguments['sign'] = md5(md5(arguments['params'] + arguments['time']) + app_key)
    return arguments


def do_post(method_path, params, files=None):
    ret = HttpCore().post(buildup_url(method_path), params, files=files)
    return ret


def do_get(method_path, params):
    ret = HttpCore().get(buildup_url(method_path), params)
    return ret


def test_app_create():
    module = 'app'
    params = dict(
            method='create_app',
            title='蜜蜂聚财',
            description_url='http://www.baidu.com',
    )
    ret = do_post(module, buildup_arguments(params))
    print(ret)


# test_app_create()

# def test_upload_image(files):
def test_upload_image():
    files = [('recruit.jpg', ('recruit.jpg', open('recruit.jpg', mode='rb'), 'image/jpeg'))]
    module = 'image'
    params = dict(
            method='upload',
            path='/cars/2016/01/17/',
    )
    ret = do_post(module, buildup_arguments(params), files=files)
    print(ret)

def test_maintenace_notify():
    from collections import OrderedDict
    order_id = '56e263f043e74a0a4f1d445f'
    url = 'http://test.dashenglaile.com/autoResponse/'
    # params = {'service':'maintenance','partner':'7066715120801720','order_id':1,'status':1}
    # params_list = [k + '=' + str(value) for k,value in params.items()]
    # params = '&'.join(params_list)
    # print(params)

    params = 'service=maintenance&partner=7066715120801720&order_id='+order_id+'&status=1'
    a = requests.get(url+'?'+params)
    print(a.url)
    print(a.text)

if __name__ == '__main__':
    test_maintenace_notify()


