# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import tornado
from tornado.options import define,options
from setting import *
from router import urls


define('address',default=server_host,type=str,help='please input server ip')
define('port',default=11811,type=int,help='run on the given port')

application = tornado.web.Application(urls,**env)

if __name__ == '__main__':

    options.parse_command_line()
    application.listen(options.port,xheaders=True)
    print('server running at:http://%s:%s' % (server_host,options.port))
    tornado.ioloop.IOLoop.instance().start()
