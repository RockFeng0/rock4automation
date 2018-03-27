# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.pc.uiwpf.MuiaServer

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pc.uiwpf.MuiaServer,v 1.0 2017年3月28日
    FROM:   2017年3月28日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import time,os,threading,subprocess
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

class MuiaServer(object):    
    def __init__(self, uiwpfdriver_exe):
        p,f = os.path.split(uiwpfdriver_exe);os.chdir(p);self.command = [f]
                    
    def start_server(self):
        """start the Server.
        Doc note: Functionality within multiprocessing requires that the __main__ module be importable by the children.
        -简单说，就是要在  if __name__ == "__main__"中 调用该方法
        """
        freeze_support()
        p = Process(target=RunServer(self.command).start())
        p.start()
        time.sleep(5)   
        
    def stop_server(self):
        """stop the Server
        :return:
        """
        os.popen('taskkill /f /im  uiwpfdriver.exe*').close()
                                
    def re_start_server(self):
        """reStart the selenium Remote server
        """
        self.stop_server()
        self.start_server()
    
if __name__ == "__main__":
    wpf = MuiaServer(r'D:\auto\python\delegation\rock4\softtest\support\wpfdriver\uiwpfdriver.exe')
    wpf.start_server()
    time.sleep(3)
    wpf.stop_server()