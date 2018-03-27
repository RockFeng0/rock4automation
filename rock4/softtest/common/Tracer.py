# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.common.Tracer

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.common.Tracer,v 1.0 2017年2月18日
    FROM:   2017年2月18日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import os
from rock4.common import p_env
from rock4.common.p_log import CaseLog
from rock4.common.p_applog import AppLog 

class Tracer(CaseLog):
    def __init__(self, case_result_path = None, sys_log_path = None, device_id="", module_name = ""): 
        ''' Parameter
                case_result_path:  测试日志路径
                sys_log_path    系统日志路径
                device_id:    用于标识测试结果的唯一性
                module_name:    用于标识测试结果的名称
        '''       
        super(Tracer, self).__init__(case_result_path, device_id, module_name)
        
        if sys_log_path:
            p_env.BUFFER_PATH = sys_log_path
                    
        if not os.path.isdir(p_env.BUFFER_PATH):
            raise Exception("Project do not have a sys log path.")
        
        
    def __call__(self,name, screen_log = False):
        traces_file = os.path.join(p_env.BUFFER_PATH, name+".log")
        
        screen_log = False
              
        return AppLog(name,filename = traces_file,hand2screen=screen_log)
            
    def start(self,case_name):
        self.start_test(case_name)
                
    def section(self,strs):        
        self.step_info("section", self.__deal_str(strs))    
    
    def normal(self,strs):        
        self.step_info("normal", self.__deal_str(strs))
    
    def step(self,strs):
        self.step_info("step", self.__deal_str(strs))
    
    def ok(self,strs):
        self.step_info("pass", self.__deal_str(strs))
    
    def fail(self,strs):
        self.step_info("fail", self.__deal_str(strs))
    
    def error(self,strs):
        self.step_info("error", self.__deal_str(strs))
    
    def stop(self,titles_sequnce=["CaseName","Status","RespTester","Tester","ExecDate","ExecTime"],**kwargs):
        self.stop_test(titles_sequnce, **kwargs)
    
    def __deal_str(self,strs):
        if isinstance(strs, str):
            try:
                return strs.decode("utf-8")
            except:
                pass
        return strs
        
    
def usage_forTracer():    
    t = Tracer(case_result_path=r'D:\auto\buffer\testProject\result',sys_log_path=r'D:\auto\buffer\testProject\buffer')
    
    # 执行日志
    t.start("case1")    
    t.section("场景1")
    t.normal("网络信号状态测试")
    t.step("执行 步骤一")    
    t.ok("信号满载")
    t.fail("信号老差了")
    t.error("网络大姨妈来了")
    t.stop()
    print "Test End"
    
    #系统记录
    # level: -> debug info warning error critical
    t("traces",True).tolog("默认的调试信息")
    t("traces",True).tolog("靠，又一个小错误",level = "error")
    t("traces",True).tolog("尼玛 报了严重的错误",level = "critical")
    print "Log end"   
    
    
if __name__ == "__main__":
    usage_forTracer()    
        