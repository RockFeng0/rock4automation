# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.web.SeleniumHatch

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.web.SeleniumHatch,v 1.0 2017年2月27日
    FROM:   2017年2月27日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import urllib2,re
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from multiprocessing import Pool,freeze_support
from bs4 import BeautifulSoup as Beauty

def getRemoteHostSFormHub(hub_ip, port = 4444):
    ''' Get the data of all connected android device info and apk's capabilities.
        
    '''
    response = None
    url = "http://%s:%s/grid/console" %(hub_ip, port)
    try:
        response = urllib2.urlopen(url, timeout=5)

        if str(response.getcode()).startswith("2"):
            html = response.read()
            remote_nodes = Beauty(html,"html.parser").find_all(text = re.compile('remoteHost:.*'))            
            return [i.replace('remoteHost: ','') for i in remote_nodes]
        else:
            return ()
    except:
        return ()
    finally:
        if response:
            response.close()
            
class RunPool:
    @classmethod
    def Start(cls,callable_function,drivers):
        freeze_support()
        pool = Pool(len(drivers))
        # for i in executers:
            # result = pool.apply_async(runnCase, args=(params,));#异步
            # print result.get()
        pool.map(callable_function, drivers.items());#并行
        pool.close()
        pool.join()
        
class SeleniumHatch(object):
    ''' For Selenium Remote Driver or Selenium Grid '''
    def __init__(self, remote_hosts, browsers=[], patch_with= "firefox", marionette = False, download_path = None):
        '''
            remote_hosts:   remote hosts from selenium grid
            browsers:  firefox chrome opera safari internetexplorer edge htmlunit htmlunitwithjs  --will zip with self.__exectors  
            patch_with:    Which will be patch with if not match the length of self.__exectors             
        '''
        self.__exectors = [host + "/wd/hub" for host in remote_hosts]
        self.__set_browsers(browsers, patch_with, marionette, download_path)
                       
    def get_remote_caps(self):
        return self.__caps
    
    def get_remote_exectors(self):
        return self.__exectors
    
    def get_remote_driver(self,executor):
        self.__generate_remote_drivers(executor)
        return self.__drivers
    
    def get_remote_drivers(self):
        self.__generate_remote_drivers()
        return self.__drivers
    
    def __generate_remote_drivers(self, executor=None):
        ''' Generate remote drivers with desired capabilities(self.__caps)
        Only this divice_id's driver will be generated if specified the device_id.        
        '''
        executors = {}       
        drivers = {}
        
        if executor:
            if self.__caps.get(executor):
                executors[executor] = self.__caps.get(executor)
            else:
                print "---no",self.__caps
                return executors      
        else:
            executors = self.__caps
        
        for command_executor, cap in executors.items():
            try:
                driver = None
                firefox_profile = cap.pop("firefox_profile",None)
                # selenium requires browser's driver and PATH env. Firefox's driver is required for selenium3.0
                driver = webdriver.Remote(command_executor, desired_capabilities=cap, browser_profile = firefox_profile)
            except Exception,e:                
                print "--->Waring: %s %s %s" %(e, command_executor, cap)        
            
            if driver:
                drivers[command_executor] = driver
        self.__drivers = drivers
        
    def __set_browsers(self, browsers=[], patch_with= "firefox", marionette=False, download_path=None):
        '''
            browsers:  firefox chrome opera safari internetexplorer edge htmlunit htmlunitwithjs
        '''
        patch = len(self.__exectors) - len(browsers)
        if patch > 0:
            [browsers.append(patch_with) for i in range(patch)]
            
        
        
        caps = []
        for browser in browsers:
            browser = browser.upper()            
            cap = getattr(DesiredCapabilities, browser).copy() 
                    
            if browser == "FIREFOX":
                cap['marionette'] = marionette;# use firefox's driver if True                
                if download_path:
                    fp = webdriver.FirefoxProfile() 
                    fp.set_preference("browser.download.folderList", 2);# 设置Firefox的默认 下载 文件夹。0是桌面；1是“我的下载”；2是自定义
                    fp.set_preference("browser.download.manager.showWhenStarting", False)
                    fp.set_preference("browser.download.dir", download_path)
                    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
                    cap['firefox_profile'] = fp
                                          
            elif browser == "CHROME":
                options = webdriver.ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])                
                if download_path:
                    prefs = {"download.default_directory": download_path}
                    options.add_experimental_option("prefs", prefs)                    
                cap = options.to_capabilities()                
            caps.append(cap)
        
        self.__caps = dict(zip(self.__exectors, caps))   

### 用法
def demo_usage():    
    remote_hosts = getRemoteHostSFormHub("127.0.0.1")
    hatch = SeleniumHatch(remote_hosts, browsers = ['firefox', "chrome"], download_path = r'd:\auto\buffer')
    print hatch.get_remote_caps()
    drivers = hatch.get_remote_drivers()
    return drivers

### 示例  一
def simple_example_1():
    drivers = demo_usage()
    
    for exector, driver in drivers.items():
        print exector
        print "\t open www.baidu.com"
        driver.get('http://www.baidu.com')
        print "\t type selenium"
        driver.find_element_by_id("kw").send_keys('selenium')
        print "\t click 百度一下"
        driver.find_element_by_id("su").click()    
        driver.quit()    

### 示例  二
def case1(edriver):
    exector,driver = edriver[0],edriver[1]
    print "!!! %s" %exector
    print "\t open www.baidu.com"
    driver.get('http://www.baidu.com')
    print "\t type selenium"
    driver.find_element_by_id("kw").send_keys('selenium')
    print "\t click 百度一下"
    driver.find_element_by_id("su").click()    
    driver.quit()  

def simple_example_2():
    drivers = demo_usage()
    if drivers:
        RunPool.Start(case1, drivers)
    
    
### 示例  二
def case2(edriver):
    from rock4.common import p_env
    from actions import WebBrowser, WebElement     
    exector,p_env.BROWSER = edriver[0],edriver[1]    
    print "!!! %s" %exector
    
    print "\t open www.baidu.com"
    WebBrowser.NavigateTo("http://www.baidu.com")
    
    print "\t type selenium"
    (WebElement.by, WebElement.value, WebElement.index, WebElement.timeout) = ("id", "kw", 0, 10)
    WebElement.TypeIn('selenium')
    
    print "\t click 百度一下"
    (WebElement.by, WebElement.value, WebElement.index, WebElement.timeout) = ("id", "su", 0, 10)
    WebElement.Click()
    
    WebBrowser.WebClose()  

def simple_example_3():  
    drivers = demo_usage()
    if drivers:
        RunPool.Start(case2, drivers)
    
if __name__ == "__main__":
    simple_example_3()
    