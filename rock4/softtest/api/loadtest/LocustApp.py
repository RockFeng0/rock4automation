# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.loadtest.LocustApp

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.api.loadtest.LocustApp,v 2.0 2017年2月7日
    FROM:   2016年12月6日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
from LocustTemplate import LocustTemplate
from rock4.common import p_env
import requests
import os,sys,time,threading,subprocess

class LocustApp:
    def __init__(self,server_url="http://127.0.0.1:8089"):
        self.__server_url=server_url        
        self.script = os.path.join(p_env.BUFFER_PATH,"perfermance.py")
        self.status = None
    
    def start_exe(self,locust_count,hatch_rate,duration, host=None):
        ''' This function will start a subprocess for 'locust.exe' that run locust server   
            locust_count -并发多少用户
            hatch_rate -每秒发送多少次请求
        '''
        if subprocess.mswindows:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = 1
            startupinfo.wShowWindow = 0
            
        if host:
            self.__command = ["locust", "-H", host, "-f", self.script]
        else:
            self.__command = ["locust", "-f", self.script]
        # start server        
        self.__subp = subprocess.Popen(self.__command)
        
        # begin to run 
        head={"Content-Type": "application/x-www-form-urlencoded"}
        requests.post("%s/swarm" %self.__server_url, data="locust_count=%s&hatch_rate=%s" %(locust_count, hatch_rate),headers=head)
        
        st = time.time()
        while True:
            elapse = time.time() - st            
            print "just waiting(%s seconds)...%.2f" %(duration,elapse)            
            time.sleep(10)
            
            if elapse >= int(duration):
                break
            
        self.stop()
           
    def start_thd(self,locust_count,hatch_rate,duration, host=None):
        ''' This fuction will start a thread for locust.main.main() that run locust server with sys.argv parameter
            locust_count -并发多少用户
            hatch_rate -每秒发送多少次请求
        '''            
        
        # start server
        self.__thread = threading.Thread(target=self.__locust_server,args=[host])
        self.__thread.setDaemon(True)
        self.__thread.start()
        
        # begin to run 
        head={"Content-Type": "application/x-www-form-urlencoded"}
        requests.post("%s/swarm" %self.__server_url, data="locust_count=%s&hatch_rate=%s" %(locust_count, hatch_rate),headers=head)
        
        st = time.time()
        while True:
            elapse = time.time() - st            
            print "just waiting(%s seconds)...%.2f" %(duration,elapse)            
            time.sleep(10)
            
            if elapse >= int(duration):
                break
            
        self.stop()
        
    def stop(self):
        urls = {"stop":"%s/stop" %self.__server_url,
                "requests":"%s/stats/requests" %self.__server_url,
                "report_requests":"%s/stats/requests/csv" %self.__server_url,
                "report_exceptions":"%s/exceptions/csv" %self.__server_url,                
                "report_distribution":"%s/stats/distribution/csv" %self.__server_url,
                }
        
        try:
            # stop
            requests.get(urls["stop"])
            
            # status
            resp = requests.get(urls["requests"])
            self.status = resp.json()
            
            # save csv reports
            #self.__download_report(urls["report_requests"], name = "requests.csv")
            #self.__download_report(urls["report_exceptions"], name = "exceptions.csv")
            #self.__download_report(urls["report_distribution"] ,name = "distribution.csv")
                               
        except Exception,e:
            print e
        finally:
            #os.popen("taskkill /f /im locust.exe /t")
            print "Times up."
    
    def test_request(self,xlsfile=None,sheet=None):
        # in this test, make sure no filevar in your test xlsfile
        if not xlsfile:
            xlsfile = os.path.join(p_env.DATA_PATH,"locust_demo.xlsx")
            sheet = "Performance" 
        
        temp = LocustTemplate(xlsfile)
        temp.set_template(sheet=sheet)
        jobs = temp.get_jobs()
        
        for k,v in jobs:
            print "===test %s" %k
            d = v.split("/")[0]
            v_all = v.replace(d,d + temp.host)
            
            try:
                resp = eval("requests.%s" %v_all)
            except:
                print "invalid data: %s" %v
            else:
                try:
                    print resp.text
                except:
                    print resp.content
                print resp.status_code
                       
        
    def create_script(self,xlsfile=None,sheet=None,alias_name=True):
        if not xlsfile:
            xlsfile = os.path.join(p_env.DATA_PATH,"locust_demo.xlsx")
            sheet = "Performance"
            
        temp = LocustTemplate(xlsfile)
        temp.set_template(sheet=sheet, alias_name=alias_name)
        script = temp.get_template()
        
        with open(self.script,'w') as f:
            f.write(script)
    
    def __locust_server(self,host):
        # locust.main will make an Exception -> paramiko.ssh_exception.SSHException: Error reading SSH protocol banner
        # So self.start_exe is suggested to use instead of self.start_thd
        from locust import main
        if host:
            sys.argv[1:] = ["-H", host, "-f", self.script]
        else:
            sys.argv[1:] = ["-f", self.script]
        main.main()
        
    def __download_report(self,url, name=None):
        if name:
            f_name = name
        else:
            f_name = os.path.basename(url)
        resp = requests.get(url)
        f_abspath = os.path.join(p_env.BUFFER_PATH,f_name)                
        with open(f_abspath, 'wb') as fd:
            fd.write(resp.text.encode(resp.encoding))  

def demo_usage():
    from rock4.common import p_common    
    p_common.init_project_env("Test", debug=True)            
    r = LocustApp()    
    r.test_request()
#     r.create_script()
#     r.start("200", "10", "30")
    r.start(200, 10, 20)
    
    
if __name__ == "__main__":
    demo_usage()
    
    