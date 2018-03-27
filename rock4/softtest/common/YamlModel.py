# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.common.YamlModel

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.common.YamlModel,v 1.0 2017年2月9日
    FROM:   2017年2月9日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import os,re
from rock4.common import p_common,p_env
from rock4.common.ext.datafile.yamlparser import Yaml

# yaml = lambda stream, coding="gbk": Yaml().load_all(stream, coding)
class YamlModel(Yaml):
    def __init__(self, yaml_file, coding = "gbk"):
        self.__setup()
        yaml_file = os.path.join(p_env.DATA_PATH, yaml_file)
        if not os.path.isfile(yaml_file):        
            raise Exception("invalid yaml file '%s'." %(yaml_file))
        self.__feature["yamlfile"] = yaml_file
        self.__feature["yamlcoding"] = coding
    
    def translate(self):
        ''' usage:
            m = YamlModel(r"D:\auto\buffer\test.yaml")
            for i in m.translate():print i
        :return iterator (case_name, execute_function)
        '''
        if not self.check():
            return 
        
        for idx in range(len(self.testcases)):
            testing = self.testcases[idx]
            case_id = testing.get("testcaseid")
            case_name = p_common.get_legal_filename("%s[%s]" %(case_id,unicode(testing[self.__case_title_field])))
                         
            # executer actions
            execute_actionss = []
            for field in self.__executer_seq_fields:
                steps_info = testing.get(field)                                
                for execute_function in steps_info:                                   
                    if not execute_function:
                        continue
                    execute_actionss.append(execute_function)                
            yield (case_name, execute_actionss, idx)
    
    def check(self):
        ''' usage:
            print YamlModel(r"D:\auto\buffer\test.yaml").check()    
        :return Ture/False
        '''
        result = True
        self.testcases,invalid_cases = self.getYamlCasesValue()
        if invalid_cases:
            print "Waring: Yaml need available fields:"
            for k,v in invalid_cases.items():
                print "\t%s -> %r" %(k, v)
            result = False
        elif not self.testcases:
            print 'Warning: Invalid Yaml Test Model.'
            result = False
            
        return result
    
    def getYamlCasesValue(self):
        ''' analize the yaml file and get yaml file case value
        Sample usage:
            getYamlCasesValue()
        return:
            testSet,invalid_cases
        '''
        word_p = "^[\w-]+$"
        
        testSet = []
        invalid_cases = {}
        try:
            all_data = self.load_all(self.__feature["yamlfile"], self.__feature["yamlcoding"])
        
            features = self.__feature["steps"] + self.__feature["info"]
            for cases in all_data:
                if not isinstance(cases, list):
                    continue
                
                for case in cases:
                    if not isinstance(case, dict):
                        continue
                    
                    case_id = case.get(self.__feature["unique"])
                    if isinstance(case_id, int):
                        case_id = str(case_id)                                    
                    if not (case_id and re.search(word_p,case_id)):
                        continue
                    
                    case_keys = map(lambda key: key.lower(),case.keys())
                    invalid_field = [i for i in features if not i.lower() in case_keys]
                    if invalid_field:
                        invalid_cases[case_id] = invalid_field
                        continue
                    
                    tmp = {}
                    for k,v in case.items():
                        if k.lower() in self.__executer_seq_fields:
                            v = v if v else []
                            if isinstance(v, list):
                                tmp[k.lower()] = v
                            else:
                                invalid_cases[case_id] = "%s should be a list or none type." %k
                                break
                        else:
                            v = v if v else ""                            
                            if isinstance(v, str) or isinstance(v, unicode) or isinstance(v, int) or isinstance(v, float):
                                tmp[k.lower()] = v
                            else:
                                invalid_cases[case_id] = "%s should be a string or int or float or none type." %k
                                break
                            
                    testSet.append(tmp)
        except Exception,e:
            print e
        finally:
            return testSet,invalid_cases
    
    def getUnicodeArgs(self,*args):
        result = []
        for arg in args:
            if isinstance(arg, str):
                result.append(arg.decode('utf-8'))
            else:
                result.append(arg)
        return result 
    
    def __setup(self):
        ''' set the excel model keys 
            # 定义EXCEL的 测试用例 规范:               
                unique_name:    EXCEL中，唯一用于标识数据唯一性的标题特征，如: TestCaseID
                steps_fields:    EXCEL中，需要步骤化的标题特征
                info_fields:    EXCEL中，不需要步骤化的标题特征
        '''
        # 定义Yaml数据模型
        self.__feature = {}
        self.__feature["yamlfile"]    = ""
        self.__feature["yamlcoding"]  = ""
        self.__feature["unique"]      = "TestCaseID" 
        self.__feature["steps"]       = ["Steps","PreCommand","PostCommand","Verify"]
        self.__feature["info"]        = ["TestCaseID","Description","Head","Data"]
        
        # 定义关键字模型        
        self.__executer_seq_fields = ["precommand","steps","postcommand", "verify"]
        self.__case_title_field = 'description'

def usage_sample():
    ''' t.tmp:
---
-
  TestCaseID: ATP-1
  Description: "时代氛围分为"  
  PreCommand:
   - Set(passwd = "123456")
  Steps:
   - TypeIn("css=#login","admin")
   - TypeIn("css=#passwd","#passwd#")
  PostCommand: [test,'射手','hello',你好,nihao]
  Verify:
  Head: af
  Data: sdf
-
  TestCaseID: ATP-2
  Description: "时代氛围分为"  
  PreCommand:
   - Set(passwd = "123456")
  Steps:
   - TypeIn("css=#login","admin")
   - TypeIn("css=#passwd","#passwd#")
  PostCommand:
  Verify:
  Head: 12314
  Data: 1.2  
    '''
    #stream = r"D:\auto\env\testProject\testcase\yaml_demo.yaml"
    stream = r"D:\auto\buffer\t.tmp"
    y = YamlModel(stream, "gbk")    
    for i in y.translate():print "--",i
    for i in y.testcases:print i    
    
if __name__ == '__main__':
    usage_sample()

    