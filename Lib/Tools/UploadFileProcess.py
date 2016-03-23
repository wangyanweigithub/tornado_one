# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import json
from datetime import datetime
from Lib.Tools.Http import HttpCore
from Lib.Tools.Codec import *
from Lib.TornadoExtend import AccessSource

class UploadFileProcess(object):
    base_url = 'http://image.sfdai.com/api/' 
    app_id = '7c6081a09ca44ba69747b11db5f8ee65'
    app_key = 'sdkfjiuyfssd6f77367826746734'

    @classmethod
    def buildup_url(cls, method_path):
        p = cls.base_url + method_path
        return p

    @classmethod
    def process_params(cls, params):
        params['app_id'] = cls.app_id
        str_b64 = base64_encode(json.dumps(params))
        return str_b64

    @classmethod
    def do_post(cls, method_path, params, files=None):
        ret = HttpCore().post(cls.buildup_url(method_path), params, files=files)
        return ret

    @classmethod
    def buildup_url(cls, method_path):
        p = cls.base_url + method_path
        return p

    @classmethod
    def buildup_arguments(cls, params):
        arguments = {}
        arguments['params'] = cls.process_params(params)
        arguments['lang'] = 'zh_CN'
        arguments['time'] = str(datetime.now().strftime('%Y%m%d%H%M%S%f'))
        arguments['source'] = AccessSource.ios_iphone
        arguments['sign'] = md5(md5(arguments['params'] + arguments['time']) + cls.app_key)
        return arguments

    @classmethod
    def test_upload_image(cls, file_name,path=None):
        files = [(file_name, (file_name, open(file_name, mode='rb'), 'image/jpeg'))]
        module = 'image'
        params = dict(
                method='upload',
                path='/cars/2016/02/17/',
        )
        ret = cls.do_post(module, cls.buildup_arguments(params), files=files)
        print(ret)


if __name__ == '__main__':

    # UploadFileProcess().test_upload_image('/Users/wangyanwei/Desktop/违章/芜湖王虎/行驶证2.jpg')
    UploadFileProcess().test_upload_image('行驶证2.jpg')
