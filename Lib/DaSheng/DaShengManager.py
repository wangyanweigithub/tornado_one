# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
from Lib.DaSheng.DaSheng import DaSheng

class DaShengInsurance(DaSheng):

    def query_insurance(self,order):

        return self.insurance_query(order.company_id,order.id,order.policy_no,order.identify_no)



class DaShengMaintenance(DaSheng):
    def query_mantainence(self,order):

        return self.mantainence_query(order.brand_id,order.image_type,order.id_image_url,order.id,order.engine_number)

def test():
    from Model.OrderForMaintenance import OrderForMaintenance
    order = OrderForMaintenance.objects().first()
    da = DaShengMaintenance(order)
    da.query_mantainence()

if __name__ == '__main__':
    test()