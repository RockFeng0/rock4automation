# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.p_applog

Rough version history:
v1.0    Original version to use
v2.0    define some normal functions for this module which act as Log Center
********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com    
    RCS:      rock4.common.p_applog,v 2.0 2017年2月7日
    FROM:     2015年4月14日
********************************************************************
            
======================================================================

Provide a package for the log

'''

import os,logging

class AppLog():
    ''' record the logs with your preference  '''
    def __init__(self,logger_name,level = "debug",filename = None,hand2screen = False,strf = ""):
        '''Initial a AppLog instance.
        Sample usage:
            AppLog("bruce_luo")
        '''
        self.logger=self.__getAppLogger(logger_name)
        self.level_list=["NOTSET","DEBUG","INFO","WARNING","ERROR","CRITICAL"]
        
        if strf:
            self.format_str = strf
        else:
            self.format_str = '#%(asctime)s  %(filename)s[line:%(lineno)-4d] %(levelname)-8s:%(message)s'
        
        self.__set_basic_config(level.upper(), filename)
        if hand2screen:
            self.__handle2screen(level.upper())       
    
    def tolog(self,str_value,level = 'debug'):
        getattr(self.logger,level.lower())(str_value)
    
    def __set_format_str(self,strf):
        ''' define a format for logging . notice that you should use this after logging obj created if need
        Sample usage:
            test = AppLog()
            test.set_format_str(r'[line:%(lineno)-4d]#%(levelname)-8s: #%(filename)-20s->%(message)s')
            test.set_format_str(r'#%(asctime)s  %(filename)s[line:%(lineno)-4d] %(levelname)-8s:%(message)s')
        '''        
        self.format_str = strf
    
    def __set_basic_config(self,lev,filename=None):
        ''' Will not save log if filename is None
        Sample usage:
            set_basic_config("DEBUG","d:/auto/buffer/sample.log")
            set_basic_config("DEBUG","sample.log")
            set_basic_config("DEBUG")
        '''
        lev_up = lev.upper()        
        
        if filename:
            file_abs_path = os.path.abspath(os.path.dirname(filename))        
            if not os.path.isdir(file_abs_path):
                raise Exception("\n\tp_applog.py exception 1.0: invalid filename '%s'." %(filename))        
            
        if lev_up in self.level_list:
            logging.basicConfig(level=getattr(logging, lev_up),filename=filename,filemode='w',format=self.format_str)
        else:
            raise Exception("\n\tp_applog.py exception 1.1: invalid level '%s'." %(lev))
          
    def __handle2screen(self,lev):
        '''Call this function to output logs to screen. Only save log if not call this function
        Sample usage:
            handle2screen("INFO",False)
            handle2screen("INFO")
            handle2screen()
        '''
        if self.logger.handlers:
            return
        lev_up=lev.upper()
        
        if lev_up in self.level_list:
            self.console = logging.StreamHandler()
            self.console.setLevel(getattr(logging, lev_up)) 
        else:
            raise Exception("\n\tp_applog.py exception 2.0: invalid level '%s'." %(lev))      

        self.formatter = logging.Formatter(self.format_str)            
        self.console.setFormatter(self.formatter)
            
        self.logger.addHandler(self.console)
    
    def __getAppLogger(self,logger_name):
        '''return the named logger if it exists, creating it with the name if the logger not exists 
        Sample usage:
            getAppLogger("bruce_luo")
        '''        
        return logging.getLogger(logger_name)
    
def usage_Applog():
    log=AppLog("test",level = "info",filename = "D:/auto/buffer/test.log",hand2screen = True)
 
    log.tolog("debug msg")
    log.tolog("info msg",level = "info")
    log.tolog("warning msg",level = "warning")
    log.tolog("error msg",level = "error")
    log.tolog("critical msg",level = "critical")
                
if __name__=="__main__":
    usage_Applog()
    
    
