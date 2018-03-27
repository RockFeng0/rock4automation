# -*- encoding: utf-8 -*-
'''
Current module: demo.usage_pcmfc_driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.usage_pcmfc_driver,v 1.0 2017年5月19日
    FROM:   2017年5月19日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


from rock4 import PcMfcTest
import time,subprocess

subprocess.Popen([r"D:\auto\pc_install\npp.5.7.Installer.exe"])
# Only local mode
# PcMfcTest.find_driver or find_drivers
# Return autoit_py obj for the test of MFC UI
test = PcMfcTest()
driver = test.find_driver()
driver.invoke("Opt","WinTitleMatchMode",2)    
driver.invoke("WinActivate","Installer Language")    
driver.invoke("ControlClick","Installer Language","","OK")
time.sleep(0.5)
driver.invoke("ControlClick","Notepad++","",u"下一步(&N) >")
time.sleep(0.5)
driver.invoke("ControlClick","Notepad++","",u"我接受(&I)")
time.sleep(0.5)
driver.invoke("ControlClick","Notepad++","","[ID:1019;class:Button]")
driver.invoke("ControlSend","Notepad++","","[ID:1019;class:Button]","{END}+{HOME}")
time.sleep(1)
driver.invoke("ControlSend","Notepad++","","[ID:1019;class:Button]",ur"d:\hello input")
time.sleep(0.5)
driver.invoke("ControlClick","Notepad++","",u"下一步(&N) >")
driver.invoke("ControlClick","Notepad++","",u"取消(&C)")
time.sleep(0.5)
driver.invoke("ControlClick","Notepad++","","[ID:6]")
    