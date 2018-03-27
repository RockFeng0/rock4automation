# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.pad.uiappium.TestDriver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pad.uiappium.TestDriver,v 1.0 2017年2月8日
    FROM:   2017年2月8日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import time
from rock4.softtest.support import utilities
from AppiumServer import AppiumServer,getAndroidDevicesId
from AppiumClient import AppiumClient,getAndroidDeviceDesiredInfo,RunPool

class TestDriver:
    def __init__(self, apklocation):
        self.server, self.client = None, None
        self.__apklocation = apklocation
        self.__appium_server_root = utilities.get_appium_root_path()
        self.__adb_exe_4path = utilities.get_adb_path()
        self.__aapt_exe_4path = utilities.get_aapt_path()
                
        if not self.__appium_server_root:
            raise Exception("Not found appiumroot at softtest/support.")
        
        if not self.__adb_exe_4path:
            raise Exception("Not found android at softtest/support.")
        
        deviceidlist = getAndroidDevicesId(self.__adb_exe_4path)
        self.is_server_running = False
        if deviceidlist:
            self.server = AppiumServer(deviceidlist, self.__appium_server_root)        
            self.server.start_server()
            self.is_server_running = True
            time.sleep(2)  
    
    def find_driver(self, deviceid):
        self.__connect()
        if self.client:    
            return self.client.get_remote_driver(deviceid)

    def find_drivers(self):
        self.__connect()
        if self.client: 
            return self.client.get_remote_drivers()
    
    def find_device(self, deviceid):
        self.__connect()
        if self.client: 
            return self.client.get_desired_devices().get(deviceid)
        
    def find_devices(self):
        self.__connect()
        if self.client: 
            return self.client.get_remote_drivers()
    
    def run_model_case(self,callable_function):
        drivers = self.find_drivers()
        RunPool.Start(callable_function, drivers)
        self.stop()
        
    def __connect(self):
        device_desired = getAndroidDeviceDesiredInfo(self.__apklocation,self.__adb_exe_4path, self.__aapt_exe_4path)
        if not device_desired:
            return
        
        if not self.client:
            self.client = AppiumClient()
            self.client.set_desired_capabilities(device_desired)
    
    def stop(self):        
        if self.server:
            self.server.stop_server()
        self.server, self.client = None, None

    
def usage_TestDriver_sample1():
    test = TestDriver(r'D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk')
    driver = test.find_driver('127.0.0.1:6555')
    driver.find_elements('name',"NFC")[0].click()
    driver.quit()
    test.stop()

def usage_TestDriver_sample2():
    from rock4.common import p_env
    from actions import MobileApp,MobileElement as App
  
    test = TestDriver(r'D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk')
    driver = test.find_driver('127.0.0.1:6555')
    driver.find_elements('name',"NFC")[0].click()
        
    p_env.MOBILE = driver    
    MobileApp.Back()
    
    (App.by,App.value) = ("ID","android:id/text1")
    App.ScrollDown()
    
    (App.by,App.value) = ("NAME","Views")
    App.Click()
    
    (App.by,App.value) = ("NAME","Controls")
    App.Click()    
    
    MobileApp.CloseApp()
    test.stop()

if __name__ == "__main__":
    usage_TestDriver_sample2()
    