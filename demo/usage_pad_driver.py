# -*- encoding: utf-8 -*-
'''
Current module: demo.usage_pad_driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.usage_pad_driver,v 1.0 2017年5月19日
    FROM:   2017年5月19日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from rock4 import PadTest
# Only remote mode
# PadTest.find_driver or find_drivers
# Return appium obj for the test of Mobile UI
test = PadTest(r'D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk')
driver = test.find_driver('127.0.0.1:6555')
driver.find_elements('name',"NFC")[0].click()
driver.quit()
test.stop()