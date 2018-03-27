# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.web.SeleniumJar

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.web.SeleniumJar,v 1.0 2017年2月27日
    FROM:   2017年2月27日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


import time,os,threading,urllib2,subprocess
from multiprocessing import Process,freeze_support

class RunServer(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
    def run(self):
        try:
            subprocess.call(self.cmd)
        except KeyboardInterrupt:
            pass

class SeleniumJar(object):    
    def __init__(self, server_jar_full_path, port = 4444, role=None, hub = "http://127.0.0.1:4444/grid/register/", java_exe_full_path = None):
        self.port = port        
        if not java_exe_full_path:
            java_exe_full_path = "java.exe"
            
        self.command = [java_exe_full_path, "-jar", server_jar_full_path, "-port", str(port)]
        if role == "hub":
            self.command.extend(["-role", "hub"])
        elif role == 'node':
            self.command.extend(["-role", "node", "-hub", hub])
            
    def start_server(self):
        """start the selenium Remote Server.
        Doc note: Functionality within multiprocessing requires that the __main__ module be importable by the children.
        -简单说，就是要在  if __name__ == "__main__"中 调用该方法
        """
        freeze_support()
        p = Process(target=RunServer(self.command).start())
        p.start()
        time.sleep(2)
        
    def stop_server(self):
        """stop the selenium Remote Server
        :return:
        """
        os.popen('taskkill /f /im  java.exe*').close()
                                
    def re_start_server(self):
        """reStart the selenium Remote server
        """
        self.stop_server()
        self.start_server()
    
    def is_runnnig(self, ip):
        """Determine whether server is running
        :return:True or False
        """
        response = None
        url = "http://%s:%s/wd/hub" %(ip, str(self.port))
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
                
class SeleniumHub(SeleniumJar):
    ''' Usage:
        hub = SeleniumHub(r'D:\auto\python\app-autoApp\demoProject\tools\selenium-server-standalone-3.0.1.jar')
        hub.start_server()
    '''         
    def __init__(self, server_jar_full_path, port = 4444, java_exe_full_path = None):        
        super(SeleniumHub, self).__init__(server_jar_full_path = server_jar_full_path, port = port, role="hub", java_exe_full_path = java_exe_full_path)
        # java -jar selenium-server.jar -role hub -port 4444
        
class SeleniumNode(SeleniumJar):
    ''' Usage:
        node = SeleniumNode(r'D:\auto\python\app-autoApp\demoProject\tools\selenium-server-standalone-3.0.1.jar', 5555, 'http://localhost:4444/grid/register')
        node.start_server()
    '''    
    def __init__(self, server_jar_full_path, port, hub, java_exe_full_path = None):
        super(SeleniumNode, self).__init__(server_jar_full_path = server_jar_full_path, port = port, role="node", hub = hub, java_exe_full_path = java_exe_full_path)
        # java -jar selenium-server.jar -role node -port 4444 -hub http://127.0.0.1:4444/grid/register/
        

if __name__ ==  "__main__":    
    hub = SeleniumHub(r'D:\auto\python\app-autoApp\demoProject\tools\selenium-server-standalone-3.0.1.jar')
    hub.start_server()
    
    node = SeleniumNode(r'D:\auto\python\app-autoApp\demoProject\tools\selenium-server-standalone-3.0.1.jar', 5555, 'http://localhost:4444/grid/register')
    node.start_server()
            