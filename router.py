# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from Controller.Main import AdminController,ApiController
from Lib.TornadoExtend.BaseSyncHandler import BaseSyncHandler
from Controller.Main.DaShengNotifyController import DaShengNotifyController
urls = [
    (r'/api/(.*)',ApiController.ApiController),
    (r'/admin/(.*)',AdminController.AdminController),
    (r'/dasheng',DaShengNotifyController),
    ]