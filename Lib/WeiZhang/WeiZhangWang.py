# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import re
import os
import requests
import setting
from Lib.WeiZhang.Head import HeaderFactory,HeaderType
from Lib.WeiZhang.WeiZhangBase import WeiZhangBase
from Model.WeiZhangWangCityInfo import WeiZhangWangCityInfo

class WeiZhangWang(WeiZhangBase):

    base_url = 'http://www.weizhangwang.com'
    post_form_url = 'http://www3.weizhangwang.com/get_all_hj.php'
    get_check_code_url = 'http://www3.weizhangwang.com/mysource/validatecode/code_gg.php'
    post_check_code_url = ''
    get_result_url = 'http://www3.weizhangwang.com/querywzxml.php'
    base_img = 'http://www3.weizhangwang.com'
    message = ''

    def build_params(self,**kwargs):

        # item = WeiZhangWangCityInfo.objects(c_name=kwargs['city'],p_name=kwargs['province']).first()
        item = WeiZhangWangCityInfo.objects(c_short_name=kwargs['license_plate'][1],p_short_name=kwargs['license_plate'][0]).first()

        areacode = '%04d' % item.c_pcode
        city_sn = kwargs['license_plate'][1]
        cphm = kwargs['license_plate'][-5:]
        vin = kwargs['vin'][-6:]
        enginenumber = kwargs.get('enginenumber','')  #!!!!!!!!!!!!!
        hpzl = kwargs.get('car_type_value','01') #!!!!!!!!1!!!!!
        car_type = self.get_car_type_from_value(hpzl)

        if car_type is None:
            self.message = '没有这个汽车类型'

        hpzl_text = car_type.type
        if item is None:
            self.message = '违章查询数据库信息没有这个城市信息'
        params = dict(province=item.p_name,province_sn=item.p_short_name,c_id=item.c_id,cphm=cphm,hpzl=hpzl,enginenumber=enginenumber,
                      classnumber=vin,areacode=areacode,city_id=item.id_csy,province_id=item.province_id_csy,
                      pid=item.province_id_csy,jhcc=item.jh_city_code,id360=item.id_360,sourceline='',city_sn=city_sn,hpzl_text=hpzl_text)
        # province	浙江
        # province_sn	浙
        # city_sn	B
        # c_id	87
        # cphm	Z589X
        # hpzl	02  汽车类型
        # classnumber	106027
        # enginenumber
        # areacode	0571
        # city_id	109
        # province_id	9
            # pid	9
        # jhcc	ZJ_HZ
        # id360	87
        # sourceline
        # hpzl_text	小型汽车

        params.update(kwargs)

        _params_list = ['province','province_sn','city_sn','c_id','cphm','hpzl','classnumber',
                        'enginenumber','areacode','city_id','province_id','pid','jhcc','id360',
                        'sourceline','hpzl_text']

        _params = {}
        for i in params:
            if i in _params_list:
                _params[i] = params[i]

        # print(_params)
        return _params

    #获取网页返回数据中的k值，需要在后面使用。
    def get_k_value(self,text):
        value = re.findall("var kk='(.*)';",text)
        print('k value is ',value)
        if value:
            return value[0]
        else:
            return None

    #得到验证码图片并打开它
    def get_verify_code(self,ret):

        if 'input type="text" class="input" id="code_gg"' in ret.text:
            relative_pathname = re.findall(r'\<img src=\"(.*)\" id="getcode_gg" title="看不清，点击换一张" align="absmiddle"\>', ret.text)
            img_url = self.base_img + relative_pathname[0]

            header = HeaderFactory.return_header(HeaderType.get_code_header)
            code_ret = requests.get(img_url,stream=True,cookies=ret.cookies,headers=header)

            file_name = os.path.join(setting.project_path, "Web/Assets/VerifyCodeImg/VerifyCode.jpg")
            file = open(file_name,'wb')
            file.write(code_ret.content)
            # os.system('open '+file_name)
            return code_ret

    #得到post_check_code_url 的网址
    def check_verify_code(self,text):
        url = re.findall(r'post\(\"(.*)\",.code:code_gg',text)
        # print(url[0])
        return url[0]


    def run(self,params):

        header = HeaderFactory.return_header(HeaderType.base)
        params = self.build_params(**params)
        first_ret = self.http_get(self.base_url,headers=header)
        query_header = HeaderFactory.return_header(HeaderType.query)
        second_ret = self.http_post(self.post_form_url,params=params,headers=query_header,cookies=first_ret.cookies)

        k = self.get_k_value(second_ret.text)
        ret_result_cookie = second_ret.cookies
        print('k is ',k)
        if not k:
            ret = self.get_verify_code(second_ret)
            post_verify_code_cookie = ret.cookies
            print(dict(post_verify_code_cookie))
            # code = input()         #输入验证码，人工输入
            # params = dict(code=code)
            post_verify_code_url = self.check_verify_code(second_ret.text)
            ret = dict(img_url=setting.verifycode_img,post_verify_code_cookie=dict(post_verify_code_cookie),post_verify_code_url=post_verify_code_url)
            return ret

        return self.get_result(k,ret_result_cookie)

    def get_result(self,k,ret_result_cookie):
        if not k:
            return dict(message='验证码错误')
        url = self.get_result_url + "?k=" + k
        get_result_header = HeaderFactory.return_header(HeaderType.get_result_header)
        result_ret = self.http_get(url,headers=get_result_header,cookies=ret_result_cookie)
        print(result_ret.text)
        result = self.parse_xml(result_ret.text)
        return (result,self.message)

    def verify_code_get_result(self,post_verify_code_url,code,post_verify_code_cookie):
        params = dict(code=code)
        post_verify_code_header = HeaderFactory.return_header(HeaderType.check_code_header)
        ret = self.http_post(url=self.base_img+post_verify_code_url,headers=post_verify_code_header,params=params,cookies=post_verify_code_cookie)
        k = ret.text
        ret_result_cookie = ret.cookies
        # return (k,ret_result_cookie)
        return self.get_result(k,ret_result_cookie)
