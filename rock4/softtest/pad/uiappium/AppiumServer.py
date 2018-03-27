# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.drivers.uiappium.AppiumServer

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pad.uiappium.AppiumServer,v 2.0 2017年2月7日
    FROM:   2017年1月25日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import os,threading,urllib2
from multiprocessing import Process,freeze_support

def getAndroidDevicesId(adb_exe_4path=None):
    ''' Ids form command: adb devices
        print getAndroidDevicesId()
        
    '''
    devices = []
    adb_exe = "adb.exe"
    if adb_exe_4path:
        adb_exe = adb_exe_4path
        
    # 读取设备 id
    os.popen(adb_exe + " start-server").close()
    device_ids = os.popen(adb_exe + " devices").readlines()[1:-1]
    if not device_ids:
        print "No device is connected."
        return devices
        
    for i in device_ids:        
        deviceId,deviceStatus = i.split()
        if deviceStatus == "device":
            devices.append(deviceId)
        else:
            print "Waring: %s" %i
    return devices

class RunServer(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
    def run(self):
        os.system(self.cmd)
        
class AppiumServer:
    ''' Usage:
        names = getAndroidDevicesId()
        if names:       
            servers = AppiumServer(names,r'E:\android-sdk\Appium')
            servers.start_server()
            time.sleep(5)
            servers.re_start_server()
            time.sleep(5)
            servers.stop_server()
    '''
    def __init__(self, devices_id, appium_root_path, timeout = 120000, port = 4725, loglevel = "info:info"):  
        node = os.path.join(appium_root_path,"node.exe")                
        
        native_js = os.path.join(appium_root_path,r"node_modules/appium/bin/appium.js")
        rock4_js = os.path.join(appium_root_path,r"bin/appium.js")
        if os.path.isfile(native_js):
            js = native_js
        
        if os.path.isfile(rock4_js):
            js = rock4_js

        self.commands = []
        self.ports = []
        for dev in devices_id:
            self.commands.append('%s %s --command-timeout %d -p %d -U %s --log-level %s' %(node,js,int(timeout),int(port),dev,loglevel)) 
            self.ports.append(port)
            port += 1  
            
        #node D:\app\Appium\node_modules\appium\bin\appium.js  -p 4723 -bp 4733
        #node.exe E:\android-sdk\Appium\node_modules\appium\lib\server\main.js --command-timeout 120000 -p 4723 -U device_id_1
                
    def start_server(self):
        """start the appium server.
        Doc note: Functionality within multiprocessing requires that the __main__ module be importable by the children.
        -简单说，就是要在  if __name__ == "__main__"中 调用该方法
        """        
        for cmd in self.commands:
            t1 = RunServer(cmd)
            freeze_support()            
            p = Process(target=t1.start())
            p.start()
        
    def stop_server(self):
        """stop the appium server
        selenium_appium: appium selenium
        :return:
        """
        os.popen('taskkill /f /im  node.exe*').close()
                                
    def re_start_server(self):
        """reStart the appium server
        """
        self.stop_server()
        self.start_server()
    
    def is_runnnig(self):
        """Determine whether server is running
        :return:True or False
        """
        response = None
        for port in self.ports:
            url = "http://127.0.0.1:"+str(port)+"/wd/hub"+"/status"
            try:
                response = urllib2.urlopen(url, timeout=5)

                if str(response.getcode()).startswith("2"):
                    return True
                else:
                    return False
            except:
                return False
            finally:
                if response:
                    response.close()

if __name__ ==  "__main__":
    names = getAndroidDevicesId()
    import time
    if names:
        servers = AppiumServer(names,r'E:\android-sdk\Appium')
        servers.start_server()
        time.sleep(3)
        print servers.is_runnnig()
