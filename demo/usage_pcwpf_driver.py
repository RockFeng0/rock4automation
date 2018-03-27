# -*- encoding: utf-8 -*-
'''
Current module: demo.usage_pcwpf_driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.usage_pcwpf_driver,v 1.0 2017年5月19日
    FROM:   2017年5月19日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from rock4 import PcWpfTest
import time
# PcWpfTest.find_driver or find_drivers
# Only remote mode which server is written by IronPython
# server: uiwpfdriver.exe  -->127.0.0.1:5820
# client: launch.exe   or   find_driver or find_drivers

test = PcWpfTest()
driver = test.find_driver()
# driver.send(action, *args, **kwargs)
#    parameter will construct to:    action(*args, **kwargs)
print driver.send("StartApplication",r'D:\auto\pc_install\npp.5.7.Installer.exe')
print "---"
driver.send("MouseDragTo", 400, 400, AutomationId = "TitleBar")
time.sleep(1)

print driver.send("MouseMove", 1056, 574)    
print driver.send("ClickablePoint",Name = "Cancel")
print "---"

print driver.send("ClickWin",Name = "OK")
print driver.send("SwitchToWindow","Notepad++ v5.7 安装")    
print driver.send("ClickWin",Name = u"下一步(N) >")
print driver.send("ClickWin",Name = u"我接受(I)")
print driver.send("TypeInWin", ur"d:\hello input", AutomationId = "1019")
print driver.send("ClickWin",Name = u"下一步(N) >")
print driver.send("ClickWin",Name = u"取消(C)")
print driver.send("SwitchToDefaultWindow")  
print driver.send("MouseClick",Name = u"是(Y)")
driver.stop()