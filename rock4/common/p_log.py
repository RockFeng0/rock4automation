# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.log

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com    
    RCS:      rock4.common.p_log,v 2.0 2017年2月7日
    FROM:   2015年5月13日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import os,sys,time,codecs
import p_env,p_common,p_report

class CaseLog(object):
    def __init__(self,case_result_path=None, device_id="", module_name = ""):        
        if case_result_path:
            p_env.RST_PATH = case_result_path
                    
        if not p_env.RST_PATH:
            raise Exception("Project do not have a case result path.")        
        
        if not os.path.basename(p_env.RST_PATH):
            p_env.RST_PATH = os.path.dirname(case_result_path) 
        
        p_env.MODULE_NAME = "result"
        if device_id and module_name:
            report_TestSet = device_id + "_" + module_name
        else:
            report_TestSet = device_id + module_name        
        
        if report_TestSet:
            p_env.MODULE_NAME = report_TestSet                
                
        if p_env.MODULE_NAME != "result":
            p_env.RST_PATH = p_env.RST_PATH +"-"+ p_env.MODULE_NAME
            
        p_env.RST_CASE_LOG_PATH = os.path.join(p_env.RST_PATH,"testcase")
        p_env.RST_SCR_SHOT_PATH = os.path.join(p_env.RST_PATH,"screenshots")
    
    def start_test(self,case_name):        
        p_env.CASE_NAME = case_name
        p_env.CASE_START_TIME = time.time()
        p_env.CASE_PASS = True
                
        if p_env.MODULE_START_TIME == "":
            p_env.MODULE_START_TIME = p_env.CASE_START_TIME
            print "Test start# ",p_env.MODULE_START_TIME      
        
        p_common.mkdirs(p_env.RST_CASE_LOG_PATH)
        p_common.mkdirs(p_env.RST_SCR_SHOT_PATH)
        
        log_file = self.__get_log_file()
        with codecs.open(log_file, "a", "utf-8") as f:
            f.write(u"\n**************  %s [%s]  ***************\n" %(u"Bruce Luo(罗科峰)'s sample test",p_env.CASE_NAME))
    
    def stop_test(self, titles_sequnce=["CaseName","Status","RespTester","Tester","ExecDate","ExecTime"],**kwargs):
        '''
        :param titles_sequnce: 报告的title的顺序,其中("CaseName","Status","ExecDate","ExecTime")4个title是默认生产的
        :param kwargs: 定义非默认 title的值，如 Tester = u"张三",RespTester = u'李四'
        '''
        p_env.MODULE_STOP_TIME = p_env.CASE_STOP_TIME = time.time()
        
        result = "Fail"
        duration_time = float("%.2f" %(p_env.CASE_STOP_TIME - p_env.CASE_START_TIME))
        summary_file = os.path.join(p_env.RST_PATH,"summary.log")
        with codecs.open(summary_file, "a", "utf-8") as f:
            if p_env.CASE_PASS == True:
                result = "Pass"             
            f.write(u"%-20s\t测试结果[%4s]\t用时[%s seconds]\t用例[%s]\n" %(p_common.get_stamp_datetime(),result,duration_time,p_env.CASE_NAME))        
        
        self.__generate_report(titles_sequnce,result,**kwargs)        
        # Reset
        p_env.CASE_PASS = True
    
    def step_info(self, info, msg):
        
        if isinstance(msg, str):
            try:
                unicode_msg = msg.decode('utf-8')
            except:
                raise Exception("Log message not unicode or utf-8.")
        else:
            unicode_msg = msg
        
        info = info.upper()
        log_file = self.__get_log_file()
        with codecs.open(log_file, "a", "utf-8") as f:
            if info == "SECTION":      
                f.write(u"\n%-20s\t%-10s\t%s\n" %(p_common.get_stamp_datetime_coherent(),info, unicode_msg))
            elif info in ["NORMAL","STEP","PASS"]:
                f.write(u"%-20s\t%-10s\t%s\n" %(p_common.get_stamp_datetime_coherent(),info,unicode_msg))
            elif info in ["ERROR","FAIL"]:
                f.write(u"%-20s\t%-10s\t%s\n" %(p_common.get_stamp_datetime_coherent(),info,unicode_msg))
#                 if screenshot:
#                     screenshot_name = "%s__%s__Fail__%s.png" % (p_env.CASE_NAME, p_env.RUNNING_BROWSER, p_common.get_stamp_datetime_coherent())
#                     screenshow_file = os.path.join(p_env.RST_SCR_SHOT_PATH, screenshot_name)
#                     getattr(p_env.BROWSER, "save_screenshot")(screenshow_file)            
                p_env.CASE_PASS = False 
    
    def handle_error(self):
        ''' handle the detail error if have get the exception
        Sample usage:
            try:
                1/0
            except:
                handle_error()
        '''
        if p_env.CASE_PASS == False:
            return
        screenshot_name = "%s__%s__Fail__%s.png" % (p_env.CASE_NAME, p_env.RUNNING_BROWSER, p_common.get_stamp_datetime_coherent())
                
        if sys.exc_info()[0] != None:                
            self.step_info("normal",p_common.get_exception_error())        
            p_common.mkdirs(p_env.RST_SCR_SHOT_PATH)                      
            self.step_info("normal","Please check screen short [%s]" % (screenshot_name))           
            
            p_env.CASE_PASS = False
    
    def __generate_report(self,titles_sequnce, result, **kwargs):
        for title in titles_sequnce:
            if title in ("CaseName","Status","ExecDate","ExecTime"):
                continue
            elif not title in kwargs:
                kwargs[title] = ''
                
        p_report.add_report_data(p_env.REPORT_DATA, p_env.MODULE_NAME, p_env.CASE_NAME, result, **kwargs)    
        p_report.generate_result_html(titles_sequnce)
    
    def __get_log_file(self):        
        log_file_name = "%s_%s.log" %(p_env.CASE_NAME, p_common.get_stamp_date())
        return os.path.join(p_env.RST_CASE_LOG_PATH,log_file_name)


def simple_usage1():    
    _caselogobj = CaseLog(r'D:\auto\buffer\testProject\result');# report is D:\auto\buffer\testProject\result\result.html
#     _caselogobj = CaseLog(r'D:\auto\buffer\testProject\result',device_id="Android1");# report is D:\auto\buffer\testProject\result-Android1\result.html
#     _caselogobj = CaseLog(r'D:\auto\buffer\testProject\result',module_name = "Test1");# report is D:\auto\buffer\testProject\result-Test1\result.html
#     _caselogobj = CaseLog(r'D:\auto\buffer\testProject\result',device_id="Android1", module_name = "Test1");# report is D:\auto\buffer\testProject\result-Android1_Test1\result.html
    
    start_test = _caselogobj.start_test
    stop_test = _caselogobj.stop_test
    step_info = _caselogobj.step_info
    handle_error = _caselogobj.handle_error

    start_test("ATest");# report is result.html
    step_info("section","A test")
    step_info("normal","Step1: good")
    step_info("pass","step2: pass")
    
    step_info("section","A test2")
    step_info("normal","Step1: good")
    try:
        raise Exception("asdfsdfsdf")
    except Exception,e:
        handle_error();#用这个的话，那么就是详细的错误信息        
        step_info("error",e)
    
    step_info("section","A test3")
    step_info("normal","Step1: good")
    step_info("step","Step2: good")
    step_info("fail","step3: fail")
    step_info("pass",u"中文 Unicode")
    step_info("pass","中文 utf-8")
        
    stop_test(RespTester = "bruce", Tester="bruce")
    
    start_test("ATest2");# report is result.html
    step_info("section","A test")
    step_info("normal","Step1: good")
    step_info("pass","step2: pass")
    
    step_info("section","A test2")
    step_info("normal","Step1: good")
    try:
        raise Exception("asdfsdfsdf")
    except Exception,e:
        handle_error();#用这个的话，那么就是详细的错误信息        
        step_info("error",e)
    
    step_info("section","A test3")
    step_info("normal","Step1: good")
    step_info("step","Step2: good")
    step_info("fail","step3: fail")
    step_info("pass",u"中文 Unicode")
    step_info("pass","中文 utf-8")
        
    stop_test(RespTester = "bruce", Tester="bruce")
    

def simple_usage2():
    p_common.init_project_env("usage", proj_path = r'D:\auto\buffer\testProject', initdirs=True)
    _caselogobj = CaseLog(); # report is D:\auto\buffer\testProject\result\result.html
    start_test = _caselogobj.start_test
    stop_test = _caselogobj.stop_test
    step_info = _caselogobj.step_info
    handle_error = _caselogobj.handle_error

    start_test("ATest")
    step_info("section","A test")
    step_info("normal","Step1: good")
    step_info("pass","step2: pass")
    
    step_info("section","A test2")
    step_info("normal","Step1: good")
    try:
        raise Exception("asdfsdfsdf")
    except Exception,e:
        handle_error();#用这个的话，那么就是详细的错误信息        
        step_info("error",e)
    
    step_info("section","A test3")
    step_info("normal","Step1: good")
    step_info("step","Step2: good")
    step_info("fail","step3: fail")
    step_info("pass",u"中文 Unicode")
    step_info("pass","中文 utf-8")
        
    stop_test(RespTester = "bruce", Tester="bruce")
    
if __name__ == "__main__":
    simple_usage1()
