# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.drivers.uiappium.AppiumClient

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pad.uiappium.AppiumClient,v 2.0 2017年2月7日
    FROM:   2017年2月3日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import os,re
from appium import webdriver
from multiprocessing import Pool,freeze_support

def getAndroidDeviceDesiredInfo(apklocation=None, adb_exe_4path=None, aapt_exe_4path = None):
    ''' Get the data of all connected android device info and apk's capabilities.
        Before using the capability, 
        the 'None' values of 'deviceName' and 'platformVersion' in capabilities should be replace with the value of 'deviceId' and 'android_version'.
        Usage:
            desired =  getAndroidDeviceDesiredInfo(r'D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk')
            devices = desired.get("devices")
            cap = desired.get("capabilities")
            cap["deviceName"],cap["platformVersion"] = devices[0]["id"],devices[0]["android_version"]
            print cap
        :param apklocation: if None, Return pad info
        :param adb_exe_4path: if None, Path of OS Environment should be set for adb.exe
        :param aapt_exe_4path: if None, Path of OS Environment should be set for aapt.exe         
    '''
    devices = {}
    
    adb_exe = "adb.exe"
    if adb_exe_4path:
        adb_exe = adb_exe_4path
    
    aapt_exe = "aapt.exe"
    if aapt_exe_4path:
        aapt_exe = aapt_exe_4path
    
    # 读取设备 id
    os.popen(adb_exe +" start-server").close()
    device_ids = os.popen(adb_exe + " devices").readlines()[1:-1]
    if not device_ids:
        print "No device is connected."
        return devices
    
    #### desired capabilities
    if apklocation:
        appPackageAdb1 = list(os.popen(r'%s dump badging %s | find "package:"' %(aapt_exe, apklocation)).readlines())
        if not appPackageAdb1:
            print "Invalid: aapt.exe dump badging %s" %apklocation
            return devices
        appPackage = re.findall(r'\'(\w*.*?)\'', appPackageAdb1[0])[0].strip()
        
        appPackageAdb2 = list(os.popen(r'%s dump badging %s | find "launchable-activity:"' %(aapt_exe, apklocation)).readlines())
        if not appPackageAdb2:
            print "Invalid: aapt.exe dump badging %s" %apklocation
            return devices
        appActivity = re.findall(r'\'(\w*.*?)\'', appPackageAdb2[0])[0]
        
        devices["capabilities"] = {
            'platformName': 'Android',
            'deviceName': None,
            'platformVersion': None,
            'app': apklocation,
            'appPackage': appPackage,
            'appWaitPackage': appPackage,
            'appActivity': appActivity,
        }
    
    #### pad info
    devices["devices"]=[]
    for i in device_ids:
        deviceId,deviceStatus = i.split()        
        if deviceStatus != "device":
            print "Waring: %s" %i
            continue
            
        pad_ip = os.popen('%s -s %s shell getprop dhcp.wlan0.ipaddress' %(adb_exe, deviceId)).read().strip()
        pad_type = os.popen('%s -s %s shell getprop ro.product.model' %(adb_exe, deviceId)).read().strip()
        pad_version = os.popen('%s -s %s shell getprop ro.build.display.id' %(adb_exe, deviceId)).read().strip()
        pad_cpu = os.popen('%s -s %s shell getprop ro.product.cpu.abi' %(adb_exe, deviceId)).read().strip()
        android_version = os.popen('%s -s %s shell getprop ro.build.version.release' %(adb_exe, deviceId)).read().strip()
        linux_version = os.popen('%s -s %s shell cat /proc/version' %(adb_exe, deviceId)).read().strip()
        devices["devices"].append({
            'id':deviceId,
            'ip':pad_ip,
            'model':pad_type,
            'cpu':pad_cpu,
            'pad_version':pad_version,            
            'android_version':android_version,
            'linux_version':linux_version,
            })
    return devices

class RunPool:
    @classmethod
    def Start(cls,callable_function,drivers):
        #freeze_support()
        pool = Pool(len(drivers))
        # for i in executers:
            # result = pool.apply_async(runnCase, args=(params,));#异步
            # print result.get()
        pool.map(callable_function, drivers.items());#并行
        pool.close()
        pool.join()
        
class AppiumClient:
    
    def __init__(self):
        self.__caps = {}
        self.__devs = {}
            
    def set_desired_capabilities(self,desired, port = 4725):
        '''
        Paramerter:
            desired    --> the value is form getAndroidDeviceDesiredInfo()
            port       --> the same value with AppiumServer's port
        Usage:
            desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
            a=AppiumClient()
            a.set_desired_capabilities(desired)
            print a.get_desired_capabilities()
            print a.get_desired_devices()
        '''
        devices = desired.get("devices")
        cap = desired.get("capabilities")
        caps = {}
        devs = {}
        for device in devices:
            device_id = device.pop('id',None)
            if device_id:
                devs[device_id] = device
                
                actual_cap = cap.copy()                
                actual_cap["deviceName"],actual_cap["platformVersion"] = device.get('id'),device.get('android_version')
                actual_cap["tmp_executer"] = "http://localhost:%d/wd/hub" %port
                caps[device_id] = actual_cap
                port += 1
        self.__caps = caps 
        self.__devs = devs       
    
    def get_desired_capabilities(self):
        return self.__caps
    
    def get_desired_devices(self):
        return self.__devs
        
    def get_remote_driver(self,device_id):
        ''' Usage:
            desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
            a=AppiumClient()
            a.set_desired_capabilities(desired)
            print a.get_remote_driver("127.0.0.1:6555")
        '''
        self.__generate_remote_drivers(device_id)
        return self.__drivers.get(device_id)
    
    def get_remote_drivers(self):
        ''' Usage:
            desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
            a=AppiumClient()
            a.set_desired_capabilities(desired)
            print a.get_remote_drivers()
        '''
        self.__generate_remote_drivers()
        return self.__drivers
    
    def __generate_remote_drivers(self, device_id=None):
        ''' Generate remote drivers with desired capabilities(self.__caps)
        Only this divice_id's driver will be generated if specified the device_id.        
        '''
        drivers = {}
        caps = self.__caps
        
        if device_id:
            cap = self.__caps.get(device_id)
            if not cap:
                self.__drivers = drivers
                return
            else:
                caps = {device_id:cap}            
            
        for devid,cap in caps.items():
            command_executor=cap.pop("tmp_executer",None)
            try:
                driver = None
                driver = webdriver.Remote(command_executor,cap)
            except Exception,e:                
                print "--->Waring: %s[%s] %s" %(self.__devs[devid]["model"], devid, e)        
            
            if driver:
                drivers[devid] = driver
        self.__drivers = drivers

### 示例  一
def simple_example_1():
    import time
    desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
    client = AppiumClient()
    client.set_desired_capabilities(desired)    
    driver = client.get_remote_driver("127.0.0.1:6555")
    
    time.sleep(5)
    driver.find_elements('name',"NFC")[0].click()
    time.sleep(5)
    driver.quit()

### 示例 二
def case(driver_raw):
    import time
    devid,driver = driver_raw[0],driver_raw[1]
    print "!!! %s" %devid
    time.sleep(5)
    driver.find_elements('name',"NFC")[0].click()
    time.sleep(5)
    driver.quit()
        
def simple_example_2():
    desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
    client = AppiumClient()
    client.set_desired_capabilities(desired)    
    drivers = client.get_remote_drivers()
    RunPool.Start(case,drivers)   
    
### 示例 三
def case2(driver_raw):
    import time
    from rock4.common import p_env
    from actions import MobileApp,MobileElement as App 
    devid,p_env.MOBILE = driver_raw[0],driver_raw[1]
    print "!!! %s-%s" %(devid,p_env.MOBILE)
    
    (App.by,App.value) = ("ID","android:id/text1")
    App.ScrollDown()
    time.sleep(5)
    (App.by,App.value) = ("NAME","Views")
    App.Click()
    time.sleep(5)
    (App.by,App.value) = ("NAME","Controls")
    App.Click()
    time.sleep(5)
    MobileApp.QuitApp()
        
def simple_example_3():    
    desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
    client = AppiumClient()
    client.set_desired_capabilities(desired)    
    drivers = client.get_remote_drivers()
    RunPool.Start(case2,drivers)
      
if __name__ == "__main__":    
#     desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
#     a=AppiumClient()
#     a.set_desired_capabilities(desired)
#     print a.get_desired_capabilities()
#     print a.get_desired_devices()

#     desired = getAndroidDeviceDesiredInfo()
#     print desired
    simple_example_1()
