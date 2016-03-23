# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import tornado.web
from Model.MaintenaceResult import MaintenaceResult
from Lib.DaSheng.DaSheng import DaSheng

class DaShengNotifyController(tornado.web.RequestHandler):

    def process_argument(self,args):
        if isinstance(args,list):
            if len(args) == 1:
                return self.process_argument(args[0])
            ret = []
            for arg in args:
                ret.append(self.process_argument(arg))
        else:
            return args.decode()

    def base_get_arguments(self):
        result = {}
        for key,value in self.request.arguments.items():
            result[key] = self.process_argument(value)
        # print(result)
        return result

    def post(self):
        params = self.base_get_arguments()
        dasheng = DaSheng()
        print('params',params)
        notify_verify = dasheng.notify_verify(params['notify_id'])
        if notify_verify:
            verify_sign = dasheng.verify_sign(params)
            if verify_sign:
                print('verify_sign is success')
                maintenace = MaintenaceResult()
                try:
                    for k,v in params.items():
                        setattr(maintenace,k,v)
                except Exception as e:
                    print(e)
                maintenace.save()
                self.write('success')
            else:
                print('verify_sign is fail')