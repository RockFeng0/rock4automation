# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.pc.uiwpf.TestDriver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pc.uiwpf.TestDriver,v 1.0 2017年3月20日
    FROM:   2017年3月20日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
from MuiaServer import MuiaServer
import subprocess,os,base64,json,time,socket
from rock4.softtest.support import utilities
from rock4.common import p_common

WPF_ACTIONS = ['Check', 'CheckOff', 'CheckOn', 'ClickWin', 'CloseWin', 'ExpandOff', 'ExpandOn', 'GetTextDocumentAttribute', 'SwitchToWindow', 'SwitchToDefaultWindow', 'ScrollTo', 'SelectItem', 'SetWinStat', 'StartApplication', 'TimeSleep', 'TypeInWin', 'SetVar']
WPF_PROPERTIES = ['AcceleratorKey', 'AccessKey', 'AutomationId', 'BoundingRectangle','ClassName', 'ClickablePoint', 'ControlType', 'Culture', 'HasKeyboardFocus',
               'HelpText', 'IsContentElement', 'IsControlElement', 'IsEnabled', 'IsExists', 'IsKeyboardFocusable', 'IsOffscreen', 'IsPassword', 'LabeledBy', 'LocalizedControlType', 'Name', 'ProcessId', 'RuntimeId']
MOUSE_ACTIONS = ["MouseMove", "MousePressButton", "MouseClick", "MouseDoubleClick", "MouseDrag", "MouseDragTo"]

class Req(object):
    def resolve(self,b64str):
        return json.loads(base64.b64decode(b64str))
    
    def crypt(self,rawstr):
        return base64.b64encode(json.dumps(rawstr))
    
class ReqServer(Req):
    
    def __init__(self, driver_path):
        self.__winhandle = 0
        print "Starting wpf server..."
        self.__server = MuiaServer(driver_path)
        self.__server.start_server()       
        print "-"
        p_common.wait_for_connection(port = 5820)
        self.__sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__sock.connect(("127.0.0.1", 5820))                
     
    def send(self, action, *args, **kwargs):
        response = {"resp":{
                 "result":False,
                 "errmsg":"",
                 "globals":{}
                 }
            }
                
        if not action in WPF_ACTIONS + WPF_PROPERTIES + MOUSE_ACTIONS:
            raise Exception("Invalide action '%s'" %action)
        
        index = int(kwargs.pop("index", 0))
        timeout = int(kwargs.pop("timeout", 10))
        
        req = {"req":{
                 "action": action,
                 "args": args,
                 "kwargs":{"identifications":kwargs, "index":index, "timeout":timeout, "CURRENT_HANDLE":self.__winhandle},
                 }
            }   
        resp = self.__get_response(self.crypt(req))
        if resp:
            response.update(resp)
            self.__winhandle = resp["resp"]["globals"]["CURRENT_HANDLE"]            
        return response
    
    def stop(self):
        self.__server.stop_server()
        
    def __get_response(self, b64req):
        ## send b64request to server 127.0.0.1:5820        
        self.__send_end(self.__sock, b64req)
        response=self.resolve(self.__recv_end(self.__sock))
        return response
    
    def __recv_end(self,the_socket):
        End = base64.b64encode("RockEND")    
        total_data=[];data=''
        while True:
                data=the_socket.recv(8192)
                if End in data:
                    total_data.append(data[:data.find(End)])
                    break
                total_data.append(data)
                if len(total_data)>1:
                    #check if end_of_data was split
                    last_pair=total_data[-2]+total_data[-1]
                    if End in last_pair:
                        total_data[-2]=last_pair[:last_pair.find(End)]
                        total_data.pop()
                        break
                if not data:
                    break
        return ''.join(total_data)

    def __send_end(self,sock, b64str):
        End = base64.b64encode("RockEND")
        sock.sendall(b64str+End)
        
class ReqCmd(Req):
    def __init__(self, driver_path):
        self.driver = driver_path
        self.is_winform = False
        self.__winhandle = 0
    
    def send(self, action, *args, **kwargs):
        response = {"resp":{
                 "result":False,
                 "errmsg":"",
                 "globals":{}
                 }
            }
                
        if not action in WPF_ACTIONS + WPF_PROPERTIES + MOUSE_ACTIONS:
            raise Exception("Invalide action '%s'" %action)
        
        index = int(kwargs.pop("index", 0))
        timeout = int(kwargs.pop("timeout", 10))
        
        req = {"req":{
                 "action": action,
                 "args": args,
                 "kwargs":{"identifications":kwargs, "index":index, "timeout":timeout, "CURRENT_HANDLE":self.__winhandle},
                 }
            }        
        os.chdir(os.path.dirname(self.driver))        
        resp = self.__get_response([self.driver, self.crypt(req)])
        if resp:
            response.update(resp)
            self.__winhandle = resp["resp"]["globals"]["CURRENT_HANDLE"]            
        return response
    
    def stop(self):
        pass
        
    def __get_response(self, cmd):
        subp = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)        
        result_code = 1
        result = None
        timeout_set = False
        while True:
            if not subp.poll()==None and result_code == 1:
                #进程已结束，仍然没有得到结果，超时30秒                          
                if not timeout_set:
                    print 'listen response. just waiting 15 seconds...'
                    time_now = time.time() + 15
                    timeout_set = True
                
                if time.time() >= time_now:
                    print 'listen response timeout at 15 seconds.'
                    break
            
            next_line = subp.stdout.readline().decode('cp936')           
    
            if next_line:
                print next_line 
                if "TestResultForWpfAction->" in str(next_line):
                    result = next_line.split("TestResultForWpfAction->")[-1]
    #                     result = next_line.replace("TestResultForCurrentCase->","")
                    result_code = 0                    
                    break
                else:                    
                    result_code = 1
        
        if subp.returncode:
            result_code = 1
            
        if result_code == 0:            
            return self.resolve(result)
        
                
class TestDriver:
    def __init__(self):
        self.driver = utilities.get_wpfdriver_path()
        if not self.driver:
            raise Exception("Can't find uiwpfdriver.exe")
                
    def find_driver(self):
#         return ReqCmd(self.driver)
        return ReqServer(self.driver)
    
    def find_drivers(self):
#         return {"loacalpcdriver":ReqCmd(self.driver)} 
        return {"loacalpcdriver":ReqServer(self.driver)}
    
    def run_model_case(self,callable_function):
        drivers = self.find_drivers()
        map(callable_function, drivers.items())  

def simple_usage1():
    test = TestDriver()
    driver = test.find_driver()
    print driver.send("StartApplication",r'D:\auto\pc_install\npp.5.7.Installer.exe')
    print "---"
    driver.send("MouseDragTo", 400, 400, AutomationId = "TitleBar")
    time.sleep(1)
    
    print driver.send("MouseMove", 1056, 574)    
    print driver.send("ClickablePoint",Name = "Cancel")
    print "---"
    
    print driver.send("ClickWin",Name = "OK")
    print driver.send("SwitchToWindow","Notepad++ v5.7 安装")    
    print driver.send("ClickWin",Name = u"下一步(N) >")
    print driver.send("ClickWin",Name = u"我接受(I)")
    print driver.send("TypeInWin", ur"d:\hello input", AutomationId = "1019")
    print driver.send("ClickWin",Name = u"下一步(N) >")
    print driver.send("ClickWin",Name = u"取消(C)")
    print driver.send("SwitchToDefaultWindow")  
    print driver.send("MouseClick",Name = u"是(Y)")
    driver.stop()

if __name__ == "__main__":
    simple_usage1()
    