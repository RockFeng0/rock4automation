# -*- encoding: utf-8 -*-
'''
Current module: mobile.monkeyrunner.driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pad.hierarchy.driver,v 2.0 2017年2月7日
    FROM:   2015年12月23日
********************************************************************

======================================================================

Android UI automation frame for python.
Jython-monkeyrunner--need use jython to compileall
monkeyrunner.jar & chimpchat.jar & hierarchyviewer2lib.jar
'''


from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice
from com.android.monkeyrunner.easy import By,EasyMonkeyDevice
from com.android.chimpchat.hierarchyviewer import HierarchyViewer
import os,re,time
import p_m_env


class MobileApp():
    ''' Mobile App Test.(need MonkeyRunner + Hierarchy)'''
    @classmethod
    def WaitForConnection(cls):
        print """
        
Connecting the device...

Please check blow, if without an connection in long time:

1. USB-debug model is enabled

2. Device driver is installed

"""
        p_m_env.DEVICE = MonkeyRunner.waitForConnection();#命令:  adb wait-for-device
        print "connect ok"
        p_m_env.EASY_DEVICE = EasyMonkeyDevice(p_m_env.DEVICE)
        print "connect easy ok"
        p_m_env.HIERARCHY = p_m_env.DEVICE.getHierarchyViewer()
        print "connect hierarchy ok"            
    
    @classmethod
    def LaunchApp(cls,app_component):
        # sample: app_component = com.mytest.aischool/.ui.publics.login.LoginActivity
        # adb shell am start -W -n com.tianwen.aischool/.ui.publics.login.LoginActivity    
        getattr(p_m_env.DEVICE,"startActivity")(component=app_component)
        time.sleep(0.5)
    
    @classmethod
    def CloseApp(cls,app_package):
        ''' only close app . keep the session'''        
        result = re.search(".*%s\r\n" %app_package,os.popen("adb shell ps").read())
        if result:
            pid = re.findall("\w+",result.group())[1]
            f=open("tmp",'w')
            f.write("su\r\nkill -9 %s\r\nexit\r\nexit\r\n" %pid)
            f.close()    
            os.system("adb shell <tmp")
            os.remove("tmp")
            
    @classmethod
    def IsAppInstalled(cls,app_package):
        '''
        app_package
        app_component
        apk_path        
        '''
        if re.search(app_package,os.popen("adb shell pm list packages").read()):
            result = True
        else:
            result = False
        time.sleep(0.5)
        return result

    @classmethod
    def InstallApp(cls,apk_path):
        ''' install the app to mobile
        apk_path=r"c:\test.apk"        
        '''
        getattr(p_m_env.DEVICE,"installPackage")(apk_path)
        time.sleep(0.5)
            
    @classmethod
    def RemoveApp(cls,app_package):
        # sample: app_package = com.mytest.testschool
        # adb uninstall com.mytest.testschool
        getattr(p_m_env.DEVICE,"removePackage")(app_package)
        time.sleep(0.5)
    
    @classmethod
    def Click(cls,x,y):
        p_m_env.DEVICE.touch(x,y,MonkeyDevice.DOWN_AND_UP)
    
    @classmethod
    def TypeRaw(cls,msg):
        p_m_env.DEVICE.type(msg)
    
    @classmethod
    def WaitSecond(cls,sec):
        MonkeyRunner.sleep(sec)
    
    @classmethod
    def ShotScreen(cls,file_path):
        p_m_env.DEVICE.takeSnapshot().writeToFile(file_path,'png')
             
    @classmethod
    def Enter(cls):
        cls.Keyevent("KEYCODE_ENTER")
        
    @classmethod
    def GetCurrentActivity(cls):
        return getattr(p_m_env.HIERARCHY,"getFocusedWindowName")()        
        
    @classmethod
    def Keyevent(cls,key_code_name):
        #adb shell input keyevent KEYCODE_HOME
        getattr(p_m_env.DEVICE,"press")(key_code_name,MonkeyDevice.DOWN_AND_UP)
            
    @classmethod
    def Back(cls):
        cls.Keyevent("KEYCODE_BACK")
    
    @classmethod
    def Menu(cls):
        cls.Keyevent("KEYCODE_MENU")
    
    @classmethod
    def Home(cls):
        cls.Keyevent("KEYCODE_HOME")
        
    @classmethod
    def Tab(cls):
        cls.Keyevent("KEYCODE_TAB")
    
    @classmethod
    def PageSwapUP(cls):
        cls.Keyevent(92);# KEYCODE_PAGE_UP
    
    @classmethod
    def PageSwapDOWN(cls):
        cls.Keyevent(93);# KEYCODE_PAGE_DOWN
        
    @classmethod
    def CursorUP(cls):
        cls.Keyevent(19);# KEYCODE_DPAD_UP
    
    @classmethod
    def CursorDOWN(cls):
        cls.Keyevent(20);# KEYCODE_DPAD_DOWN
    
    @classmethod
    def CursorLEFT(cls):
        cls.Keyevent(21);# KEYCODE_DPAD_LEFT
        
    @classmethod
    def CursorRIGHT(cls):
        cls.Keyevent(22);# KEYCODE_DPAD_RIGHT
    
    @classmethod
    def CursorMoveToHOME(cls):
        cls.Keyevent(122);# KEYCODE_MOVE_HOME
    
    @classmethod
    def CursorMoveToEND(cls):
        cls.Keyevent(123);# KEYCODE_MOVE_END   
         
    @classmethod
    def selectCurrentCursor(cls):
        cls.Keyevent(23);# KEYCODE_DPAD_CENTER
                

class MobileElement():    
    ''' Mobile App Element Test.(need MonkeyRunner + Hierarchy)'''
    (by,value,parent,timeout) = (None,None,None,30)
    
    @classmethod
    def Touch(cls):
        if cls.by == "position":
            if not isinstance(cls.value, list):
                raise Exception("Need list type:",cls.value)
            p_m_env.DEVICE.touch(cls.value[0],cls.value[1],MonkeyDevice.DOWN_AND_UP)
        else:
            point = cls.GetElementCenterPoint()            
            p_m_env.DEVICE.touch(point.x,point.y,MonkeyDevice.DOWN_AND_UP)
    
    @classmethod
    def LongTouch(cls):
        if cls.by == "position":
            if not isinstance(cls.value, list):
                raise Exception("Need list type:",cls.value)
            getattr(p_m_env.DEVICE,"drag'")((cls.value[0],cls.value[1]),(cls.value[0],cls.value[1]),1,3)
        else:
            point = cls.GetElementCenterPoint()
            getattr(p_m_env.DEVICE,"drag'")((point.x,point.y),(point.x,point.y),0.5,10)
    
    @classmethod
    def Swipe(cls,duration=2,steps=100):
        ''' 模拟用户滑动
            cls.by = "positon"
            cls.value = [100,100,200,200]
            duration --> 设置拖动过程的耗时
            steps    --> 设置拖动过程的步长， 步长较短的话，效果就是长按
        '''
        if cls.by == "position":
            if not isinstance(cls.value, list):
                raise Exception("Need list type:",cls.value)
            getattr(p_m_env.DEVICE,"drag'")((cls.value[0],cls.value[1]),(cls.value[2],cls.value[3]),duration,steps)

    @classmethod
    def SwipeToObj(cls,dest_obj,duration=2,steps=3):        
        if cls.by == "position":
            if not isinstance(cls.value, list):
                raise Exception("Need list type:",cls.value)
            src_xy = [cls.value[0], cls.value[0]]
        else:
            point1 = cls.GetElementCenterPoint()
            src_xy = [point1.x, point1.y]
            
        if dest_obj.by == "positon":
            if not isinstance(dest_obj.value, list):
                raise Exception("Need list type:",cls.value)
            dest_xy = [dest_obj.value[0], dest_obj.value[0]]            
        else:
            point2 = dest_obj.GetElementCenterPoint()
            dest_xy = [point2.x, point2.y]
            
        getattr(p_m_env.DEVICE,"drag'")((src_xy[0],src_xy[1]),(dest_xy[0],dest_xy[1]),duration,steps)
        
    @classmethod
    def Type(cls, msg):
        if msg == "":
            return
        
        if msg == "SET_EMPTY":
            msg = ""
                
        cls.Touch()
        p_m_env.DEVICE.type(msg)
    
    @classmethod
    def TypeInClear(cls, msg):
        if msg == "":
            return
        
        if msg == "SET_EMPTY":
            msg = ""
                
        cls.Touch()
        text = cls.GetText()
        for i in range(len(text)):
            p_m_env.DEVICE.press('KEYCODE_DEL', MonkeyDevice.DOWN_AND_UP)
            p_m_env.DEVICE.press('KEYCODE_FORWARD_DEL', MonkeyDevice.DOWN_AND_UP)
        p_m_env.DEVICE.type(msg)
                    
    @classmethod
    def SendEnter(cls):
        getattr(p_m_env.DEVICE,"press")("KEYCODE_ENTER",MonkeyDevice.DOWN_AND_UP)    
    
    @classmethod
    def GetText(cls):
        view_node = cls.__get_view_node()        
        return p_m_env.HIERARCHY.getText(view_node).encode("utf-8")
     
    @classmethod
    def SaveCurrentImageToFile(cls,file_path):
        if not os.path.isdir(os.path.dirname(file_path)):
            raise Exception("invalid file: %s" %file_path)
        view_node = cls.__get_view_node()
        screen_snapshot = getattr(p_m_env.DEVICE,"takeSnapshot")()
        point = p_m_env.HIERARCHY.getAbsolutePositionOfView(view_node)
        
        sub_img = screen_snapshot.getSubImage((point.x,point.y,view_node.width,view_node.height))
        return sub_img.writeToFile(file_path)        
           
    @classmethod
    def GetFocusedWindowName(cls):
        return getattr(p_m_env.HIERARCHY,"getFocusedWindowName")()
    
    @classmethod
    def GetElementCenterPoint(cls):
        view_node = cls.__get_view_node()
        point = p_m_env.HIERARCHY.getAbsoluteCenterOfView(view_node)
        print "center of view:",point        
        return point
    
    @classmethod
    def GetElementRectPoint(cls):
        view_node = cls.__get_view_node()        
        point = p_m_env.HIERARCHY.getAbsolutePositionOfView(view_node)
        (left,top) = (point.x,point.y)        
        (right,bottom) = (point.x + view_node.width,point.y + view_node.height)
        return [(left,top),(right,bottom)]
    
    @classmethod
    def GetAttribute(cls, attr):
        view_node = cls.__get_view_node()
        return view_node.namedProperties
    
    @classmethod
    def IsExist(cls):
        if cls.__get_view_node():
            return True
        return False
    
    @classmethod
    def IsVisible(cls):
        view_node = cls.__get_view_node()
        if not view_node:
            return False
        return p_m_env.HIERARCHY.visible(view_node)  
              
    @classmethod
    def __getPropertyList(cls):
        return p_m_env.DEVICE.getPropertyList()
        
    @classmethod
    def __get_view_node(cls):
        view_node = None
        if cls.by == "id":
            view_node = cls.__find_element_by_id(cls.value)
        elif cls.by == "link_text":            
            view_node = cls.__find_element_by_link_text(cls.parent,cls.value)
        elif cls.by == "index":
            view_node = cls.__find_element_by_index(cls.parent,cls.value)
        
        return view_node
    
    @classmethod
    def __wait(cls,aid):
        # MonkeyRunner search element need id(parent id or self id)
        endtime = time.time() + cls.timeout
        while True:
            view_node = p_m_env.HIERARCHY.findViewById(aid)            
            if view_node:
#                 print "-->'%s' is OK" %aid
                return view_node
            elif time.time()>endtime:
#                 raise Exception("Timeout at %d seconds.Element(%s-%s-%s) not found." %(cls.timeout,cls.by,repr(cls.value),cls.parent))
                print "Warning: Timeout at %d seconds.Element(%s-%s-%s) not found." %(cls.timeout,cls.by,repr(cls.value),cls.parent)
                return
    
    @classmethod
    def __find_element_by_id(cls,aid):
        # Sample usage:
        #    node = __find_element_by_id("id/login_account_input")
                
        return cls.__wait(aid)
            
    @classmethod
    def __find_element_by_link_text(cls,root_id,strs):
        #Sample usage:
        #     u"科目"        --> u'\u79d1\u76ee'
        #    node=__find_element_by_link_text(id,u'\u79d1\u76ee')
        if not isinstance(strs,unicode):
            raise Exception("Need unicode string:",strs)    
        view_node = cls.__find_element_by_id(root_id)        
        return cls.__search_element(view_node,strs)
        
    @classmethod    
    def __find_element_by_index(cls,root_id,index_list):
        # sample usage:
        #    __find_element_by_index("id/grid",[0,0,1,0])
        if not isinstance(index_list,list):
            raise Exception("Need list type:",index_list)
        
        view_node = cls.__find_element_by_id(root_id)      
        return cls.__search_element(view_node,index_list)
            
    @classmethod
    def __search_element(cls,child_node,strs_or_list):
        if not child_node:
            return 
        
        # 依据index列表，返回节点
        if isinstance(strs_or_list, list):
            for i in strs_or_list:
                if child_node.children:
                    child_node = child_node.children[i]
                else:
                    return
            return child_node
        
        # 递归遍历,返回节点
        if "TextView" in child_node.name:
            mText = child_node.namedProperties.get("text:mText")            
            if mText and mText.value == strs_or_list:
                # print strs_or_list.encode("utf-8")
                # print mText.value.encode("utf-8")
                return child_node
        else:
            for child in child_node.children:
                result = cls.__search_element(child,strs_or_list)
                if result:
                    return result              
   

if __name__ == "__main__":
    # monkeyrunner driver.py
    #等待连接
    MobileApp.WaitForConnection()
    
    #登录的示例
    component = "com.tianwen.aischool/.ui.publics.login.LoginActivity"
    MobileApp.LaunchApp(component)
    print "launch app ok"
    
    # 截图
    MobileElement.by = "id"
    MobileElement.value = "id/login_user_img"    
    MobileElement.SaveCurrentImageToFile(r"d:\auto\buffer\test.png")
    print "Saving a picture to a file. ok"
    
    #用户名
    MobileElement.by = "id"
    MobileElement.value = "id/login_account_input";#使用android sdk中的工具-->hierarchyviewer.bat查看。还有一个辅助工具 uiautomatorviewer.bat    
    MobileElement.TypeInClear("brucestudent1")
    print "Typing username(brucestudent1) ok"
        
    #密码
    (MobileElement.by,MobileElement.value) = ("id","id/login_password_input")         
    MobileElement.TypeInClear("123456")
    print "Typing password(123456) ok"
        
    #登录按钮
    (MobileElement.by,MobileElement.value) = ("id","id/login_start_button")
    MobileElement.Touch()
    print "Tap login button ok"
    
    #验证信息
    (MobileElement.by,MobileElement.value) = ("id","id/login_error_tip_text")        
    result = MobileElement.GetText()
    print "verify login info"    
    print "-->",result
    if "正在登录" in result:
        print "Login Test Pass"
    else:
        print "Login Test Fail"
    
    # 点击 练习作业
    print "->click link_text"
    (MobileElement.by,MobileElement.value,MobileElement.parent,MobileElement.timeout) = ("link_text",u"练习作业","id/homepage_exercise",30)    
    MobileElement.Touch()
    print "Link_text is ok"
    
    # 点击 练习作业
    print "->click index"
    (MobileElement.by,MobileElement.value,MobileElement.parent) = ("index",[0,0,1,0],"id/grid")  
    MobileElement.Touch()
    print "Index is ok"
        
    
    
    
    
    
