# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.web.actions

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.web.actions,v 1.0 2017年2月18日
    FROM:   2017年2月18日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time,os
from rock4.common import p_env, p_log

class WebBrowser:
    ''' Browser Element.(selenium)'''
        
    @classmethod
    def Init(cls,name,download_path, marionette=False):
#         name = name.lower()
#         if name in ("firefox","chrome","ie","opera","safari"):
#             p_env.BROWSER = getattr(webdriver,name[0].upper()+name[1:])()
#         else:
#             p_env.BROWSER = webdriver.Ie()
                    
        if name == "firefox":
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
                
            p_env.BROWSER = webdriver.Firefox(firefox_profile=fp, capabilities =cap)
                   
        elif name == "chrome":
            options = webdriver.ChromeOptions()
            if download_path and os.path.isdir(download_path):
                prefs = {"download.default_directory": download_path}
                options.add_experimental_option("prefs", prefs)
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
            p_env.BROWSER = webdriver.Chrome(chrome_options=options)
            
    
    @classmethod
    def Title(cls):
        # 获取当前页面的title
        return p_env.BROWSER.title
    
    @classmethod
    def URL(cls):
        """ 获取当前页面的url """
        return getattr(p_env.BROWSER,"current_url")
    
    @classmethod
    def Js(self, script):
        """ 浏览器最大化       """
        getattr(p_env.BROWSER,"execute_script")(script)

    @classmethod
    def Maximize(self):
        """ 浏览器最大化       """
        getattr(p_env.BROWSER,"maximize_window")()

    def SetWindowSize(self, width, height):
        """ 设定浏览器宽高   """
        getattr(p_env.BROWSER,"set_window_size")(width, height)        
    
    @classmethod
    def ScrollTo(cls, x, y):
        #p_log.step_info("normal",u"Element [%s]: Scroll To [%s, %s]" % (cls.__name__, x, y))
        # X-Y-top: window.scrollTo("0","0")
        # X-bottom:  window.scrollTo("10000","0"),   Y-bottom:  window.scrollTo("0","10000")           
        getattr(p_env.BROWSER,"execute_script")("window.scrollTo(%s, %s);" % (x, y))
    
    @classmethod
    def Refresh(cls):
        #p_log.step_info("normal",u"Element [%s]: Browser Refresh" % (cls.__name__,))
        getattr(p_env.BROWSER,"refresh")()
            
    @classmethod
    def NavigateTo(cls, url):
        #p_log.step_info("normal",u"Element [%s]: Navigate To [%s]" % (cls.__name__, url))
        getattr(p_env.BROWSER,"get")(url)
        
    @classmethod
    def IESkipCertError(cls):
        #p_log.step_info("normal","IE Skip SSL Cert Error.")
        getattr(p_env.BROWSER,"get")("javascript:document.getElementById('overridelink').click();")
    
    
    @classmethod
    def Forward(cls):
        #p_log.step_info("normal","To move forwards in browser’s history")
        getattr(p_env.BROWSER,"forward")()
        
    
    @classmethod
    def Back(cls):
        #p_log.step_info("normal","To move backwards in browser’s history.")
        getattr(p_env.BROWSER,"back")()
        
            
    @classmethod
    def AlertAccept(cls):                
        alert = cls.SwitchToAlert()
        if alert:
            alert.accept()
        cls.SwitchToDefaultFrame()
               
    @classmethod
    def AlertDismiss(cls):
        alert = cls.SwitchToAlert()
        if alert:
            alert.dismiss()
        cls.SwitchToDefaultFrame()
                    
    
    @classmethod
    def AlertSendKeys(cls, value):
        alert = cls.SwitchToAlert()
        if alert:
            alert.send_keys(value)
        cls.SwitchToDefaultFrame()
        
    @classmethod
    def AlertTextHave(cls, txt_value):        
        alert = cls.SwitchToAlert()
        result = False    
        if alert and txt_value in alert.text:                        
            result = True                        
        cls.SwitchToDefaultFrame()
        return result
    
    @classmethod
    def SwitchToAlert(cls):
        driver = p_env.BROWSER
        try:            
            alert = WebDriverWait(driver, cls.timeout).until(lambda driver: driver.switch_to_alert())
            return alert            
        except:            
            print "Waring: Timeout at %d seconds.Alert was not found."
        
    @classmethod
    def SwitchToFrame(cls,frame_name):
        driver = p_env.BROWSER
        try:            
            WebDriverWait(driver, cls.timeout).until(lambda driver: getattr(driver,"switch_to.frame")(frame_name))          
        except:            
            print "Waring: Timeout at %d seconds.Frame %s was not found." %frame_name
    
    @classmethod
    def SwitchToDefaultFrame(cls):        
        try:
            getattr(p_env.BROWSER,"switch_to_default_content")()
        except:
            pass        
        
    @classmethod
    def SwitchToNewPopWindow(cls):
        driver = p_env.BROWSER
        try:            
            WebDriverWait(driver, cls.timeout).until(lambda driver: len(driver.window_handles) < 2)
            driver.switch_to.window(driver.window_handles[-1])
        except:            
            print "Waring: Timeout at %d seconds. Pop Window Not Found."
            
    @classmethod
    def SwitchToDefaultWindow(cls):             
        try:
            getattr(p_env.BROWSER,"switch_to.window")(getattr(p_env.BROWSER,"window_handles")[0])
        except:
            pass                
    
    @classmethod
    def ScreenShoot(cls,f_path):
        return getattr(p_env.BROWSER,"save_screenshot")(f_path)
    
    @classmethod
    def WebClose(cls):
        try:
            getattr(p_env.BROWSER,"quit")()
        except:
            pass


class WebElement:
    ''' Web Element.(selenium)'''
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
    def TimeSleep(cls, seconds):
        time.sleep(seconds)
        
    @classmethod
    def Set(cls, value):
        if value == "":
            return
        
        if value == "SET_EMPTY":
            value = ""
        
        #p_log.step_info("normal",u"Element [%s]: Set Value [%s]." % (cls.__name__, value))
        
        element = cls.__wait()        
        
        if element.tag_name == "select" or element.tag_name == "ul":
            cls.Select(value)        
        else:
            element.clear()
            action = ActionChains(p_env.BROWSER)
            action.send_keys_to_element(element, value)            
            action.perform()
            
            cls.__clearup()
    
    @classmethod
    def TypeIn(cls, value):
        '''
        input value without clear existed values
        '''
        if value == "": return
        
        #p_log.step_info("normal",u"Element [%s]: TypeIn Value [%s]." % (cls.__name__, value))
        
        element = cls.__wait()
        
        action = ActionChains(p_env.BROWSER)
        action.send_keys_to_element(element, value)
        action.perform()
        
        cls.__clearup()
        
    @classmethod
    def Select(cls, value):
        if value == "":
            return
        
        #p_log.step_info("normal","Element [%s]: Do Select [%s]." % (cls.__name__, value))
        
        element = cls.__wait()
        
        #### select ################
        if element.tag_name == "select":
            options = element.find_elements_by_tag_name('option')
            
            for option in options:
                if option.text == value:
                    option.click()
                    break
        
        #### ul ################
        elif element.tag_name == "ul":
            lis = element.find_elements_by_tag_name('li')
            
            for li in lis:
                if li.text == value:
                    li.click()
                    break
        
        #### NOT Supported ################
        else:
            #p_log.step_info("fail","Element [%s]: Tag Name [%s] Not Support [Select]." % (cls.__name__, elements[cls.index].tag_name))
            print "Element [%s]: Tag Name [%s] Not Support [Select]." % (cls.__name__, element.tag_name)
        cls.__clearup()
    
    
    @classmethod
    def SelectByOrder(cls, order):
        if order == "": return
        
        #p_log.step_info("normal","Element [%s]: Do Select by Order [%s]" % (cls.__name__, order))
        
        order = int(order)
        
        element= cls.__wait()
        
        #### ul ################
        if element.tag_name == "ul":
            lis = element.find_elements_by_tag_name('li')
            
            if order > 0:
                
                ### Wait and try more times if NO item found. ###
                t = 0
                while (len(lis) == 0):
                    lis = element.find_elements_by_tag_name('li')
                    time.sleep(0.5)
                    t = t + 1
                    #p_log.step_info("normal","Element [%s]: Wait 3 Seconds for [li]" % cls.__name__)
                    
                    if t == 8 and len(lis) == 0:
                        #p_log.step_info("fail","Element [%s]: List Count = [%s]." % (cls.__name__, len(lis)))
                        return
                
                
                #p_log.step_info("normal","Element [%s]: List Count = [%s]." % (cls.__name__, len(lis)))
                
                if (order > len(lis)):
                    #p_log.step_info("normal","Element [%s]: Not so many lists. [%s]" % (cls.__name__, len(lis)))
                    print "Element [%s]: Not so many lists. [%s]" % (cls.__name__, len(lis))
                else:
                    #p_log.step_info("normal","Element [%s]: Do Click [%s]" % (cls.__name__, order))
                    action = ActionChains(p_env.BROWSER)
                    action.click(lis[order-1])
                    action.perform()
            else:
                #p_log.step_info("fail","Order = [%s], Value Error." % order)
                print "Order = [%s], Value Error." % order
                
        #### select ################
        if element.tag_name == "select":
            options = element.find_elements_by_tag_name('option')
            
            if order > 0:
                
                ### Wait and try more times if NO item found. ###
                t = 0
                while (len(options) == 0):
                    options = element.find_elements_by_tag_name('option')
                    time.sleep(0.5)
                    t = t + 1
                    #p_log.step_info("normal","Element [%s]: Wait 3 Seconds for [option]" % cls.__name__)
                    
                    if t == 8 and len(lis) == 0:
                        #p_log.step_info("fail","Element [%s]: options Count = [%s]." % (cls.__name__, len(options)))
                        return
                
                
                #p_log.step_info("normal","Element [%s]: options Count = [%s]." % (cls.__name__, len(options)))
                
                if (order > len(options)):
                    #p_log.step_info("normal","Element [%s]: Not so many options. [%s]" % (cls.__name__, len(options)))
                    print "Element [%s]: Not so many options. [%s]" % (cls.__name__, len(options))
                else:
                    #p_log.step_info("normal","Element [%s]: Do Click [%s]" % (cls.__name__, order))
                    action = ActionChains(p_env.BROWSER)
                    action.click(options[order-1])
                    action.perform()
            else:
                #p_log.step_info("fail","Order = [%s], Value Error." % order)
                print "Order = [%s], Value Error." % order
        
        
        cls.__clearup()
    
    
    @classmethod
    def MouseOver(cls):
        #p_log.step_info("normal","Element [%s]: Do MouseOver()" % (cls.__name__))
        
        element = cls.__wait()
                
        action = ActionChains(p_env.BROWSER)
        action.move_to_element(element)
        action.perform()
        
        cls.__clearup()
        
        time.sleep(1)
    
    
    @classmethod
    def Click(cls):
        #p_log.step_info("normal","Element [%s]: Do Click()" % (cls.__name__))
        
        element= cls.__wait()
        
        action = ActionChains(p_env.BROWSER)
        action.click(element)
        action.perform()
        
        cls.__clearup()
    
    @classmethod
    def ClickText(cls, text):
        elements= cls.__waits()
        action = ActionChains(p_env.BROWSER)
        for element in elements:
            try:
                if element.text.strip() == text:
                    action.click(element)
                    action.perform()
                    break           
            except:
                pass
        cls.__clearup()
            
    @classmethod
    def EnhancedClick(cls):
        '''
        Description:
            Sometimes, one click on the element doesn't work. So wait more time, then click again and again.
        Risk:
            It may operate more than one click operations.
        '''
        #p_log.step_info("normal","Element [%s]: Doing EnhancedClick()" % (cls.__name__))
        
        element = cls.__wait()
        
        i = 0
        while(i < 3):
                       
            action = ActionChains(p_env.BROWSER)
            action.move_to_element(element)
            action.perform()
            
            time.sleep(0.5)
            i = i + 1
                
        cls.__clearup()
    
    @classmethod
    def RightClick(cls):
        #p_log.step_info("normal","Element [%s]: Do DoubleClick()" % (cls.__name__))
        
        element = cls.__wait()
        
        action = ActionChains(p_env.BROWSER)
        action.context_click(element)
        action.perform()
        
        cls.__clearup()
    
    @classmethod
    def RightClickText(cls, text):
        elements = cls.__waits()
        for element in elements:
            try:
                if text == element.text.strip():
                    ActionChains(p_env.BROWSER).context_click(element).perform()
                    break
            except:
                pass
        cls.__clearup()
                
    @classmethod
    def DoubleClick(cls):
        #p_log.step_info("normal","Element [%s]: Do DoubleClick()" % (cls.__name__))
        
        element = cls.__wait()
        
        action = ActionChains(p_env.BROWSER)
        action.double_click(element)
        action.perform()
        
        cls.__clearup()
    
    
    @classmethod
    def DoubleClickText(cls, text):
        elements = cls.__waits()
        for element in elements:
            try:
                if text == element.text.strip():
                    ActionChains(p_env.BROWSER).double_click(element).perform()
                    break
            except:
                pass
        cls.__clearup()
    
    @classmethod
    def ClickAndHold(cls):
        #p_log.step_info("normal","Element [%s]: Do ClickAndHold()" % (cls.__name__))
        
        element = cls.__wait()
        
        action = ActionChains(p_env.BROWSER)
        action.click_and_hold(element)
        action.perform()
        
        cls.__clearup()
    
    
    @classmethod
    def ReleaseClick(cls):
        #p_log.step_info("normal","Element [%s]: Do ReleaseClick()" % (cls.__name__))
        
        element = cls.__wait()
        
        action = ActionChains(p_env.BROWSER)
        action.release(element)
        action.perform()
        
        cls.__clearup()
    
    @classmethod
    def MoveAndDropTo(cls):
        cls.ReleaseClick()
    
    @classmethod
    def Enter(cls):
        #p_log.step_info("normal",u"Element [%s]: SendEnter()" % (cls.__name__, ))
        
        element = cls.__wait()
        
        action = ActionChains(p_env.BROWSER)
        action.send_keys_to_element(element, Keys.ENTER)
        action.perform()
        
        cls.__clearup()
    
    @classmethod
    def Ctrl(cls, key):
        """
        在指定元素上执行ctrl组合键事件
        :param key: 如'X'
        """
        element = cls.__wait()
        element.send_keys(Keys.CONTROL, key)
        cls.__clearup()
        
    @classmethod
    def Alt(cls, key):
        """
        在指定元素上执行alt组合事件
        :param key: 如'X'
        """
        element = cls.__wait()
        element.send_keys(Keys.ALT, key)
        cls.__clearup()
    
    @classmethod
    def Space(cls):
        """
        在指定输入框发送空格
        """
        element = cls.__wait()
        element.send_keys(Keys.SPACE)
        cls.__clearup()
    
    @classmethod
    def Backspace(cls):
        """
        在指定输入框发送回退键
        """
        element = cls.__wait()
        element.send_keys(Keys.BACK_SPACE)
        cls.__clearup()
    
    @classmethod
    def Tab(cls):
        """
        在指定输入框发送回制表键
        """
        element = cls.__wait()
        element.send_keys(Keys.TAB)
        cls.__clearup()
    
    @classmethod
    def Escape(cls):
        """
        在指定输入框发送回制表键
        """
        element = cls.__wait()
        element.send_keys(Keys.ESCAPE)
        cls.__clearup()    
    
    @classmethod
    def GetFocus(cls):
        #p_log.step_info("normal",u"Element [%s]: GetFocus()" % (cls.__name__, ))
        
        element = cls.__wait()
        
        element.send_keys(Keys.NULL)
        
        action = ActionChains(p_env.BROWSER)
        action.send_keys_to_element(element, Keys.NULL)
        action.perform()
        
        cls.__clearup()
    
    @classmethod
    def Upload(cls, filename):
        """
        文件上传
        :param file: 文件名(文件必须存在在工程resource目录下), upload.exe工具放在工程tools目录下
        """
        tool_4path = os.path.join(p_env.TOOLS_PATH, "upload.exe")        
        file_4path = os.path.join(p_env.RESOURCE_PATH, filename)
        #file_4path.decode('utf-8').encode('gbk')
        
        if os.path.isfile(file_4path):
            cls.Click()
            os.system(tool_4path + ' ' + file_4path)
        else:
            raise Exception('%s is not exists' % file_4path)
    
    @classmethod
    def UploadType(cls, file_name):
        """
        文件上传-输入方式，支持原生file文件框
        :param file_name: 文件名(文件必须存在在工程resource目录下)
        """
        file_4path = os.path.join(p_env.RESOURCE_PATH, file_name)
        if os.path.isfile(file_4path):
            cls.TypeIn(file_4path)
        else:
            raise Exception('%s is not exists' % file_name)
        
    @classmethod
    def GetObjectsCount(cls):
        #p_log.step_info("normal","Element [%s]: GetObjectsCount." % (cls.__name__))
        
        cls.__wait_for_appearing()        
        elements = getattr(p_env.BROWSER,"find_elements")(cls.by, cls.value)
        #p_log.step_info("normal","Element [%s]: GetObjectsCount = [%s]" % (cls.__name__, len(elements)))
        
        cls.__clearup()
        return len(elements)
    
    
    @classmethod
    def GetInnerHTML(cls):
        #p_log.step_info("normal",u"Element [%s]: GetInnerHTML." % (cls.__name__, ))
        
        element = cls.__wait()        
        #p_log.step_info("normal",u"Element [%s]: InnerHTML = [%s]" % (cls.__name__, elements[cls.index].get_attribute('innerHTML')))
        
        cls.__clearup()
        return element.get_attribute('innerHTML')
    
    
    @classmethod
    def GetPageHTML(cls):
        return getattr(p_env.BROWSER,"page_source")
            
        
    @classmethod
    def GetAttribute(cls, attr):
        #p_log.step_info("normal",u"Element [%s]: Get Attribute [%s]." % (cls.__name__, attr))
        
        element = cls.__wait()
        
        attr_value = element.get_attribute(attr)
        #p_log.step_info("normal",u"Element [%s]: Attribute Value = [%s]." % (cls.__name__, attr_value))
        
        cls.__clearup()
        return attr_value
    
    @classmethod
    def GetText(cls):
        element= cls.__wait()
        
        try:
            return element.text
        except:
            return 
        
        cls.__clearup()
                    
    @classmethod
    def Wait(cls):
        result = cls.__wait()
        cls.__clearup()
        return result
    
    @classmethod
    def WaitForAppearing(cls):
        #p_log.step_info("normal","Element [%s]: AppearingWait." % (cls.__name__))
        
        result = cls.__wait_for_appearing()
        cls.__clearup()
        return result
    
    
    @classmethod
    def WaitForDisappearing(cls):
        #p_log.step_info("normal","Element [%s]: DisappearingWait." % (cls.__name__))
        
        result = cls.__wait_for_disappearing()
        cls.__clearup()
        return result
    
    
    @classmethod
    def WaitForVisible(cls):
        #p_log.step_info("normal","Element [%s]: WaitForVisible." % (cls.__name__))
        
        element = cls.__wait()
        result = element.is_displayed()
        cls.__clearup()
        return result
    
    @classmethod
    def IsEnabled(cls):
        #p_log.step_info("normal",u"Element [%s]: Is Enabled?" % (cls.__name__))
        
        element = cls.__wait()
        
        if element.is_enabled():
            #p_log.step_info("normal",u"Yes!")
            cls.__clearup()
            return True
        else:
            #p_log.step_info("normal",u"No!")
            cls.__clearup()
            return False
    
    
    @classmethod
    def IsExist(cls):
        cls.__wait_for_appearing()
        elements = getattr(p_env.BROWSER,"find_elements")(cls.by, cls.value)
        #p_log.step_info("normal","Element [%s]: IsExist? Count = [%s]" % (cls.__name__, len(elements)))
        
        cls.__clearup()        
        if len(elements) > 0:
            return True
        else:
            return False
    
    
    @classmethod
    def IsVisible(cls):
        #p_log.step_info("normal","Element [%s]: IsVisible?" % (cls.__name__))
        
        element = cls.__wait()
        
        if element.is_displayed():
            cls.__clearup()
            return True
        else:
            cls.__clearup()
            return False
    
    @classmethod
    def IsText(cls, text):
        #p_log.step_info("normal","Element [%s]: IsVisible?" % (cls.__name__))
        if text == cls.GetText():
            return True
        return False
    
    @classmethod
    def __wait(cls):
        if not cls.__is_selector():
            raise Exception("Invalid selector[%s]." %cls.by)
        
        driver = p_env.BROWSER
        try:            
            elements = WebDriverWait(driver, cls.timeout).until(lambda driver: getattr(driver,"find_elements")(cls.by, cls.value))
        except:            
            raise Exception("Timeout at %d seconds.Element(%s) not found." %(cls.timeout,cls.by))
        
        if len(elements) < cls.index + 1:                    
            raise Exception("Element [%s]: Element Index Issue! There are [%s] Elements! Index=[%s]" % (cls.__name__, len(elements), cls.index))
        
        if len(elements) > 1:              
            print "Element [%s]: There are [%d] elements, choosed index=%d" %(cls.__name__,len(elements),cls.index)
            
        return elements[cls.index]                          
    
    @classmethod
    def __waits(cls):
        if not cls.__is_selector():
            raise Exception("Invalid selector[%s]." %cls.by)
        
        driver = p_env.BROWSER
        try:            
            elements = WebDriverWait(driver, cls.timeout).until(lambda driver: getattr(driver,"find_elements")(cls.by, cls.value))
        except:            
            raise Exception("Timeout at %d seconds.Element(%s) not found." %(cls.timeout,cls.by))
            
        return elements
    
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
            #p_log.step_info("normal","Element [%s]: The Operation Element Index = [%s]." % (cls.__name__, cls.index))
            print "Element ['%s']: The Operation Element Index = [%s]." % (cls.__name__, cls.index)
        
        cls.index = 0
        
        
    ''' Useless functions
    @classmethod
    def VerifyExistence(cls, trueORfalse):
        #p_log.step_info("normal","Element [%s]: Verify Existence = [%s]." % (cls.__name__, trueORfalse))
        
        if trueORfalse == True:
            cls.__wait_for_appearing()
        else:
            cls.__wait_for_disappearing()
        
        elements = getattr(p_env.BROWSER,"find_elements")(cls.by, cls.value)
        #p_log.step_info("normal","Element [%s]: Count = [%s]" % (cls.__name__, len(elements)))
        
        
        cls.__clearup()
        if len(elements) > 0:
            if trueORfalse == True:
                #p_log.step_info("pass","Exist!")
                print "pass,Exists!"
            else:
                #p_log.step_info("fail","Exist!")
                print "fail,Exists!"
        else:
            if trueORfalse == False:
                #p_log.step_info("pass","Not Exist!")
                print "pass,Not Exists!"
            else:
                #p_log.step_info("fail","Not Exist!")
                print "fail,Not Exists!"
    
    
    @classmethod
    def VerifyEnabled(cls, trueOrfalse):
        #p_log.step_info("normal",u"Element [%s]: Verify Enabled = [%s]" % (cls.__name__, trueOrfalse))
        
        cls.__wait()
        elements = getattr(p_env.BROWSER,"find_elements")(cls.by, cls.value)
        
        if elements[cls.index].is_enabled():
            if trueOrfalse == True:
                #p_log.step_info("pass","Pass")
                print "Pass"
            else:
                #p_log.step_info("fail","Fail")
                print "Fail"
        else:
            if trueOrfalse == True:
                #p_log.step_info("fail","Fail")
                print "Fail"
            else:
                #p_log.step_info("pass","Pass")
                print "Pass"
        
        cls.__clearup()
    
    
    @classmethod
    def VerifyInnerHTMLContains(cls, contain_content):
        if contain_content == "": return
        
        #p_log.step_info("normal","Element [%s]: VerifyInnerHTMLContains [%s]." % (cls.__name__, contain_content))
        
        cls.__wait()
        elements = getattr(p_env.BROWSER,"find_elements")(cls.by, cls.value)
        inner_html = elements[cls.index].get_attribute('innerHTML')
        
        if contain_content in inner_html:
            #p_log.step_info("pass","Real inner_hmtl=[%s]" % inner_html)
            print "Real inner_hmtl=[%s]" % inner_html
        else:
            #p_log.step_info("fail","Real inner_hmtl=[%s]" % inner_html)
            print "Real inner_hmtl=[%s]" % inner_html
        cls.__clearup()
    
    
    @classmethod
    def VerifyAttribute(cls, attr, contain_content):
        if contain_content == "": return
        
        #p_log.step_info("normal","Element [%s]: Verify Attribute [%s] == [%s]." % (cls.__name__, attr, contain_content))
        
        cls.__wait()
        elements = getattr(p_env.BROWSER,"find_elements")(cls.by, cls.value)
        attr_value = elements[cls.index].get_attribute(attr)
        
        if contain_content == attr_value:
            #p_log.step_info("pass","Real attr_value=[%s]" % attr_value)
            print "Real attr_value=[%s]" % attr_value
        else:
            #p_log.step_info("fail","Real attr_value=[%s]" % attr_value)
            "Real attr_value=[%s]" % attr_value
        cls.__clearup()
    
    
    @classmethod
    def VerifyAttributeContains(cls, attr, contain_content):
        if contain_content == "": return
        
        #p_log.step_info("normal","Element [%s]: Verify [%s] Contains [%s]." % (cls.__name__, attr, contain_content))
        
        cls.__wait()
        elements = getattr(p_env.BROWSER,"find_elements")(cls.by, cls.value)
        attr_value = elements[cls.index].get_attribute(attr)
        
        #p_log.step_info("normal","Element [%s]: attr_value = [%s]." % (cls.__name__, attr_value))
        
        if contain_content in attr_value:
            #p_log.step_info("pass","Real attr_value=[%s]" % attr_value)
            print "Real attr_value=[%s]" % attr_value
        else:
            #p_log.step_info("fail","Real attr_value=[%s]" % attr_value)
            print "Real attr_value=[%s]" % attr_value
        
        cls.__clearup()
    '''
        
def usage_for_web():
    print "open firefox"
    WebBrowser.Init("firefox")
    print "navigate to www.baidu.com"    
    WebBrowser.NavigateTo("http://www.baidu.com")
    print "refresh www.baidu.com"    
    WebBrowser.Refresh()
    
    print "navigate to knitterDemo"
    WebBrowser.NavigateTo("http://sleepycat.org/static/knitter/KnitterDemo.html")
    
    WebElement.by, WebElement.value = "ID", "title"
    print "select box-test"
    WebElement.Select("Mrs.")
    time.sleep(0.5)
    WebElement.Set("Mr.")
    time.sleep(0.5)
    WebElement.SelectByOrder(3)
    time.sleep(0.5)
    
    WebElement.by, WebElement.value = "CSS_SELECTOR", "#name"
    print "text box-test"
    WebElement.TypeIn("Hello world! 1")
    time.sleep(0.5)
    WebElement.Set("Hello world! 2")
    time.sleep(0.5)
    WebElement.TypeIn("Hello world! 3")
    WebElement.GetFocus()
    WebElement.TypeIn("Hello world! 4")
    time.sleep(0.5)
    print "close firefox"
    WebBrowser.WebClose()
        
if __name__ == "__main__":
    usage_for_web()