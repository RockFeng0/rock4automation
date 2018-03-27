# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.pc.uimfc.TestDriver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pc.uimfc.TestDriver,v 1.0 2017年3月7日
    FROM:   2017年3月7日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import subprocess,time
from autoitpy.autoit import WinMFCDriver

class TestDriver:
    def __init__(self):
        self.driver = WinMFCDriver()
    
    def find_driver(self):
        return self.driver
    
    def find_drivers(self):
        return {"loacalpcdriver":self.driver} 
    
    def run_model_case(self,callable_function):
        drivers = self.find_drivers()
        map(callable_function, drivers.items())            

def simple_usage1():
    subprocess.Popen([r"D:\auto\pc_install\npp.5.7.Installer.exe"])
    test = TestDriver()
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
    
    

if __name__ == "__main__":
    simple_usage1()
    