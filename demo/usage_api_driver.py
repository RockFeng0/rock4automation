# -*- encoding: utf-8 -*-
'''
Current module: demo.usage_api_driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.usage_api_driver,v 1.0 2017年5月19日
    FROM:   2017年5月19日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from rock4 import PacketTest
# Only local mode
# PacketTest.find_driver or find_drivers
# Return requests module for the test of web services
test = PacketTest()
driver = test.find_driver()
resp = driver.get("http://www.baidu.com")
print resp.status_code