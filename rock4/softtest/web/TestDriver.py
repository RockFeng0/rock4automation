# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.web.TestDriver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.web.TestDriver,v 1.0 2017年2月18日
    FROM:   2017年2月18日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import time,sys,os
from rock4.softtest.support import utilities
from SeleniumJar import SeleniumHub,SeleniumNode
from SeleniumHatch import SeleniumHatch, RunPool, getRemoteHostSFormHub
from selenium import webdriver


class TestDriver:
    def __init__(self, hub_ip="localhost", hub_port=4444, **kwargs):
        ''' parameter kwargs keys:
                Default Remote:
                    browsers:      list of browser, only support (firefox, chrome). all of these: firefox chrome opera safari internetexplorer edge htmlunit htmlunitwithjs  
                    patch_with:    brwoser will be padding with, if not match the length of remote hosts              
                    marionette:    False / True, firefox driver will get started if True
                    download_path:    set default download path of firefox or chrome
                Webdriver:
                    browser:    firefox or chrome
                    download_path:    set default download path of firefox or chrome
                    marionette:       True / False, use firefox browser version 47.0.1 or greater if True 
                    
        '''
        self.hatch = None
        self.is_server_running = False        
        remote_hosts = getRemoteHostSFormHub(hub_ip, hub_port)
        if remote_hosts:
            self.__connect(remote_hosts = remote_hosts, **kwargs)            
        else:
            self.__loneliness(kwargs.get("browser","firefox"), download_path = kwargs.get("download_path"), marionette = kwargs.get("marionette", False))
                
            
    def find_caps(self):
        if self.hatch:
            return self.hatch.get_remote_caps()
    
    def find_exectors(self):
        if self.hatch:
            return self.hatch.get_remote_exectors()
        
    def find_driver(self, executor=None):
        if self.hatch:
            return self.hatch.get_remote_driver(executor)
        else:
            print "Waring: ignored the driver of executor[%s], use localwebdriver." %executor
            return self.driver

    def find_drivers(self):
        if self.hatch:
            return self.hatch.get_remote_drivers()
        else:
            return {"loacalwebdriver":self.driver}
    
    def run_model_case(self,callable_function):
        drivers = self.find_drivers()
        if self.is_local_server:
            map(callable_function, drivers.items())
        else:  
            RunPool.Start(callable_function, drivers)
                
    def __connect(self,remote_hosts, **kwargs):
        ''' For Remote Webdriver ''' 
        self.hatch = SeleniumHatch(remote_hosts, kwargs.get("browsers", []), kwargs.get("patch_with", "firefox"), marionette = kwargs.get("patch_with", False), download_path = kwargs.get("download_path"))
        self.is_server_running = True
        self.is_local_server = False
    
    def __loneliness(self, browser, download_path, marionette):
        ''' For Local Webdriver '''
        
        if browser == "firefox":
            fp=None
            if download_path and os.path.isdir(download_path):
                fp = webdriver.FirefoxProfile()     
                fp.set_preference("browser.download.folderList", 2)
                fp.set_preference("browser.download.manager.showWhenStarting", False)
                fp.set_preference("browser.download.dir", download_path)
                fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            
            if marionette == True:
                cap = None
            else:
                cap = {}
                
            self.driver = webdriver.Firefox(firefox_profile=fp, capabilities =cap)
                   
        elif browser == "chrome":
            options = webdriver.ChromeOptions()
            if download_path and os.path.isdir(download_path):
                prefs = {"download.default_directory": download_path}
                options.add_experimental_option("prefs", prefs)
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
            self.driver = webdriver.Chrome(chrome_options=options)
            
        self.is_server_running = True
        self.is_local_server = True
            
class SelRemote:
    def __init__(self):
        self.java_exe = utilities.get_java_path()
        if not self.java_exe:
            return
                
        self.jar = utilities.get_selenium_jar_path()
        if not self.jar:
            return
            
    def start_hub(self, port=4444, block = True):
        ''' usage:
            SelRemote().start_hub()
        '''       
        self.server = SeleniumHub(self.jar, port)
        try:   
            self.server.start_server()
            time.sleep(2)
            if block:
                self.__wait_quit("hub")
        except KeyboardInterrupt:
            pass
                   
    def start_node(self, port, hub_ip="localhost", hub_port = 4444, block = True):
        ''' # start hub is necessary before start node
        usage:
            SelRemote().start_node(5555)
        '''     
        self.server = SeleniumNode(self.jar, port, "http://%s:%s/grid/register" %(hub_ip, hub_port), self.java_exe)
        try:   
            self.server.start_server()
            time.sleep(2)   
            if block:
                self.__wait_quit("node")
        except KeyboardInterrupt:
            pass
    
    def stop(self):        
        if self.server:
            self.server.stop_server()
            self.server = None
        
    def __wait_quit(self, role):
        while True:
            cmd = raw_input("""
#################
            Commands[%s]:
                quit -- or CTRL + C to quit servers\n
#################
""" %role)
            if cmd == "quit":
                self.stop()
                sys.exit(0)
                break

def simple_example1():
    ### Local Webdriver
    
    # firefox
    test = TestDriver()
    drivers =  test.find_drivers()
    driver = test.find_driver()
    print driver
    print drivers    
    driver.get('http://www.baidu.com')
    time.sleep(2)
    driver.quit()
    
    # chrome profile
    test = TestDriver(browser = "chrome", download_path = r"d:\auto\buffer")
    driver = test.find_driver()    
    driver.get('http://www.baidu.com')
    time.sleep(2)
    driver.quit()   
    
    # firefox profile
    test = TestDriver(browser = "firefox", download_path = r"d:\auto\buffer", marionette = False)
    driver = test.find_driver()    
    driver.get('http://www.baidu.com')
    time.sleep(2)
    driver.quit()
    
def simple_example2():
    ### Remote Webdriver
    
    # PC1 -> start hub;  
    SelRemote().start_hub(block=False)
    
    # PC2 -> start node;  
    SelRemote().start_node(5555, hub_ip="127.0.0.1", hub_port=4444, block=False)
    
    # PC n -> start node    
    # PC n+1 -> start test    
    test = TestDriver(hub_ip="127.0.0.1", hub_port=4444, browsers = ["firefox","chrome"])
    print "caps-->",test.find_caps()
    print "exectors-->",test.find_exectors()
    drivers = test.find_drivers()
    print "drivers-->",drivers
    
    for exectors, driver in drivers.items():
        print "----Testing %s" %exectors
        driver.get('http://www.baidu.com')
        time.sleep(2)
        driver.quit()
    
    # clean java
    os.popen('taskkill /f /im  java.exe*').close()

if __name__ == "__main__":
    simple_example2()
