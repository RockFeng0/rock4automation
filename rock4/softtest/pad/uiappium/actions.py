# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.pad.uiappium.actions

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pad.uiappium.actions,v 1.0 2017年2月8日
    FROM:   2017年2月8日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''



from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os,time,subprocess
from rock4.common import p_env, p_common


class MobileApp():
    ''' Mobile App Test.(need appium API>=17)'''
    
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
            raise Exception("Executor['%s'] was not supported.Select one for your executor in %s" %(executor,executors.keys()))
        
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
    def Lock(cls,seconds):
        getattr(p_env.MOBILE,"lock")(seconds)
        time.sleep(0.5)
    
    @classmethod
    def BackgroundApp(cls,seconds):
        getattr(p_env.MOBILE,"background_app")(seconds)
        time.sleep(0.5)
    
    @classmethod
    def OpenNotifications(cls):
        getattr(p_env.MOBILE,"open_notifications")()
        time.sleep(0.5)
    
    @classmethod
    def NavigateTo(cls,app_package ,app_activity):
        ''' 
        app_package = "io.appium.android.apis"
        app_activity = ".view.DragAndDropDemo"
        app_activity = ".ApiDemos"
        '''
        getattr(p_env.MOBILE,"start_activity")(app_package,app_activity)
        time.sleep(0.5)
        
    @classmethod
    def IsAppInstalled(cls,app_package):
        return getattr(p_env.MOBILE,"is_app_installed")(app_package)
            
    @classmethod
    def InstallApp(cls,app_abs_path):
        ''' install the app to mobile
        app_abs_path=r"c:\test.apk"        
        '''
        # // todo
        return getattr(p_env.MOBILE,"is_app_installed")(app_abs_path)
        
    
    @classmethod
    def Reset(cls):
        '''相当于卸载、重装应用'''
        getattr(p_env.MOBILE,"reset")()
        
    @classmethod
    def RemoveApp(cls,app_package):
        getattr(p_env.MOBILE,"remove_app")(app_package)
    
    @classmethod
    def CloseApp(cls):
        ''' only close app . keep the session'''
        getattr(p_env.MOBILE,"close_app")()
        
    @classmethod
    def LaunchApp(cls):
        ''' use current session to launch and active the app'''
        getattr(p_env.MOBILE,"launch_app")()
    
    @classmethod
    def GetCurrentContext(cls):        
        return getattr(p_env.MOBILE,"current_context")
    
    @classmethod
    def GetCurrentContexts(cls):        
        return getattr(p_env.MOBILE,"contexts")
    
    @classmethod
    def GetCurrentActivity(cls):        
        return getattr(p_env.MOBILE,"current_activity")
    
    @classmethod
    def GetAppString(cls):        
        return getattr(p_env.MOBILE,"app_strings")()
            
    @classmethod
    def SwitchToContext(cls,context_name):
        try:
            getattr(p_env.MOBILE,"switch_to.context")(context_name)
        except:
            pass
        
    @classmethod
    def SwitchToDefaultContext(cls):        
        try:
            getattr(p_env.MOBILE,"switch_to.context")(None)
        except:
            pass
    
    @classmethod
    def Keyevent(cls,key_code_name):
        getattr(p_env.MOBILE,"keyevent")(key_code_name)
        
    @classmethod
    def Forward(cls):
        getattr(p_env.MOBILE,"forward")()
       
    @classmethod
    def Back(cls):
        getattr(p_env.MOBILE,"back")()
    
    @classmethod
    def Shake(cls):
        ''' 模拟设备摇晃 '''
        getattr(p_env.MOBILE,"shake")()
        
    @classmethod
    def Swipe(cls, startx, starty, endx, endy,duration=None):
        ''' 模拟用户滑动 '''
        getattr(p_env.MOBILE,"swipe'")(startx,starty,endx,endy,duration)
    
    @classmethod
    def SwipeLeft(cls,times):
        driver = p_env.MOBILE        
        width = driver.get_window_size()["width"]
        height = driver.get_window_size()["height"]
        for i in range(times):
            driver.swipe(width/4*3, height / 2, width / 4 *1, height / 2, 500)
            time.sleep(1)
    
    @classmethod
    def SwipeRight(cls,times):
        driver = p_env.MOBILE        
        width = driver.get_window_size()["width"]
        height = driver.get_window_size()["height"]
        for i in range(times):
            driver.swipe(width/4*1, height / 2, width / 4 *3, height / 2, 500)
            time.sleep(1)
    
    @classmethod
    def SwipeUp(cls,times):
        driver = p_env.MOBILE        
        width = driver.get_window_size()["width"]
        height = driver.get_window_size()["height"]
        for i in range(times):
            driver.swipe(width/2, height/4*3, width /2, height/4*1, 500)
            time.sleep(1)
            
    @classmethod
    def SwipeDown(cls,times):
        driver = p_env.MOBILE        
        width = driver.get_window_size()["width"]
        height = driver.get_window_size()["height"]
        for i in range(times):
            driver.swipe(width/2, height/4*1, width /2, height/4*3, 500)
            time.sleep(1)
                        
    @classmethod
    def Tap(cls,positions,duration=None):
        ''' 模拟用户点击 '''
        getattr(p_env.MOBILE,"tap'")(positions,duration)
         
    @classmethod
    def QuitApp(cls):
        ''' will close the session '''
        try:
            getattr(p_env.MOBILE,"quit")()            
        except:
            pass
        
        try:
            cls.__sub_process.kill()
        except:
            pass
            
    
    
class MobileElement():
    ''' Mobile App Element Test.(need appium API>=17)'''
    (by, value) = (None, None)
    (index,timeout) = (0,10)
    __glob = {}
    
    @classmethod
    def SetVar(cls, name, value):
        ''' set static value
        :param name: glob parameter name
        :param value: parameter value
        '''
        cls.__glob.update({name:value})
                
    @classmethod
    def GetVar(cls, name):
        return cls.__glob.get(name)
    
    @classmethod
    def TimeSleep(cls,seconds):
        time.sleep(seconds)
        
    @classmethod
    def GetElement(cls):
        element = None
        try:
            element = cls.__wait()
        except Exception,e:
            print e
        finally:
            return element
    
    @classmethod
    def Set(cls, value):
        if value == "":
            return
        
        if value == "SET_EMPTY":
            value = ""
                
        element = cls.__wait()
        
        if element.tag_name == "android.widget.ListView":
            cls.Select(value)        
        else:
            element.clear()
            action = ActionChains(p_env.MOBILE)
            action.send_keys_to_element(element, value)            
            action.perform()
            
            cls.__clearup()
    
    @classmethod
    def Select(cls, value):
        if value == "":
            return
                
        element = cls.__wait()        
        #### ListView ################
        if element.tag_name == "android.widget.ListView":
            elms = element.find_elements_by_name(value)            
            if elms:
                elms[0].click()
                        
        #### NOT Supported ################
        else:
            print "Element [%s]: Tag Name [%s] Not Support [Select]." % (cls.__name__, element.tag_name)
        cls.__clearup()
    
    @classmethod
    def TypeIn(cls, value):
        '''
        input value without clear existed values
        '''
        if value == "": return
                
        element = cls.__wait()        
        action = ActionChains(p_env.MOBILE)
        action.send_keys_to_element(element, value)
        action.perform()
        
        cls.__clearup()
        
    @classmethod
    def SelectByOrder(cls, order):
        if order == "":
            return
        
        order = int(order)
        
        element = cls.__wait()
        
        #### ListView ################
        if element.tag_name == "android.widget.ListView":
            elms = getattr(p_env.MOBILE,"find_elements")("xpath", "//android.widget.ListView[%s]/*" %(cls.index))
            
            if elms and order<len(elms):
                elms[order].click()
                        
        #### NOT Supported ################
        else:
            print "Element [%s]: Tag Name [%s] Not Support [Select]." % (cls.__name__, element.tag_name)
        cls.__clearup()
  
    @classmethod
    def ScrollDown(cls):
        ''' 
        Sample usage:
        (by,value)=(By.XPATH,"//android.widget.TextView")
        ScrollDown()
        '''
        cls.__wait()
        elements = getattr(p_env.MOBILE,"find_elements")(cls.by, cls.value)        
        getattr(p_env.MOBILE,"scroll")(elements[len(elements)-1], elements[0])        
        cls.__clearup()
    
    @classmethod
    def ScrollUp(cls):
        '''
        Sample usage:
        (by,value)=(By.XPATH,"//android.widget.TextView")
        ScrollUp()
        '''
        cls.__wait()
        elements = getattr(p_env.MOBILE,"find_elements")(cls.by, cls.value)        
        getattr(p_env.MOBILE,"scroll")(elements[0],elements[len(elements)-1])        
        cls.__clearup()
    
    @classmethod
    def Click(cls):
        element = cls.__wait()        
        element.click()
        cls.__clearup()
   
    @classmethod
    def LongPress(cls):
        element = cls.__wait()   
        action = TouchAction(p_env.MOBILE)
        action.long_press(element)
        action.perform()        
        cls.__clearup()
    
    @classmethod
    def PressAndHold(cls):        
        element = cls.__wait()
        action = TouchAction(p_env.MOBILE)
        action.press(element)
        action.perform()        
        cls.__clearup()    
    @classmethod
    def MoveTo(cls):
        
        element = cls.__wait()
        action = TouchAction(p_env.MOBILE)
        action.move_to(element)
        action.perform()
        cls.__clearup()    
    
    @classmethod        
    def ReleasePress(cls):
        action = TouchAction(p_env.MOBILE)
        action.release()
        action.perform()
                
    @classmethod
    def MultiDraw(cls):
        e1 = TouchAction()
        e1.press(x=150, y=100).release()

        e2 = TouchAction()
        e2.press(x=250, y=100).release()

        smile = TouchAction()
        smile.press(x=110, y=200).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=2, y=1)
#         smile.press(x=110, y=200).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=2, y=1).move_to(x=2, y=1).\
#             move_to(x=2, y=1).move_to(x=2, y=1).move_to(x=2, y=1).move_to(x=3, y=1).move_to(x=3, y=1).move_to(x=3, y=1).move_to(x=3, y=1).move_to(x=3, y=1).move_to(x=4, y=1).\
#             move_to(x=4, y=1).move_to(x=4, y=1).move_to(x=4, y=1).move_to(x=4, y=1).move_to(x=5, y=1).move_to(x=5, y=1).move_to(x=5, y=1).move_to(x=5, y=1).move_to(x=5, y=1).\
#             move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=-1).\
#             move_to(x=5, y=-1).move_to(x=5, y=-1).move_to(x=5, y=-1).move_to(x=5, y=-1).move_to(x=4, y=-1).move_to(x=4, y=-1).move_to(x=4, y=-1).move_to(x=4, y=-1).move_to(x=4, y=-1).\
#             move_to(x=3, y=-1).move_to(x=3, y=-1).move_to(x=3, y=-1).move_to(x=3, y=-1).move_to(x=3, y=-1).move_to(x=2, y=-1).move_to(x=2, y=-1).move_to(x=2, y=-1).move_to(x=2, y=-1).\
#             move_to(x=2, y=-1).move_to(x=1, y=-1).move_to(x=1, y=-1).move_to(x=1, y=-1).move_to(x=1, y=-1).move_to(x=1, y=-1)
        smile.release()

        ma = MultiAction(p_env.MOBILE)
        ma.add(e1, e2, smile)
        ma.perform()
        
    @classmethod
    def SendEnter(cls):
        element = cls.__wait()        
        action = ActionChains(p_env.MOBILE)
        action.send_keys_to_element(element, Keys.ENTER)
        action.perform()        
        cls.__clearup()
    
    @classmethod
    def GetFocus(cls):
        
        element = cls.__wait()   
        element.send_keys(Keys.NULL)        
        action = ActionChains(p_env.MOBILE)
        action.send_keys_to_element(element, Keys.NULL)
        action.perform()        
        cls.__clearup()    
    
    @classmethod
    def GetObjectsCount(cls):        
        cls.__wait_for_appearing()        
        elements = getattr(p_env.MOBILE,"find_elements")(cls.by, cls.value)
        cls.__clearup()
        return len(elements)
        
    @classmethod
    def GetPageXML(cls):
        return getattr(p_env.MOBILE,"page_source")
        
    @classmethod
    def GetAttribute(cls, attr):        
        element = cls.__wait()        
        attr_value = element.get_attribute(attr)        
        cls.__clearup()
        return attr_value
                        
    @classmethod
    def WaitForAppearing(cls):
        result = cls.__wait_for_appearing()
        cls.__clearup()
        return result
           
    @classmethod
    def WaitForDisappearing(cls):
        result = cls.__wait_for_disappearing()
        cls.__clearup()
        return result
    
    @classmethod
    def WaitForVisible(cls):
        element = cls.__wait()
        result = element.is_displayed()
        cls.__clearup()
        return result
        
    @classmethod
    def IsEnabled(cls):
        element = cls.__wait()        
        if element.is_enabled():
            cls.__clearup()
            return True
        else:
            cls.__clearup()
            return False    
    
    @classmethod
    def IsExist(cls): 
        elements = getattr(p_env.MOBILE,"find_elements")(cls.by, cls.value)
        cls.__clearup()        
        if len(elements) > 0:
            return True
        else:
            return False
    
    @classmethod
    def IsVisible(cls):
        element = cls.__wait()
        if element.is_displayed():
            cls.__clearup()
            return True
        else:
            cls.__clearup()
            return False
          
    @classmethod
    def __wait(cls):
        if not cls.__is_selector():
            raise Exception("Invalid selector[%s]." %cls.by)
            
        driver = p_env.MOBILE
        try:            
            elements = WebDriverWait(driver, cls.timeout).until(lambda driver: getattr(driver,"find_elements")(cls.by, cls.value))
        except:            
            raise Exception("Timeout at %d seconds.Element(%s) not found." %(cls.timeout,cls.value))
        
        if len(elements) < cls.index + 1:                    
            raise Exception("Element [%s]: Element Index Issue! There are [%s] Elements! Index=[%s]" % (cls.__name__, len(elements), cls.index))
        
        if len(elements) > 1:              
            print "Element [%s]: There are [%d] elements, choosed index=%d" %(cls.__name__,len(elements),cls.index)
            
        return elements[cls.index]
                
    @classmethod
    def __wait_for_disappearing(cls):
        try:
            if cls.__wait():
                return False
            return True
        except:
            return True
    
    @classmethod
    def __wait_for_appearing(cls):
        try:
            if cls.__wait():
                return True
            return False
        except:
            return False
    
    @classmethod
    def __is_selector(cls):
        all_By_selectors = ['CLASS_NAME', 'CSS_SELECTOR', 'ID', 'LINK_TEXT', 'NAME', 'PARTIAL_LINK_TEXT', 'TAG_NAME', 'XPATH']
        all_selectors = [By.CLASS_NAME, By.CSS_SELECTOR, By.ID, By.LINK_TEXT, By.NAME, By.PARTIAL_LINK_TEXT, By.TAG_NAME, By.XPATH]
        
        if cls.by in all_By_selectors:
            cls.by = getattr(By, cls.by)
            return True
        
        if cls.by in all_selectors:
            return True
        
        print "Warning: selector[%s] should be in %s" %(cls.by,all_By_selectors)
        return False
        
    @classmethod
    def __clearup(cls):
        if cls.index != 0:
            
            print "Element [%s]: The Operation Element Index = [%s]." % (cls.__name__, cls.index)
        
        cls.index = 0
    
    ''' Useless Functions
    @classmethod
    def VerifyExistence(cls, trueORfalse):        
        if trueORfalse == True:
            cls.__wait_for_appearing()
        else:
            cls.__wait_for_disappearing()
        
        
        
        cls.__clearup()
        if len(elements) > 0:
            if trueORfalse == True:
                print "pass,Exists!"
            else:
                print "fail,Exists!"
        else:
            if trueORfalse == False:
                print "pass,Not Exists!"
            else:
                print "fail,Not Exists!"
    
    
    @classmethod
    def VerifyEnabled(cls, trueOrfalse):
        
        
        element = cls.__wait()
        
        
        if element.is_enabled():
            if trueOrfalse == True:
                
                print "Pass"
            else:
                
                print "Fail"
        else:
            if trueOrfalse == True:
                
                print "Fail"
            else:
                
                print "Pass"
        
        cls.__clearup()
    
  
    @classmethod
    def VerifyAttribute(cls, attr, contain_content):
        if contain_content == "": return
        
        
        
        element = cls.__wait()
        
        attr_value = element.get_attribute(attr)
        
        if contain_content == attr_value:
            
            print "Real attr_value=[%s]" % attr_value
        else:
            
            "Real attr_value=[%s]" % attr_value
        cls.__clearup()
    
    
    @classmethod
    def VerifyAttributeContains(cls, attr, contain_content):
        if contain_content == "": return
        
        element = cls.__wait()
        
        attr_value = element.get_attribute(attr)
        
                
        if contain_content in attr_value:            
            print "Real attr_value=[%s]" % attr_value
        else:            
            print "Real attr_value=[%s]" % attr_value
        
        cls.__clearup()
    '''
def usage_for_appium():
    #app_path = os.path.dirname(__file__)
    app_path = r'D:\auto\python\app-autoApp\demoProject\apps\ApiDemos'
    PATH = lambda p: os.path.abspath(
        os.path.join(app_path, p)
    )
    
    desired_capabilities = {}
    desired_capabilities['platformName'] = 'Android'
    desired_capabilities['platformVersion'] = '4.4.2'
    desired_capabilities['deviceName'] = 'device'
    desired_capabilities['app'] = PATH("ApiDemos-debug.apk")
    #desired_capabilities['appPackage'] = 'io.appium.android.apis'
    #desired_capabilities['appActivity'] = '.ApiDemos'
            
    
    try:
        # Initial connection
        MobileApp.Init("appium", desired_capabilities, server_path = r'E:\android-sdk\Appium')
        
        #  Start activity
        MobileApp.NavigateTo("io.appium.android.apis", ".view.DragAndDropDemo")    
        
        #
        (MobileElement.by,MobileElement.value) = ("ID","io.appium.android.apis:id/drag_dot_3")
        MobileElement.PressAndHold()
        (MobileElement.by,MobileElement.value) = ("ID","io.appium.android.apis:id/drag_dot_2")
        MobileElement.MoveTo()
        time.sleep(2)
        MobileElement.ReleasePress()
        
        MobileApp.NavigateTo("io.appium.android.apis", ".ApiDemos")
        (MobileElement.by,MobileElement.value) = ("ID","android:id/text1")
        MobileElement.ScrollDown()
        
        (MobileElement.by,MobileElement.value) = ("NAME","Views")
        MobileElement.Click()
        
        (MobileElement.by,MobileElement.value) = ("NAME","Controls")
        MobileElement.Click()
        
        (MobileElement.by,MobileElement.value) = ("ID","android:id/list")
        MobileElement.Select("1. Light Theme")
        MobileApp.Back()    
        MobileElement.Set("1. Light Theme")
        print MobileApp.GetCurrentActivity();# 打印   u'.view.Controls1'
        
        (MobileElement.by,MobileElement.value) = ("ID","io.appium.android.apis:id/edit")
        MobileElement.TypeIn("Hello Android.")
        MobileElement.Set("Hello World!")
        
        print MobileElement.GetPageXML().encode("utf-8")
        print "edit is exist: ",MobileElement.IsExist()
        print "edit is visible: ",MobileElement.IsVisible()
        print "edit is enabled: ",MobileElement.IsEnabled()
        
        # 画个 笑脸
        MobileApp.NavigateTo("io.appium.android.apis", ".graphics.TouchPaint");# apidemos->Graphics->Touch Paint
        print MobileApp.GetCurrentActivity();# 打印   u'.graphics.TouchPaint'
        MobileElement.MultiDraw()
    except Exception,e:
        print "======================================end"
        print e
    finally:
        MobileApp.QuitApp()
        
if __name__ == "__main__":    
    usage_for_appium()
    