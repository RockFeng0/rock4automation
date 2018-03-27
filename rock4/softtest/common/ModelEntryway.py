# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.common.ModelEntryway

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.common.ModelEntryway,v 1.0 2017年5月17日
    FROM:   2017年5月17日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import re,importlib
from Tracer import Tracer
from rock4.common import p_common,p_env

class ModelEntryway(object):
    ''' Usage:
        model_obj = ModelEntryway.Select("yaml", "pcmfc")
        model_obj = ModelEntryway.Select("excel", "web") 
    '''
    parent_model_class = None
            
    @classmethod
    def Select(cls, model, model_type):        
        m1 = {'yaml':("rock4.softtest.common.YamlModel","YamlModel"),
              'excel':("rock4.softtest.common.ExcelModel","ExcelModel"),
              }
        m2 = {'web':UiWeb,'pad':UiPad,'pcmfc':UiPcMfc,'pcwpf':UiPcWpf,'api':WebService}
        
        if not model.lower() in m1:
            errmsg = "Please select the test model in %r" %m1.keys()
            return (None,errmsg)
        
        if not model_type.lower() in m2:
            errmsg = "Please select the test model type in %r" %m2.keys()
            return (None,errmsg)
        
        module = m1.get(model.lower())
        cls.parent_model_class = getattr(importlib.import_module(module[0]), module[1])        
        return (m2.get(model_type.lower()),None)

class WebService(object):
    
    def __init__(self, model_file, parent_model_class):
        self.model_obj = parent_model_class(model_file)        
        self.Actions = importlib.import_module("rock4.softtest.api.webservice.irequests.actions")
        
    def apply_actions(self, devdriver, debug = False):
        
        ''' apply excel actions '''       
        
        tracer = Tracer()
        print "Device ready: %s" %devdriver[0]
        opration_class = self.Actions.WebHttp
        element_actions = p_common.get_callable_class_method_names(opration_class)
        
        case_steps = self.model_obj.translate()
        for case_name, execute_actions, idx in case_steps:
            print "##### Starting Test[%s]: %s" %(idx, case_name)
            tracer.start(case_name)
            tracer.section(case_name)
            
            for execute_function in execute_actions:
                try:
                    execute_function = self.__replace_var(execute_function)
                    
                    action = execute_function.split("(", 1)[0]
                    text = eval(execute_function.replace(action, "self.map_api_actions", 1))
                    
                    print "-->",action
                    if action in element_actions:
                        opration_class.head = None
                        if self.model_obj.testcases[idx]["head"]:                            
                            opration_class.head = self.__replace_var(self.model_obj.testcases[idx]["head"])
                        
                        opration_class.data = None
                        if self.model_obj.testcases[idx]["data"]:
                            opration_class.data = self.__replace_var(self.model_obj.testcases[idx]["data"])
                    else:
                        tracer.fail("Do not hava action:%s\t%s" %(action,execute_function))
                        continue                
                    
                    if text:                        
                        result = getattr(opration_class, action)(*text)
                    else:
                        result = getattr(opration_class, action)()
                    
                    if result == False:
                        tracer.fail(execute_function)
                    else:
                        tracer.ok(execute_function)
                        
                except Exception,e:
                    tracer.error("%s\t%s" %(e,execute_function))            
            tracer.stop(RespTester = "administrator", Tester = "administrator")
                                          
                                          
    def map_api_actions(self,*args, **kwargs):
        """
        :param args for the parameter, kwargs for features
        """
        text = kwargs.get("text",[])
        if args:
            text = args
        text = self.model_obj.getUnicodeArgs(*text) 
        return text
    
    def __replace_var(self, strs):        
        keys = re.findall('#(.*?)#', strs)        
        for key in keys:
            var = self.Actions.WebHttp.GetVar(key)
            strs = strs.replace('#' + key + '#', var)
        return strs
    
class UiWeb(object):
    def __init__(self, model_file, parent_model_class):
        self.model_obj = parent_model_class(model_file)
        self.Actions = importlib.import_module("rock4.softtest.web.actions")
    
    def apply_actions(self, devdriver, debug = False):
        ''' apply excel actions '''
        
        devid, p_env.BROWSER = devdriver[0], devdriver[1]
        if devid == "loacalwebdriver":
            tracer = Tracer()
        else:
            tracer = Tracer(device_id=p_common.get_legal_filename(devid))
        print "Device ready: %s" %devid        
        
        Actions = self.Actions
        browser_actions = p_common.get_callable_class_method_names(Actions.WebBrowser)            
        element_actions = p_common.get_callable_class_method_names(Actions.WebElement)
        
        case_steps = self.model_obj.translate()        
        for case_name, execute_actions, idx in case_steps:
            print "##### Starting Test[%s]: %s" %(idx, case_name)
            tracer.start(case_name)
            tracer.section(case_name)
            
            for execute_function in execute_actions: 
                try:
                    execute_function = self.__replace_var(execute_function)
                         
                    action = execute_function.split("(", 1)[0]                        
                    by, value, text, index, timeout = eval(execute_function.replace(action, "self.map_web_actions", 1))
            
                    if debug:
                        print  '\t',by,value,index,timeout,action,text
                        continue 
                    
                    print "-->",action
                    if action in element_actions:
                        opration_class = Actions.WebElement
                        opration_class.by, opration_class.value, opration_class.index, opration_class.timeout = by, value, index, timeout
                        
                    elif action in browser_actions:
                        opration_class = Actions.WebBrowser
                        
                    else:
                        tracer.fail("Do not hava action:%s\t%s" %(action,execute_function))
                        continue                
                    
                    if text:          
                        result = getattr(opration_class, action)(*text)
                    else:
                        result = getattr(opration_class, action)()
                    
                    if result == False:
                        tracer.fail(execute_function)
                    else:
                        tracer.ok(execute_function)
                        
                except Exception,e:
                    tracer.error("%s\t%s" %(e,execute_function))
            tracer.stop(RespTester = "administrator", Tester = "administrator")
                
    def map_web_actions(self,*args, **kwargs):
        """
        :param args for the parameter, kwargs for features
        """
        find_types = {'css': "CSS_SELECTOR", 'id':"ID", 'name':"NAME", 'class':"CLASS_NAME", 'tagname':"TAG_NAME", 'xpath':"XPATH", 'link':"LINK_TEXT", 'plink':"PARTIAL_LINK_TEXT"}
        [by, value, text, index, timeout] = [find_types.get(kwargs.get("by")), kwargs.get("value"), kwargs.get("text",[]), kwargs.get("index",0), kwargs.get("timeout",10)]
        if args:
            text = args
        text = self.model_obj.getUnicodeArgs(*text)            
        return [by, value, text, index, timeout]
    
    def __replace_var(self, strs):        
        keys = re.findall('#(.*?)#', strs)        
        for key in keys:
            var = self.Actions.WebElement.GetVar(key)
            strs = strs.replace('#' + key + '#', var)
        return strs
    
class UiPcMfc(object):
    def __init__(self, model_file, parent_model_class):
        self.model_obj = parent_model_class(model_file)
        self.Actions = importlib.import_module("rock4.softtest.pc.uimfc.actions")
    
    def apply_actions(self, devdriver, debug = False):
        ''' apply excel actions '''
        
        devid, p_env.WINMFC = devdriver[0], devdriver[1]
        tracer = Tracer()
        print "Device ready: %s" %devid
                
        Actions = self.Actions         
        element_actions = p_common.get_callable_class_method_names(Actions.MFCElement)
        
        case_steps = self.model_obj.translate()
        for case_name, execute_actions, idx in case_steps:
            print "##### Starting Test[%s]: %s" %(idx, case_name)
            tracer.start(case_name)
            tracer.section(case_name)
            
            for execute_function in execute_actions:
                try:
                    execute_function = self.__replace_var(execute_function)
                    
                    action = execute_function.split("(", 1)[0]                    
                    identifications, timeout, params = eval(execute_function.replace(action, "self.map_pc_actions", 1))
            
                    if debug:
                        print  '\t',identifications, timeout, params
                        continue 
                    
                    print "-->",action
                    if action in element_actions:
                        opration_class = Actions.MFCElement 
                        opration_class.identifications,opration_class.timeout = identifications, timeout
                    else:
                        tracer.fail("Do not hava action:%s\t%s" %(action,execute_function))
                        continue                
                    
                    if params:
                        result = getattr(opration_class, action)(*params)
                    else:
                        result = getattr(opration_class, action)()
                    
                    if result == False:
                        tracer.fail(execute_function)
                    else:
                        tracer.ok(execute_function)
                        
                except Exception,e:
                    tracer.error("%s\t%s" %(e,execute_function))
                                
            tracer.stop(RespTester = "administrator", Tester = "administrator")
            
    def map_pc_actions(self,*args, **kwargs):
        """
        :param args for the parameter, kwargs for features
        """        
        timeout, classname = kwargs.pop("timeout",10), kwargs.pop("classname",None)
        if classname:
            kwargs["class"] = classname        
        identifications = kwargs
        
        params = self.model_obj.getUnicodeArgs(*args)
         
        return [identifications, timeout, params]
    
    def __replace_var(self, strs):        
        keys = re.findall('#(.*?)#', strs)  
        for key in keys:
            var = self.Actions.MFCElement.GetVar(key)
            strs = strs.replace('#' + key + '#', var)
        return strs

class UiPcWpf(object):
    def __init__(self, model_file, parent_model_class):
        self.model_obj = parent_model_class(model_file)
        md = importlib.import_module("rock4.softtest.pc.uiwpf.TestDriver")
        self.__glob = {}
        self.element_actions = md.WPF_ACTIONS + md.WPF_PROPERTIES + md.MOUSE_ACTIONS
    
    def apply_actions(self, devdriver, debug = False):
        ''' apply excel actions '''
        
        devid, p_env.WINWPF = devdriver[0], devdriver[1]
        tracer = Tracer()
        print "Device ready: %s" %devid
        
        opration_class = devdriver[1]
        element_actions = self.element_actions
        
        case_steps = self.model_obj.translate()
        for case_name, execute_actions, idx in case_steps:
            print "##### Starting Test[%s]: %s" %(idx, case_name)
            tracer.start(case_name)
            tracer.section(case_name)
            
            for execute_function in execute_actions:
                try:
                    execute_function = self.__replace_var(execute_function)
                    
                    action = execute_function.split("(", 1)[0]                    
                    params, kwparams = eval(execute_function.replace(action, "self.map_pcwpf_actions", 1))
            
                    if debug:
                        print  '\t',params, kwparams
                        continue 
                    
                    print "-->",action
                    if not action in element_actions:                        
                        tracer.fail("Do not hava action:%s\t%s" %(action,execute_function))
                        continue
                    response = getattr(opration_class, "send")(action, *params, **kwparams)                                                    
                    result = response["resp"]["result"]
                    errmsg = response["resp"]["errmsg"]
                    print "result:%s, errmsg:%s" %(result,errmsg)
                    self.__glob.update(response["resp"]["globals"])
                    
                    if result == False:
                        errmsg = "%s\t%s" %(errmsg, execute_function) if errmsg else execute_function
                        tracer.fail(errmsg)
                    else:
                        tracer.ok(execute_function)                    
                except Exception,e:
                    tracer.error("%s\t%s" %(e,execute_function))            
            tracer.stop(RespTester = "administrator", Tester = "administrator")
        getattr(opration_class, "stop")()
            
    def map_pcwpf_actions(self,*args, **kwargs):
        """
        :param args for the parameter, kwargs for features
        """        
        params = self.model_obj.getUnicodeArgs(*args)
        return [params, kwargs]
    
    def __replace_var(self, strs):
        keys = re.findall('#(.*?)#', strs)  
        for key in keys:
            var = self.__glob.get(key)
            strs = strs.replace('#' + key + '#', var)
        return strs
    
class UiPad(object):
    def __init__(self, model_file, parent_model_class):
        self.model_obj = parent_model_class(model_file)
        self.Actions = importlib.import_module("rock4.softtest.pad.uiappium.actions")
                    
    def apply_actions(self, devdriver, debug = False):        
        ''' apply excel actions '''
        
        devid, p_env.MOBILE = devdriver[0], devdriver[1]
        tracer = Tracer(device_id=p_common.get_legal_filename(devid))
        print "Device ready: %s" %devid
                
        Actions = self.Actions
        device_actions = p_common.get_callable_class_method_names(Actions.MobileApp)            
        element_actions = p_common.get_callable_class_method_names(Actions.MobileElement)
        
        case_steps = self.model_obj.translate()
        for case_name, execute_actions, idx in case_steps:
            print "##### Starting Test[%s]: %s" %(idx, case_name)
            tracer.start(case_name)
            tracer.section(case_name)
            
            for execute_function in execute_actions: 
                try:
                    execute_function = self.__replace_var(execute_function)
                            
                    action = execute_function.split("(", 1)[0]                
                    by, value, text, index, timeout = eval(execute_function.replace(action, "self.map_pad_actions", 1))
            
                    if debug:
                        print  '\t',by,value,index,timeout,action,text
                        continue 
                    
                    print "-->",action
                    if action in element_actions:
                        opration_class = Actions.MobileElement 
                        opration_class.by, opration_class.value, opration_class.index, opration_class.timeout = by, value, index, timeout                    
                    elif action in device_actions:
                        opration_class = Actions.MobileApp
                    else:
                        tracer.fail("Do not hava action:%s\t%s" %(action,execute_function))
                        continue                
                    
                    if text:          
                        result = getattr(opration_class, action)(*text)
                    else:
                        result = getattr(opration_class, action)()
                    
                    if result == False:
                        tracer.fail(execute_function)
                    else:
                        tracer.ok(execute_function)
                        
                except Exception,e:
                    tracer.error("%s\t%s" %(e,execute_function))
            tracer.stop(RespTester = "administrator", Tester = "administrator")
            
    def map_pad_actions(self,*args, **kwargs):
        """
        :param args for the parameter, kwargs for features
        """
        find_types = {'css': "CSS_SELECTOR", 'id':"ID", 'name':"NAME", 'class':"CLASS_NAME", 'tagname':"TAG_NAME", 'xpath':"XPATH", 'link':"LINK_TEXT", 'plink':"PARTIAL_LINK_TEXT"}
        [by, value, text, index, timeout] = [find_types.get(kwargs.get("by")), kwargs.get("value"), kwargs.get("text",[]), kwargs.get("index",0), kwargs.get("timeout",10)]
        if args:
            text = args
        text = self.model_obj.getUnicodeArgs(*text) 
        return [by, value, text, index, timeout]
    
    def __replace_var(self, strs):        
        keys = re.findall('#(.*?)#', strs)        
        for key in keys:
            var = self.Actions.MobileElement.GetVar(key)
            strs = strs.replace('#' + key + '#', var)
        return strs

def usage_sample():
    model_obj,errmsg = ModelEntryway.Select("yaml", "api")
    print errmsg
    stream = r"D:\auto\env\testProject\testcase\yaml_demo.yaml"
    y = model_obj(stream,ModelEntryway.parent_model_class)
    for i in y.model_obj.translate():print "--",i
    for i in y.model_obj.testcases:print i
    
if __name__ == "__main__":
    usage_sample()
