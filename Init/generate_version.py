# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
import gene_tools
gene_tools.init_path()
from datetime import datetime
from Model.Version import Version

def generate_versioin():

    new_version = Version()
    new_version.version = '0.0.1'
    new_version.date = datetime.now()
    new_version.remark = '测试版本'
    new_version.status = 1
    new_version.url = 'http://www.baidu.com'
    new_version.save()

if __name__ == '__main__':
    generate_versioin()
