# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.drivers.uiautomator.driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pad.uiautomator.driver,v 2.0 2017年2月7日
    FROM:   2016年3月14日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


import threading,os
from uiautomator import Device
from rock4.common import p_env

class PadDevice: 
    ''' Mobile App Test.(need uiautomator)'''
    p_env.MOBILE = Device() 
    
    @classmethod
    def Wakeup(cls):
        print """
        
Connecting the device...

Please check blow, if without an connection in long time:

1. USB-debug model is enabled

2. Device driver is installed

"""
        getattr(p_env.MOBILE,"wakeup")()
        print "connect ok"
   
    @classmethod
    def LaunchApp(cls,app_component):
        # sample: app_component = com.mytest.aischool/.ui.publics.login.LoginActivity
        # adb shell am start -W -n com.tianwen.aischool/.ui.publics.login.LoginActivity    
        cls.Shell("am","start",app_component)        
    
    @classmethod
    def CloseApp(cls,app_package):
        # only close app . keep the session
        # app_package = com.mytest.aischool
        import re
        result = re.search(".*%s\r\n" %app_package,os.popen("adb shell ps").read())
        if result:
            pid = re.findall("\w+",result.group())[1]
            f=open("tmp",'w')
            f.write("su\r\nkill -9 %s\r\nexit\r\nexit\r\n" %pid)
            f.close()
            os.system("adb shell <tmp")
            os.remove("tmp")
            
    @classmethod
    def Click(cls,x,y):
        getattr(p_env.MOBILE,"click")(x, y)
    
    @classmethod
    def LongClick(cls,x,y):
        getattr(p_env.MOBILE,"long_click")(x, y)
    
    @classmethod
    def Swipe(cls,x,y,x2,y2,steps=10):
        getattr(p_env.MOBILE,"swipe")(x, y, x2, y2, steps)

    @classmethod
    def Drag(cls,x,y,x2,y2,steps=10):
        getattr(p_env.MOBILE,"drag")(x, y, x2, y2, steps)
    
    @classmethod
    def Press(cls,name):
        '''You can specify the name in blow:
        ["name","back","left","right","uo","down","center","menu","search","enter","delete","recent","volume_up","volume_down","camera","power",]
        or the name can be the key code for Android KeyEvent
        '''
        getattr(p_env.MOBILE,"press")()
         
    @classmethod
    def Screenoff(cls):
        getattr(p_env.MOBILE,"screen").off()
            
    @classmethod
    def Screenon(cls):
        getattr(p_env.MOBILE,"screen").on()
            
    @classmethod
    def Sleep(cls):
        getattr(p_env.MOBILE,"sleep")()
    
    @classmethod
    def TackScreenShot(cls,img_path):
        # img_path = r'd:\auto\buffer\test.png'
        getattr(p_env.MOBILE,"screenshot")(img_path) 
    
    @classmethod
    def Shell(cls,*cmdstr):
        '''Usage:
            Shell("am","start","com.tianwen.aischool/.ui.publics.login.LoginActivity")
        '''
        tmp = ["shell"]+list(cmdstr)
        getattr(p_env.MOBILE,"server").adb.cmd(*tmp)
        
        
class PadUI:
    ''' Mobile App Element Test.(need uiautomator)'''
    uiselector = {};# uiautomator使用组合的属性，定位UiObject
    uiindex = 0;# 当定位的 UiObject包含多个 elem,使用 index,获取指定UiObject
    childtree = [];# 获取到 UiObject后,通过 childtree 遍历子节点，返回指定UiObject
    timeout = 10000
    
    @classmethod
    def Click(cls):
        if cls.__wait():
            cls.obj.click()
    
    @classmethod    
    def ClickAndWait(cls):
        if cls.__wait():
            cls.obj.click.wait()
    
    @classmethod
    def LongClick(cls):
        if cls.__wait():
            cls.obj.long_click()
    
    @classmethod
    def SetText(cls,unicodestr):
        if cls.__wait():
            cls.obj.click()
            cls.obj.set_text(unicode(unicodestr))
    
    @classmethod
    def ClearText(cls):
        if cls.__wait():
            cls.obj.clear_text()
    
    @classmethod
    def TypeInClear(cls,unicodestr):
        if cls.__wait():
            cls.obj.clear_text()
            cls.obj.set_text(unicode(unicodestr))
    
    @classmethod
    def FlingHorizForward(cls):
        if cls.__wait():
            cls.obj.fling.horiz.forward()
    
    @classmethod
    def FlingVertForward(cls):
        if cls.__wait():
            cls.obj.fling.vert.forward()
        
    @classmethod
    def FlingHorizBackward(cls):
        if cls.__wait():
            cls.obj.fling.horiz.backward()
        
    @classmethod
    def FlingVertBackward(cls):
        if cls.__wait():
            cls.obj.fling.vert.backward()
        
    @classmethod
    def FlingHorizToBegin(cls):
        if cls.__wait():
            cls.obj.fling.horiz.toBeginning()
        
    @classmethod
    def FlingVertToBegin(cls):
        if cls.__wait():
            cls.obj.fling.vert.toBeginning()
        
    @classmethod
    def FlingHorizToEnd(cls):
        if cls.__wait():
            cls.obj.fling.horiz.toEnd()
        
    @classmethod
    def FlingVertToEnd(cls):
        if cls.__wait():
            cls.obj.fling.vert.toEnd()
        
    @classmethod
    def ScrollHorizForward(cls):
        if cls.__wait():
            cls.obj.scroll.horiz.forward()
        
    @classmethod
    def ScrollVertForward(cls):
        if cls.__wait():
            cls.obj.scroll.vert.forward()
        
    @classmethod
    def ScrollHorizBackward(cls):
        if cls.__wait():
            cls.obj.scroll.horiz.backward()
        
    @classmethod
    def ScrollVertBackward(cls):
        if cls.__wait():
            cls.obj.scroll.vert.backward()
        
    @classmethod
    def ScrollHorizToBegin(cls):
        if cls.__wait():
            cls.obj.scroll.horiz.toBeginning()
        
    @classmethod
    def ScrollVertToBegin(cls):
        if cls.__wait():
            cls.obj.scroll.vert.toBeginning()
        
    @classmethod
    def ScrollHorizToEnd(cls):
        if cls.__wait():
            cls.obj.scroll.horiz.toEnd()
        
    @classmethod
    def ScrollVertToEnd(cls):
        if cls.__wait():
            cls.obj.scroll.vert.toEnd()
                  
    @classmethod
    def ScrollToObjTarget(cls,**uiselector):
        print "Get scroll target obj."
        cls.obj.scroll.to(**uiselector)
        print "Scroll action finish."
            
    @classmethod
    def ScrollToObjSource(cls):
        if cls.__wait():
            print "Get scroll source obj."
    
    @classmethod
    def GetInfo(cls):
        if cls.__wait():
            return cls.obj_info
    
    @classmethod
    def GetRectangle(cls):
        if cls.__wait():
            return cls.obj_info.get("bounds")
    
    @classmethod
    def GetText(cls):
        if cls.__wait():
            return cls.obj_info.get("text")
    
    @classmethod
    def GetClassname(cls):
        if cls.__wait():
            return cls.obj_info.get("className")
    
    @classmethod
    def IsExists(cls):        
        if cls.__wait():
            return True
        return False
    
    @classmethod
    def IsChecked(cls):
        if cls.__wait():
            return cls.obj_info.get("checked")
        
    @classmethod
    def IsScrollable(cls):
        if cls.__wait():
            return cls.obj_info.get("scrollable")
    
    @classmethod
    def IsSelected(cls):
        if cls.__wait():
            return cls.obj_info.get("selected")
        
    @classmethod
    def IsEnabled(cls):
        if cls.__wait():
            return cls.obj_info.get("enabled")
    
    @classmethod
    def IsClickable(cls):
        if cls.__wait():
            return cls.obj_info.get("clickable")

    @classmethod
    def __wait_not_exists(cls):
        obj = cls.__get_element()
        
        # 调用UiObject实例方法, 实例Obj对应Elem存在则返回True, 实例Obj对应Elem不存在则会返回False
        if cls.timeout:
            result  = obj.wait.gone(timeout = cls.timeout)
        else:
            result  = obj.wait.gone()
            
        if not result:
            print "Warning: time out(%d).Still exists object. %s " %(cls.timeout,str(cls.uiselector))
        
        return result
    
    @classmethod
    def __wait(cls):
        cls.__clean()              
        obj = cls.__get_element()
        
        # 调用UiObject实例方法, 实例Obj对应Elem存在则返回True, 实例Obj对应Elem不存在则会返回False
        if cls.timeout:
            result = obj.wait.exists(timeout = cls.timeout)
        else:
            result = obj.wait.exists()
            
        if result:
            cls.obj         = obj   
            cls.obj_info    = obj.info
            print "Ok. -> ChildTree: %s; Selector: %s." %(cls.childtree,cls.uiselector)
        else:
            print "Warning: time out(%d).\nNot found object: ChildTree %s; Selector: %s.)" %(cls.timeout,cls.childtree,cls.uiselector)
            
        return result
    
    @classmethod
    def __get_element(cls):
        # 通过对 UiSelector的处理，确保 能唯一识别到Element控件        
        # 使用 UiSelector创建 UiObject实例
        
        obj = p_env.MOBILE(**cls.uiselector)        
        
        # UiObject实例，如果存在多个的情况下，使用 index,确保识别到唯一Element控件
        if obj.count > 1:
            print "Found %d UiObject with %s. Index[%d] has be choosed." %(obj.count,cls.uiselector,cls.uiindex)
            obj = obj[cls.uiindex]
        
        # UiObject实例, 使用childtree，确保识别到唯一Element控件; 如:  cls.uiselector = {"resourceId":"sh.lilith.dgame.DK:id/bd_rl_title"}, cls.childtree = [0,1]
        for i in cls.childtree:            
            if not obj.exists:
                break
            obj = obj.child(instance = i)
        
        return obj
        
    
    @classmethod
    def __clean(cls):
        cls.obj = None
                     
    
class FuncThread(threading.Thread):
    def __init__(self, func, *params, **paramMap):
        threading.Thread.__init__(self)
        self.func = func
        self.params = params
        self.paramMap = paramMap
        self.rst = None
        self.finished = False
 
    def run(self):
        self.rst = self.func(*self.params, **self.paramMap)
        self.finished = True
 
    def getResult(self):
        return self.rst
 
    def isFinished(self):
        return self.finished
    
def doInThread(func, *params, **paramMap):
    t_setDaemon = None
    if 't_setDaemon' in paramMap:
        t_setDaemon = paramMap['t_setDaemon']
        del paramMap['t_setDaemon']
    ft = FuncThread(func, *params, **paramMap)
    if t_setDaemon != None:
        ft.setDaemon(t_setDaemon)
    ft.start()
    return ft

if __name__ == "__main__":
    PadDevice.Wakeup()
    PadDevice.Swipe(965,398,1132,398,steps=50);#屏幕解锁
    # import os
    #     os.popen("adb shell am start com.tianwen.aischool/.ui.publics.login.LoginActivity")
    PadDevice.Shell("am","start","com.tianwen.aischool/.ui.publics.login.LoginActivity")
    
    PadUI.uiselector={"className" : "android.widget.EditText","instance" : 0}
    PadUI.SetText("bruceteacher")
    
    PadUI.uiselector={"className" : "android.widget.EditText","instance" : 1}
    PadUI.SetText("123456")
    
    PadUI.uiselector={"className" : "android.widget.Button"}
    PadUI.ClickAndwait()
    
    PadUI.uiselector={"text" : u"系统管理"}
    PadUI.ClickAndwait()
    
    PadUI.uiselector={"text" : u"安全退出"}
    PadUI.ClickAndwait()
    
    PadUI.uiselector={"text" : u"确定"}
    PadUI.ClickAndwait()
    
    
    
    
