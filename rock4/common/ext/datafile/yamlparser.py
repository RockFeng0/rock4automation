# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.datafile.yamlparser

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      pyrunner.ext.datafile.yamlparser,v 1.0 2017年2月4日
    FROM:   2017年2月4日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import os,codecs
import yaml

class Yaml():       
    
            
    def load(self, stream, coding = "utf-8"):
        """ Load one section
        Parameter:
            steam --> a yaml file or yaml string
            coding --> yaml file's coding
        Usage:
            stream = u'''
- {case_id: 1001, element_info: id/login_account_input, find_type: id, operate_type: type,  test_intr: 用户名, text: admin}
- {case_id: 1002, element_info: id/login_password_input, find_type: id, operate_type: type,  test_intr: 密码, text: 123456}
- {case_id: 1003, element_info: id/login_error_tip_text, find_type: id, operate_type: click,  test_intr: 登录按钮}
'''
            print load(stream)
        """
        if not stream:
            return ()
        
        if os.path.isfile(stream):  
            return yaml.load(codecs.open(stream, 'rb',encoding = coding))
        else:
            return yaml.load(stream)
    
    def load_all(self,stream, coding = "utf-8"):
        """ Load more sections
        Parameter:
            steam --> a yaml file or yaml string
            coding --> yaml file's coding
        Usage:
            stream = u'''
- {case_id: 1001, element_info: id/login_account_input, find_type: id, operate_type: type,  test_intr: 用户名, text: admin}
- {case_id: 1002, element_info: id/login_password_input, find_type: id, operate_type: type,  test_intr: 密码, text: 123456}
- {case_id: 1003, element_info: id/login_error_tip_text, find_type: id, operate_type: click,  test_intr: 登录按钮}
---
- {case_id: 1001, element_info: id/login_account_input, find_type: id, operate_type: type,  test_intr: 用户名2, text: admin}
- {case_id: 1002, element_info: id/login_password_input, find_type: id, operate_type: type,  test_intr: 密码2, text: 123456}
- {case_id: 1003, element_info: id/login_error_tip_text, find_type: id, operate_type: click,  test_intr: 登录按钮2}
'''
            for i in load_all(stream): print i
        Return:
            iterator
        """
        if not stream:
            return ()
             
        if os.path.isfile(stream):
            return yaml.load_all(codecs.open(stream, 'rb', encoding = coding))
        else:
            return yaml.load_all(stream)
    
    def dump(self,data,yamlfile):
        '''Dump one section
        Usage:
            y = Yaml()
            a={"a":1,"b":2,"c":y}
            yamlfile = r'd:\auto\buffer\t1.tmp'
            y.dump(a, yamlfile)        
        '''
        with codecs.open(yamlfile,'wb') as f:            
            try:
                yaml.dump(data, stream=f)
            except:
                pass
    
    def dump_all(self,data,yamlfile):
        '''Dump more section
        Parameter:
            data --> sequence of dict or iterator
            yamlfile --> save to yaml file
        Usage:
            y = Yaml()
            a=[{"a":1,"b":2,"c":y},{"a":3,"b":4,"c":y}]
            yamlfile = r'd:\auto\buffer\t1.tmp'
            y.dump_all(a, yamlfile)
        '''
        with codecs.open(yamlfile,'wb') as f:            
            try:
                yaml.dump_all(data, stream=f)
            except:
                pass
            
if __name__ == "__main__":
    
    y = Yaml()
    a=[{"a":1,"b":2,"c":y},{"a":3,"b":4,"c":y}]
    yamlfile = r'd:\auto\buffer\t1.tmp'
    y.dump_all(a, yamlfile)