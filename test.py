# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'


from datetime import datetime
import xmltodict
from Lib.DaSheng.DaSheng import DaSheng
from Lib.DaSheng.DaShengBase import DaShengBase
from Lib.Tools.UploadFileProcess import UploadFileProcess
from Controller.Main.BaseProcess import BaseProcess

def test_upload():
    up = UploadFileProcess()
    file_name = '/Users/wangyanwei/Desktop/5.jpg'
    files = [(file_name, (file_name, open(file_name, mode='rb'), 'image/jpeg'))]
    module = 'image'
    params = dict(
            method='upload',
            path='/cars/'+ datetime.now().strftime('%Y/%m/%d')
    )
    ret = up.do_post(module, up.buildup_arguments(params), files=files)
    print(ret)

def test_car_brand():
    da = DaSheng()
    # ret = da.get_car_brand()
    ret1 = da.get_policy_company_list()

def test_mantainence_query():
    da = DaSheng()
    # ret = da.get_car_brand()
    # ret1 = da.get_policy_company_list()
    params = dict(
            car_brand_id = 17,
            # image_type = 'url',
            # image = 'http://image.sfdai.com/assets/7c6081a09ca44ba69747b11db5f8ee65/cars/2016/01/2786bc6e41501fb395622a3086265db5d3.jpg',
            image_type = 'vin',
            image = 'LSVFB66R1B2113635',
            order_id = 1000000,
    )
    ret = da.mantainence_query(**params)
    print(ret)

def test_insurance_query():
    da = DaSheng()
    params = dict(
            company_id = 14,
            order_id = 'sdfljldas12312',
            policy_no = 123123123,
            identify_no = 'slfjsdf',
            verify_code = ''
    )
    ret = da.insurance_query(**params)
    print(ret)

def test_weizhang():
    id = '56cd1ae7e0839202a31c8bf7'
    file = '''<xml><querystatus>3</querystatus><hphm>浙B598B0</hphm><weizhang><item><id>1383334</id><province>ZJ</province><city>ZJ_NB</city><hphm>浙B598B0</hphm><date>2015-11-28 14:31:00</date><area>翠柏路与西湾路南口</area><act>遇前方机动车停车排队或者缓慢行驶时,借道超车或者占用对面车道、穿插等候车辆的</act><code></code><fen>2</fen><money>100</money><handled>0</handled><queryid>22316174615972420</queryid></item><item><id>1383335</id><province>ZJ</province><city>ZJ_NB</city><hphm>浙B598B0</hphm><date>2015-09-19 00:43:00</date><area>江南公路北仑段1Km＋750m</area><act>驾驶中型以上载客载货汽车、危险物品运输车辆以外的其他机动车行驶超过规定时速10%未达20%的</act><code></code><fen>3</fen><money>200</money><handled>0</handled><queryid>22316174615972420</queryid></item><item><id>1383336</id><province>ZJ</province><city>ZJ_NB</city><hphm>浙B598B0</hphm><date>2015-05-04 09:25:00</date><area>杨木碶路（229号旁）</area><act>不按规定停放影响其他车辆和行人通行的</act><code></code><fen>0</fen><money>150</money><handled>0</handled><queryid>22316174615972420</queryid></item></weizhang></xml>'''
    ret = xmltodict.parse(file)
    BaseProcess().save_peccancy(ret,id)

if __name__ == '__main__':
    test_weizhang()

