# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

class HeaderType(object):

    base = 100
    query = 200
    get_code_header = 300
    check_code_header = 400
    get_result_header = 500

class HeaderFactory(object):

    base_header = '''Host: www.weizhangwang.com
                    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
                    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36
                    Accept-Encoding: gzip, deflate, sdch
                    Accept-Language: zh-CN,zh;q=0.8,en;q=0.6'''

    query_header = '''Host: www3.weizhangwang.com
                    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0
                    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
                    Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
                    Accept-Encoding: gzip, deflate
                    Referer: http://www.weizhangwang.com/
                    Connection: keep-alive
                    Content-Type: application/x-www-form-urlencoded'''

    get_code_header = '''Host: www3.weizhangwang.com
                        User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0
                        Accept: image/png,image/*;q=0.8,*/*;q=0.5
                        Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
                        Accept-Encoding: gzip, deflate
                        Referer: http://www3.weizhangwang.com/get_all_hj.php'''

    check_code_header = '''Host: www3.weizhangwang.com
                        User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0
                        Accept: */*
                        Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
                        Accept-Encoding: gzip, deflate
                        Content-Type: application/x-www-form-urlencoded; charset=UTF-8
                        X-Requested-With: XMLHttpRequest
                        Referer: http://www3.weizhangwang.com/get_all_hj.php
                        Connection: keep-alive'''

    get_result_header = '''Host: www3.weizhangwang.com
                        User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0
                        Accept: text/html, */*; q=0.01
                        Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
                        Accept-Encoding: gzip, deflate
                        X-Requested-With: XMLHttpRequest
                        Referer: http://www3.weizhangwang.com/get_all_hj.php
                        Connection: keep-alive'''

    @classmethod
    def build_str_to_header(cls,header):

        dic = [x.strip() for x in header.split('\n')]
        _list = []
        for x in dic:
            _list.append(x.split(':',1))
        # print(_list)
        header = dict(_list)
        return header

    @classmethod
    def return_header(cls,header_type):

        if header_type == HeaderType.base:
            header = cls.base_header
        if header_type == HeaderType.query:
            header = cls.query_header
        if header_type == HeaderType.get_code_header:
            header = cls.get_code_header
        if header_type == HeaderType.check_code_header:
            header = cls.check_code_header
        if header_type == HeaderType.get_result_header:
            header = cls.get_result_header

        return cls.build_str_to_header(header)


