# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

from Controller.Api.AuthCode.AuthCodeProcess import AuthCodeProcess
from Controller.Api.Insurance.InsuranceProcess import InsuranceProcess
from Controller.Api.Maintenance.MaintenanceProcess import MaintenanceProcess
from Controller.Api.Member.MemberProcess import MemberProcess
from Controller.Api.Peccancy.PeccancyProcess import PeccancyProcess
from Controller.Api.PersonCenter.PersonCenter import PersonCenter

class ProcessFactory(object):
    ProcessClass = None

    def return_class(self,action):

        if action == 'member':
            self.ProcessClass = MemberProcess
        elif action == 'authcode':
            self.ProcessClass = AuthCodeProcess
        elif action == 'insurance':
            self.ProcessClass = InsuranceProcess
        elif action == 'maintenance':
            self.ProcessClass = MaintenanceProcess
        elif action == 'peccancy':
            self.ProcessClass = PeccancyProcess
        elif action == 'personcenter':
            self.ProcessClass = PersonCenter

        return self.ProcessClass

