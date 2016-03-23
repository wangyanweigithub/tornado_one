# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
import gene_tools
gene_tools.init_path()
import re
from Model.CarType import CarType
from Lib import Tools

info = '''<option value="01">大型汽车</option>
          <option selected="selected" value="02">小型汽车</option>
          <option value="03">使馆汽车</option>
          <option value="04">领馆汽车</option>
          <option value="05">境外汽车</option>
          <option value="06">外籍汽车</option>
          <option value="07">两、三轮摩托车</option>

          <option value="08">轻便摩托车</option>
          <option value="09">使馆摩托车</option>
          <option value="10">领馆摩托车</option>
          <option value="11">境外摩托车</option>
          <option value="12">外籍摩托车</option>
          <option value="13">低速车</option>

          <option value="14">拖拉机</option>
          <option value="15">挂车</option>
          <option value="16">教练汽车</option>
          <option value="17">教练摩托车</option>
          <option value="20">临时入境汽车</option>
          <option value="21">临时入境摩托车</option>

          <option value="22">临时行驶车</option>
          <option value="23">警用汽车</option>
          <option value="24">警用摩托</option>
          <option value="99">其它</option>'''

def run():
    CarType.drop_collection()
    ret = re.findall(r'value=\"(.*)\"\>(.*)\<',info)

    for item in ret:
        car_type = CarType()
        car_type.value = item[0]
        car_type.type = item[1]
        car_type.save()

if __name__ == '__main__':
    run()
