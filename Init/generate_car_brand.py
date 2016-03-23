# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
import gene_tools
gene_tools.init_path()
from Lib.DaSheng.DaSheng import DaSheng

def generate_car_brand():
    obj = DaSheng()
    obj.get_car_brand()

if __name__ == '__main__':

    generate_car_brand()

