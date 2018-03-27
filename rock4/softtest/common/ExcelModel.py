# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.common.ExcelModel

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.common.ExcelModel,v 1.0 2017年2月9日
    FROM:   2017年2月9日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import os,re
from rock4.common import p_common,p_env
from rock4.common.ext.datafile.excel import Excel

class ExcelModel(Excel):
    ''' translate excel data to dict '''
    
    def __init__(self, xls_file):
        Excel.__init__(self)
        self.__setup()
        xls_file = os.path.join(p_env.DATA_PATH, xls_file)
        if not os.path.isfile(xls_file):        
            raise Exception("invalid excel file '%s'." %(xls_file))
        self.__feature["workbook"] = xls_file
                    
    def getUnicodeArgs(self,*args):
        result = []
        for arg in args:
            if isinstance(arg, str):
                result.append(arg.decode('utf-8'))
            else:
                result.append(arg)
        return result 
        
    def translate(self):
        ''' usage:
            m = ExcelModel(r"D:\auto\buffer\test.xlsx")
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
            print ExcelModel(r"D:\auto\buffer\test.xlsx").check()    
        :return Ture/False
        '''
        result = True
        self.testcases,invalid_cases = self.getXlsCasesValue()
        if invalid_cases:
            print "Waring: Excel need available fields:"
            for k,v in invalid_cases.items():
                print "\t%s -> %r" %(k, v)
            result = False
        elif not self.testcases:
            print 'Warning: Invalid Excel Test Model.'
            result = False
            
        return result
    
    def getXlsCasesValue(self):
        ''' analize the xls or xlsx file and get the fixed form data in the sheet named "TestCase"
        Use for twsm's auto upddate   
        Sample usage:
            getXlsCasesValue()
        return:
            testSet
        '''
        word_p = "^[\w-]+$"
        
        self.open_excel(self.__feature["workbook"],self.__feature["worksheet"])

        # 依据 TestCaseID 获取测试步骤信息
        testSet = []
        invalid_cases = {}
        features = self.__feature["steps"] + self.__feature["info"]        
        for i in xrange(1, self.excel_nrows()):
            
            case_id = self.excel_cell(i,self.__feature["unique"])            
            if isinstance(case_id, int):                
                case_id = str(case_id)                                
            if not (case_id and re.search(word_p,case_id)):
                continue
            
            invalid_field = [feature for feature in features if self.excel_cell(0, feature) == None]
            if invalid_field:
                invalid_cases[case_id] = invalid_field
                continue
                    
            tmp ={}
            tmp[self.__feature["unique"].lower()] = case_id
            for f in features:
                if f == self.__feature["unique"]:
                    continue
                # 处理步骤化特征
                content = self.excel_cell(i, f)
                #print repr(content)
                
                if isinstance(content, int):
                    tmp[f.lower()] = content
                                    
                elif f in self.__feature["steps"]:
                    tmp[f.lower()] = self.__generateCaseSteps(content)
                    
                else:
                    tmp[f.lower()] = content
            testSet.append(tmp)
        return testSet,invalid_cases
      
    def __generateCaseSteps(self,strs):
        ''' format the string to steps 
        Sample usage:
            steps = __generateCaseSteps("asdfasdfsdf")
            steps = __generateCaseSteps("1.asdfasdfsdf\n2.sodfi")
            steps = __generateCaseSteps("1.1.dfasdfahttp://192.168.1.1sdfsdf2.1.1.1.1\n")
            steps = __generateCaseSteps("dfasdfahttp://192.168.1.1sdfsdf2.1.1.1.1\n")
        '''   
        result = []
        num_head = "^\d+\.";#去掉数字编号; 按照行数分步骤，第一行就是第一步，依次...
        
        if strs:
            raws = [i.strip() for i in strs.split("\n") if i.strip()];#去除空行
            for raw in raws:
                raw = re.sub(num_head,"",raw)
                if raw:
                    result.append(raw)
        return result
    
    def __generateCaseSteps_bak(self,strs):
        ''' format the string to steps 
        Sample usage:
            steps = __generateCaseSteps("asdfasdfsdf")
            steps = __generateCaseSteps("1.asdfasdfsdf\n2.sodfi")
            steps = __generateCaseSteps("1.1.dfasdfahttp://192.168.1.1sdfsdf2.1.1.1.1\n")
            steps = __generateCaseSteps("dfasdfahttp://192.168.1.1sdfsdf2.1.1.1.1\n")
        '''   
        result = {}
        num_head = "^\d+\.";#去掉数字编号; 按照行数分步骤，第一行就是第一步，依次...
        
        if strs:
            raws = [i.strip() for i in strs.split("\n") if i.strip()];#去除空行
            for raw in raws:
                step_num = raws.index(raw) + 1
                raw = re.sub(num_head,"",raw)
                if raw:
                    result["Step_%s_info" %step_num] = raw
        return result
    
    def __setup(self):
        ''' set the excel model keys 
            # 定义EXCEL的 测试用例 规范:
                sheet_name:     EXCEL的sheet名称
                unique_name:    EXCEL中，唯一用于标识数据唯一性的标题特征，如: TestCaseID
                steps_fields:    EXCEL中，需要步骤化的标题特征
                info_fields:    EXCEL中，不需要步骤化的标题特征
        '''
        # 定义Excel数据模型
        self.__feature = {}
        self.__feature["workbook"]    = ""
        self.__feature["worksheet"]   = "TestCase"
        self.__feature["unique"]      = "TestCaseID" 
        self.__feature["steps"]       = ["Steps","PreCommand","PostCommand","Verify"]
        self.__feature["info"]        = ["TestCaseID","Description","Head","Data"]
        
        # 定义关键字模型        
        self.__executer_seq_fields = ["precommand","steps","postcommand", "verify"]
        self.__case_title_field = 'description'
                      
def usage_sample1():
    datadriver = Excel()    
    datadriver.open_excel(r"d:\auto\buffer\test.xlsx", "TestCase002")
    
    # 依据 Title给的cell值
    for i in xrange(1, datadriver.excel_nrows()):
        title   = datadriver.excel_cell(i, "Title")
        name    = datadriver.excel_cell(i, "Name")
        gender  = datadriver.excel_cell(i, "Gender")
        hobbies = datadriver.excel_cell(i, "Hobbies")
        print "%s %s %s %s" %(title,name,gender,hobbies)


def usage_sample2():
    #p_common.init_project_env("web_excel_usage", proj_path = r'D:\auto\buffer\testProject', initdirs = True)
    m = ExcelModel(r"D:\auto\env\testProject\testcase\web_excel_usage.xlsx")    
    for i in m.translate():print "--",i
    for i in m.testcases:print i
    
if __name__ == '__main__':
    usage_sample2()
    
    