# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.p_executer

Rough version history:
v1.0    Original version to use
v1.1    add 'launch_mobile' function
********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com    
    RCS:     rock4.common.p_executer,v 2.0 2017年2月7日
    FROM:   2015年5月11日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import re

class SimplifyExecuter:
    def __init__(self,module,debug = False):
        self.m = module
        self.debug = debug
        
    def call(self,func_string):
        '''
        return (result,err_msg)
        '''
        p  = re.compile("(?P<func>([\w]+)\()")        
        
        if not func_string or not isinstance(func_string, str) and not isinstance(func_string, unicode):            
            # 字符串  和 unicode，为有效功能函数字符串
            err_msg = "Invalid function: %s" %repr(func_string)
            return (None, err_msg)
        
        func_string = p.sub("%s.\g<func>" %"self.m",func_string)
        return self.__exec_string(func_string)

    def queue(self,func_string):
        '''
        return (result,err_msg)
        '''
                
        if not func_string or not isinstance(func_string, str) and not isinstance(func_string, unicode):            
            # 字符串  和 unicode，为有效功能函数字符串
            err_msg = "Invalid function: %s" %repr(func_string)
            return (None, err_msg)
        
        func_string = ("self.m" + "." + func_string)
        return self.__exec_string(func_string)
    
    def __exec_string(self,strs):
        '''
        return (result,err_msg)
        '''
        
        result = None
        err_msg = None
        
        if self.debug:
            print '--===>eval(%s)' %repr(strs)
            return (result, err_msg)
        
        try:
            result = eval(strs)
            if not result:
                result = True
        except NameError,e:            
            err_msg = "%s,Please check module funtion" %e
        except Exception,e:
            err_msg = e
        finally:
            return (result, err_msg)


import unittest
class TestEntrance(unittest.TestCase):
    def __init__(self,methodname="runTest", **kwargs):
        super(TestEntrance, self).__init__(methodName=methodname)
        self.params = kwargs
    
    @staticmethod
    def parametrize(test_sub_class, **kwargs):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(test_sub_class)
        
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(test_sub_class(name, **kwargs))
        return suite
    
    @staticmethod
    def go(casesuite, logfile=None, verbose=1):
        if logfile:
            with open(logfile, 'w') as f:
                unittest.TextTestRunner(stream=f, verbosity=verbose).run(casesuite)
        else:
            unittest.TextTestRunner(verbosity=verbose).run(casesuite)

def usage_forTestEntrance():
    class Ass(TestEntrance):
        
        def setUp(self):
            print "start ---"
            
        def tearDown(self):            
            print "end ---"
            
        def test_print(self):            
            print "hello unit test"
            print self.params
            
    suite = TestEntrance.parametrize(Ass, a=1, b=2)
    TestEntrance.go(suite)

def usage_forExecuter():
    
    from rock4 import common
    debug = True
    SimplifyExecuter(common, debug = debug).call('t()')
    SimplifyExecuter(common, debug = debug).call('tt(1,2)')
    SimplifyExecuter(common, debug = debug).call('ttt(1,2,3)')
    SimplifyExecuter(common, debug = debug).call('tttt(1,{2:3,3:4},[3,4])')
    SimplifyExecuter(common, debug = debug).call('ttttt(1,2,3,a=1,b=2,c=t())')
    SimplifyExecuter(common, debug = debug).queue('class.subclass.ttttt(1,2,3,a=1,b=2,c=t())')        
    
if __name__ == "__main__":
    usage_forExecuter()
#     usage_forTestEntrance()
    
    
    