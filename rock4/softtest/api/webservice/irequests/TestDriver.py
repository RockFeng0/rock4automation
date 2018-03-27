# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.api.webservice.irequests.TestDriver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.api.webservice.irequests.TestDriver,v 1.0 2017年3月8日
    FROM:   2017年3月8日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import requests

class TestDriver:    
    
    def find_driver(self):
        return requests
        
    def find_drivers(self):
        return {"loacalapidriver": requests} 
    
    def run_model_case(self,callable_function):
        drivers = self.find_drivers()
        map(callable_function, drivers.items())            

def simple_usage1():
    test = TestDriver()
    driver = test.find_driver()
    resp = driver.get("http://www.baidu.com")
    print resp.status_code
    
if __name__ == "__main__":
    simple_usage1()