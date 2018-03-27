# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.common.XmlModel

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.common.XmlModel,v 1.0 2017年2月9日
    FROM:   2017年2月9日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import os
from rock4.common import p_env
from rock4.common.ext.datafile.xmlparser import Xml

class XmlModel(Xml):
    def __init__(self,xmlFileName):
        ''' initial xml data object with the your project        --data driver with xml'''        
        xml_file = os.path.join(p_env.DATA_PATH,xmlFileName) 
        Xml.__init__(self, xml_file)                
            
    def setFeature(self,str_feature=["by","value"],int_feature=["index"],class_feature="Web",root_tag='root',feature_tag='by',attr_feature = []):
        ''' 定义 XML规范，并生成继承类:
            root_tag:     XML根节点
            feature_tag:    XML叶子节点，用于识别元素特征，并生成类的成员变量，如:("by","value")=("id","login_input")
            class_feature:    指定继承的类
            str_feature:    XML元素特征的值是 "字符串" 的"成员列表"
            int_feature:    XML元素特征的值是 "数字" 的"成员列表"
            attr_feature:   XML设置属性标签： attr_feture = ["className","text"]等
        '''
        # 初始设置
        self.int_feature = int_feature
        self.str_feature = str_feature
        self.attr_feature = attr_feature        
        self.feature = self.int_feature + self.str_feature + self.attr_feature
        self.clas = class_feature
        self.root_tag = root_tag
        self.feature_tag = feature_tag        
    
    def classifyFeatureAll(self): 
        ''' Sample usage:
            classifyFeatureAll()
        '''
        feats = self.find_elements(self.feature_tag)
             
        
        count = len(feats)
        print "Features count: %d" %count
        class_stack = []
        for index in range(count):
            class_stack.append([])
            feat = feats[index]
            while self.get_node_parent(feat):
                parent = self.get_node_parent(feat)
                if self.get_node_tagname(parent) != self.root_tag:                  
                    feat = parent
                    class_stack[index].append(self.get_node_tagname(parent))
                else:
                    break
            class_stack[index].reverse()
#             print class_stack
            
        # 生成feature结构类
        all_class = ""
        tmp = ""
        for i in class_stack:    
            if tmp != i[0]:
                all_class = all_class + self.classfyFeature(i)
                tmp = i[0]
            else:                
                all_class = all_class + self.classfyFeature(i)[len(tmp)+8:]
        return all_class
    
    def classifyFeatureAll_back(self): 
        ''' Sample usage:
            classifyFeatureAll()        
        '''
        
        # 遍历feature结构，组成列表
        if self.swt == "Beautiful":               
            feats = self.root.find_all(self.feature_tag)
            count = len(feats)
            fp = lambda nd: nd.parent
            fc = lambda index: feats[index]            
        elif self.swt == "Minidom":
            feats = self.root.getElementsByTagName(self.feature_tag)
            count = feats.length
            fp = lambda nd: nd.parentNode
            fc = lambda index: feats.item(index)
        else:
            # self.swt --> "System"
            feats = self.root.GetElementsByTagName(self.feature_tag)            
            count = feats.Count
            fp = lambda nd: nd.ParentNode
            fc = lambda index: feats.Item(index)            
        
        print "Features count: %d" %count
        class_stack = []
        for index in range(count):
            class_stack.append([])
            feat = fc(index)
            while fp(feat):
                parent = fp(feat)
                if self.get_node_tagname(parent) != self.root_tag:                  
                    feat = parent
                    class_stack[index].append(self.get_node_tagname(parent))
                else:
                    break
            class_stack[index].reverse()
#             print class_stack
            
        # 生成feature结构类
        all_class = ""
        tmp = ""
        for i in class_stack:    
            if tmp != i[0]:
                all_class = all_class + self.classfyFeature(i)
                tmp = i[0]
            else:                
                all_class = all_class + self.classfyFeature(i)[len(tmp)+8:]
        return all_class
    
    def classfyFeature(self,tag_list):
        ''' Sample usage:
            classfyFeature(["Login","TextUserName"])    
            classfyFeature(["Login","TextUserNamealskdjflsj"])      
        '''   
        feature = self.getFeature(tag_list)
        
#         f_class = lambda num,tag,clas: "\n"+("\t"*num)+"@classmethod"+"\n"+("\t"*num)+"class %s(%s):" %(tag,clas)
        f_class = lambda num,tag,clas: "\n"+("\t"*num)+"class %s(%s):" %(tag,clas)
        f_int   = lambda num,parm,parmv: "\n"+("\t" * num)+"""%s = %d""" %(parm,int(parmv))
        f_str   = lambda num,parm,parmv: "\n"+("\t" * num)+"""%s = '%s'""" %(parm,parmv)
        f_attr  = lambda num,parm,parmv: "\n"+("\t" * num)+"""%s = %s""" %(parm,parmv)
#         f_static= lambda num,by_v,va_v: "\n"+("\t" * num)+"""(by,value) = ('%s','%s')""" %(by_v,va_v)
        
        for tag in tag_list:
            index = tag_list.index(tag)
            if index == 0:
                class_strs="""
class %s:""" %tag
            else:
                class_strs = class_strs + f_class(index, tag, self.clas)
            
            if index == len(tag_list)-1:
                # 这里添加 变量 参数
                for (k,v) in [(i,feature.get(i)) for i in self.int_feature if feature.get(i)]:
                    class_strs = class_strs + f_int(len(tag_list),k,v)
                
                for i in self.str_feature:                    
                    class_strs = class_strs + f_str(len(tag_list),i,feature.get(i))
#                 class_strs = class_strs + f_static(len(tag_list),feature.get("feature"),feature.get("value"))
                
                if self.attr_feature:
                    result = dict([(i,feature.get(i)) for i in self.attr_feature if feature.get(i)])
                    class_strs = class_strs + f_attr(len(tag_list),"uiselector",result)
                    
        return class_strs
    
    def getFeature(self,tag_list):        
        ''' return a dict of the feature 
            Sample usage:
                print getFeature(["Login","TextUserName"]);# Login.TextUserName.Type("123456")
        '''
        if not tag_list:
            raise Exception("Invalid tag_list '%s'" %tag_list)
        
        elm = self.find_element(tag_list)
         
        if not elm:
            raise Exception("Not find the feature '%s'" %tag_list)
        
        result = self.get_children_texts(elm)
        tmp = result.keys()            
        for j in [i for i in tmp if not i in self.feature]:
            result.pop(j)
        
        return result

def usage_sample():
    ef = XmlModel(r"D:\auto\python\app-autoApp\demoProject\data\sysweb.xml")
    ef.setFeature(str_feature=["by","value"],int_feature=["index"],class_feature="Web",root_tag='root',feature_tag='by')    
    result = ef.getFeature(["Login","LoginAccountInput"])
    print result
    try:
        print ef.classfyFeature(["Login","LoginPasswordInputs"])
    except Exception,e:
        print "Error: %s" %e
    finally:
        print ef.classfyFeature(["Login","LoginPasswordInput"])
           
    print ef.classifyFeatureAll()

if __name__ == '__main__':
    usage_sample()
    