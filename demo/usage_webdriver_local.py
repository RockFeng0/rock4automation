# -*- encoding: utf-8 -*-
'''
Current module: demo.usage_webdriver_local

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.usage_webdriver_local,v 1.0 2017年5月19日
    FROM:   2017年5月19日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


from rock4 import WebTest
# local webdriver

'''
WebTest local parameter:
    browser:    firefox or chrome
    download_path:    set default download path of firefox or chrome
    marionette:       True / False, use firefox browser version 47.0.1 or greater if True 
'''                 
test = WebTest(browser = "chrome")
# find_driver 与 find_drivers  优先连接 Remote driver,连接不上再连接Local driver
# find_driver 返回第一个driver; find_drivers 返回dict; 返回的 driver 是 selenium 对象
driver = test.find_driver()
driver.get("http://www.baidu.com")
driver.quit()
