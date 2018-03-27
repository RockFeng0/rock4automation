# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.pc.uimfc.actions

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pc.uimfc.actions,v 1.0 2017年3月7日
    FROM:   2017年3月7日
********************************************************************

======================================================================

MFC UI automation frame for python.

'''


import os,time,subprocess
from rock4.common import p_env
from autoitpy.autoit import WinMFCDriver

p_env.WINMFC = WinMFCDriver()        
class MFCElement:
    '''Window MFC Elements'''
    (identifications, timeout)=({}, 10)
    __glob = {}
    
    ###  Parameterized
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
    
    ### Miscellaneous    
    @classmethod
    def StartAppliaction(cls, app_path):
        if not os.path.exists(app_path):
            raise Exception('Not found "%s"' %app_path)
#         os.system('cmd /c start %s' %app_path)
        subprocess.Popen([app_path])
        time.sleep(0.2)    
    
    @classmethod
    def SetTitleOpt(cls,mode=2):
        '''
        :param mode: 1 = Match the title from the start (default)
                    2 = Match any substring in the title
                    3 = Exact title match
                    4 = Advanced mode
        '''
        getattr(p_env.WINMFC,"invoke")("Opt","WinTitleMatchMode",int(mode))
    
    @classmethod
    def GetWinCount(cls):
        if not cls.__wait():
            return False
        win_list = getattr(p_env.WINMFC,"invoke")("WinList",cls.__title)
        win_list_count = win_list[0][0]        
        return win_list_count
        
    
    @classmethod
    def GetWinText(cls):
        if not cls.__wait():
            return False
        return getattr(p_env.WINMFC,"invoke")("ControlGetText",cls.__title,"",cls.__con)
    
    
    ### Mouse Control
    @classmethod
    def ClickXY(cls, x, y):
        getattr(p_env.WINMFC,"invoke")("MouseClick", "left", x, y, 1)
    
    @classmethod
    def RightClickXY(cls, x, y):
        getattr(p_env.WINMFC,"invoke")("MouseClick", "right", x, y, 1)
    
    @classmethod
    def ClickDrag(cls, x1, y1, x2, y2):
        getattr(p_env.WINMFC,"invoke")("MouseClickDrag", "left", x1, y1, x2, y2)
    
    @classmethod
    def ClickDoubleXY(cls, x, y):
        getattr(p_env.WINMFC,"invoke")("MouseClick", "left", x, y, 2)    
    
    @classmethod
    def MouseMove(cls, x, y):
        getattr(p_env.WINMFC,"invoke")("MouseMove",x, y)
    
    ### Windows
    @classmethod
    def FindAndActivateWin(cls):
        if not cls.__wait():
            return False
        
        if not cls.IsActiveWin():
            cls.ActivateWin()    
    
    @classmethod
    def ActivateWin(cls):
        if not cls.__wait():
            return False
        getattr(p_env.WINMFC,"invoke")("WinActivate",cls.__title)        
        
    @classmethod
    def KillWin(cls):
        if not cls.__wait():
            return False
        getattr(p_env.WINMFC,"invoke")("WinKill",cls.__title)
    
    @classmethod
    def CloseWin(cls):
        if not cls.__wait():
            return False
        getattr(p_env.WINMFC,"invoke")("WinClose",cls.__title)        
    
    ### Window Controls   
    @classmethod
    def TypeInWin(cls,value):
        if not cls.__wait():
            return False
        
        getattr(p_env.WINMFC,"invoke")("ControlSend",cls.__title,"",cls.__con,"{END}+{HOME}")
        time.sleep(0.2)        
        if getattr(p_env.WINMFC,"invoke")("ControlSend",cls.__title,"",cls.__con,value):
            return True
        else:
            return False
                
    
    @classmethod
    def ClickWin(cls):
        if not cls.__wait():
            return False        
        if getattr(p_env.WINMFC,"invoke")("ControlClick",cls.__title,"",cls.__con):
            return True
        else:
            return False        
            
    @classmethod
    def SelectItem(cls,value):
        #ListBox or ComboBox
        if not cls.__wait():
            return False
        getattr(p_env.WINMFC,"invoke")("ControlCommand",cls.__title,"",cls.__con,"SelectString",value)
            
    @classmethod
    def IsExistsWin(cls):
        if not cls.__wait():
            return False        
        if getattr(p_env.WINMFC,"invoke")("WinExists",cls.__title):
            return True
        return False        
                
    @classmethod
    def IsActiveWin(cls):
        if not cls.__wait():
            return False
        if getattr(p_env.WINMFC,"invoke")("WinActive",cls.__title):
            return True
        return False       
        
    @classmethod
    def __wait(cls):
        mfc_controls = ("id", "text", "class", "classnn", "name", "instance")        
        if not isinstance(cls.identifications, dict):
            try:
                identify = eval(cls.identifications)
            except:
                identify = None
            finally:
                if not isinstance(identify, dict):
                    raise Exception("Invalid format of Element: %s" %(cls.identifications))
                cls.identifications = identify
        
        ident = cls.identifications.copy()
                
        con = []
        for key, value in ident.items():
            low_key = key.lower()
            
            if isinstance(value, str):
                value = value.decode('utf-8')                
            
            if low_key == "title":
                ident.pop(key)
                cls.__title = value
                continue
            
            if not low_key in mfc_controls:
                raise Exception("identifications controls do not have '%s'." %key)
            con.append("%s:%s" %(key,value))
        
        if not cls.__title:
            raise Exception("identifications do not have 'title'.")            
        cls.__con = "["+ ";".join(con) + "]"
                  
        ret = getattr(p_env.WINMFC,"invoke")("WinWait",cls.__title,"",cls.timeout)
        if ret == 1:
            return True
        return False

def usage_mfc():
    # notepad++ installation example
    app_path = r"F:\BaiduYunDownload\pcinstall\npp.5.7.Installer.exe"
    MFCElement.StartAppliaction(app_path)    
    MFCElement.SetTitleOpt(2)
    MFCElement.identifications = {"Title" : "Installer Language"}
    MFCElement.ActivateWin()
    MFCElement.identifications = {"Title" : "Installer Language","text":"OK"}
    MFCElement.ClickWin()
    MFCElement.identifications = {"Title" : u"Notepad++ v5.7 安装","text":u"下一步(&N) >"}
    MFCElement.ClickWin()
    MFCElement.identifications = {"Title" : "Notepad++","text":u"我接受(&I)"}
    MFCElement.ClickWin()
    MFCElement.identifications = {"Title" : "Notepad++","ID":1019,"class":"Button"}
    MFCElement.TypeInWin(ur"d:\hello input")
    MFCElement.identifications = {"Title" : "Notepad++","text":u"下一步(&N) >"}
    MFCElement.ClickWin()
    MFCElement.identifications = {"Title" : "Notepad++","text":u"取消(&C)"}
    MFCElement.ClickWin()
    MFCElement.identifications = {"Title" : "Notepad++","id":6}
    MFCElement.ClickWin()
    
if __name__ == "__main__":
    usage_mfc()
    