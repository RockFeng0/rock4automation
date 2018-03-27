# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.drivers.uiselendroid.driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pad.uiselendroid.driver,v 2.0 2017年2月7日
    FROM:   2016年5月11日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import os,subprocess
from selenium import webdriver

from rock4.softtest.web.driver import WebBrowser
from rock4.softtest.web.driver import WebElement
from rock4.common import p_env, p_common

class MobileApp(WebBrowser):
    ''' Mobile App Test.(need selendroid API<17)'''
    
    @classmethod
    def Init(cls, executor, desired_capabilities=None,browser_profile=None, proxy=None, keep_alive=False, server_path=None, apk_path=None,):
        '''
        # Selendroid need parameters:
            executor                = "selendorid"            
            desired_capabilities    = {"aut":"com.tianwen.aischool:V006R001C01B10SP02B04"}
            server_path             = r"D:\auto\python\app-autoApp\demoProject\tools\selendroid-standalone.jar"
            apk_path                = r"D:\auto\python\app-autoApp\demoProject\resource\V006R001C01B10SP02B04.apk"
        
        # Appium need parameters:
            executor                = "appium"            
            desired_capabilities    = {"platformName":"Android","platformVersion":'4.4.2',"deviceName":"device",
                                        "app":r'D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk'
                                        }
            server_path             = r'E:\android-sdk\Appium'
            #### desired_capabilities中，选择定义[app 或者 appPackage + appActivity],app指定apk，如果已经安装app，可以使用后者定义
            #desired_capabilities['appPackage'] = 'io.appium.android.apis'
            #desired_capabilities['appActivity'] = '.ApiDemos'
            
            
        '''
        executors= {"selendroid":{
                                  "executor":'http://localhost:4444/wd/hub',
                                  "API_limited":False
                                  },
                    "appium":{
                              "executor":'http://localhost:4723/wd/hub',
                              "API_limited":True,
                              "API_require":">= 17"
                            }
                    }
        
        if not executor in executors:
            raise Exception("Executor['%s'] was not supported.Selections:\n%s" %executors)
        
        #### Start Server
        with open("%s.log" %executor, 'w') as f:
            if executor == "selendroid":    
                # 设置2分钟命令超时，断开连接            
                selendroid_cmd = [p_env.JAVA_EXE,"-jar",server_path,"-app",apk_path,"-sessionTimeout","120000"]
                cls.__sub_process = subprocess.Popen(selendroid_cmd, stdout = f , stderr = f)
                
                p_common.wait_for_connection(port = 4444)
                
            if executor == "appium":
                #设置2分钟命令超时，断开连接
                node_path = os.path.join(server_path,"node.exe")
                main_js_path = os.path.join(server_path,r"node_modules\appium\lib\server\main.js")
                
                appium_cmd = [node_path, main_js_path, "--command-timeout", "120000"]
                cls.__sub_process = subprocess.Popen(appium_cmd, stdout = f, stderr = f)
                
                p_common.wait_for_connection(port=4723)
            print cls.__sub_process.pid
        server = executors.get(executor)
        #### Connect Server
        try:            
            executor = server["executor"]
            p_env.MOBILE = webdriver.Remote(executor, desired_capabilities, browser_profile, proxy, keep_alive)
            p_env.BROWSER = p_env.MOBILE
        except Exception,e:
            raise Exception("%s\nNo connection has been created.Please check you server and device." %e)
    
    @classmethod
    def AppClose(cls):        
        try:
            getattr(p_env.MOBILE,"quit")()            
        except:
            pass
        finally:
            cls.__sub_process.kill()
        

class MobileElement(WebElement):
    ''' Mobile App Element Test.(need selendroid API<17)'''
    (by, value) = (None, None)
    (index,timeout) = (0,10)
    
    @classmethod
    def Click(cls):
        # The parent Click is currently not yet supported by selendroid
        # So overwrite Click 
        element = cls.Wait()
        element.click()    
    
    
def usage_for_selendroid():
    # aischool
    server_jar_path = r"D:\auto\python\app-autoApp\demoProject\tools\selendroid-standalone.jar"
    test_apk = r"D:\auto\python\app-autoApp\demoProject\resource\V006R001C01B10SP02B04.apk"
    caps={}
    caps['aut']= "com.tianwen.aischool:V006R001C01B10SP02B04"
    
    
    try:
        MobileApp.Init("selendroid", desired_capabilities = caps, apk_path = test_apk, server_path = server_jar_path)
        
        (MobileElement.by,MobileElement.value) = ("ID","login_account_input")
        print "Input:brucestudent1",MobileElement.IsExist()
        MobileElement.Set("brucestudent1")
        (MobileElement.by,MobileElement.value) = ("ID","login_password_input")
        print "Input:123456",MobileElement.IsExist()
        MobileElement.Set("123456")
        (MobileElement.by,MobileElement.value) = ("ID","login_start_button")
        print "Click loginbtn",MobileElement.IsExist()
        MobileElement.Click()
        MobileElement.WaitForDisappearing()
        
        (MobileElement.by,MobileElement.value) = ("PARTIAL_LINK_TEXT","课前预习")
        print "Click 课前预习",MobileElement.IsExist()
        MobileElement.Click()    
        (MobileElement.by,MobileElement.value) = ("ID","search_drop_down")
        print "Click 搜索",MobileElement.IsExist()
        MobileElement.Click()
        (MobileElement.by,MobileElement.value) = ("PARTIAL_LINK_TEXT","时间")
        print "Click 时间",MobileElement.IsExist()
        MobileElement.Click()
        print "Home return"    
        MobileApp.Back()
        
#         (MobileElement.by,MobileElement.value) = (By.XPATH,"//TextView[@value='自动化测试--编辑游戏练...']")
#         print "Text is:",MobileElement.text
    except Exception,e:
        print "======================================end"
        print e
    finally:     
        MobileApp.AppClose()
        print "Closed session."
        
    
if __name__ == "__main__":
    usage_for_selendroid()
    
