# -*- encoding: utf-8 -*-
'''
Current module: demo.simple_usage

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.simple_usage,v 1.0 2017年3月11日
    FROM:   2017年3月11日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from rock4 import shoot,target

######  WebTest
from rock4 import WebTest,Grid
# remote
def remote_test():
    grid = Grid()
    grid.start_hub(block = False)
    grid.start_node(5555, block=False)
    
    test = WebTest(browsers = ["chrome"])
    drivers = test.find_drivers()
    driver = drivers.items()[0][1]    
    driver.get("http://www.baidu.com")
    driver.quit()
    
    grid.stop()
    
# local
def local_test():
    test = WebTest(browser = "chrome")
    driver = test.find_driver()
    driver.get("http://www.baidu.com")
    driver.quit()
    
# shoot
def shoot_webtest():
    test = WebTest()
    drivers = test.find_drivers()
    devdriver = drivers.items()[0]
    
    target(proj_path = r'D:\auto\buffer\testProject')
    shoot(devdriver = devdriver,modelfile = r'D:\auto\buffer\testProject\testcase\web_excel_usage.xlsx',modeltype="web")
    
######  PcTest
from rock4 import PcMfcTest
from rock4 import PcWpfTest
import time,subprocess
# local
def mfc_test():
    subprocess.Popen([r"D:\auto\pc_install\npp.5.7.Installer.exe"])
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
    

# shoot
def shoot_pctest():
    test = PcMfcTest(r"D:\auto\pc_install\npp.5.7.Installer.exe")
    drivers = test.find_drivers()
    devdriver = drivers.items()[0]
    
    target(proj_path = r'D:\auto\buffer\testProject')
    shoot(devdriver = devdriver,modelfile = r'D:\auto\buffer\testProject\testcase\pc_mfc_excel_usage.xlsx',modeltype="pc")

##### PadTest
from rock4 import PadTest
# remote
def remote_pad_test():
    test = PadTest(r'D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk')
    driver = test.find_driver('127.0.0.1:6555')
    driver.find_elements('name',"NFC")[0].click()
    driver.quit()
    test.stop()

# shoot
def shoot_padtest():
    test = PadTest(r'D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk')    
    drivers = test.find_drivers()
    devdriver = drivers.items()[0]
    
    target(proj_path = r'D:\auto\buffer\testProject')
    shoot(devdriver = devdriver,modelfile = r'D:\auto\buffer\testProject\testcase\pad_excel_usage.xlsx',modeltype="pad")
    
##### PacketTest
from rock4 import PacketTest
# local
def local_packet_test():
    test = PacketTest()
    driver = test.find_driver()
    resp = driver.get("http://www.baidu.com")
    print resp.status_code
    
# shoot
def shoot_packet_test():
    test = PacketTest()    
    drivers = test.find_drivers()
    devdriver = drivers.items()[0]
    
    target(proj_path = r'D:\auto\buffer\testProject')
    shoot(devdriver = devdriver,modelfile = r'D:\auto\buffer\testProject\testcase\api_excel_usage.xlsx',modeltype="api")


if __name__ == "__main__":
    remote_test()
    