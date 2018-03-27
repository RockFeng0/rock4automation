# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.loadtest.LocustTemplate

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.api.loadtest.LocustTemplate,v 2.0 2016年12月15日
    FROM:   2016年12月15日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import re
from rock4.common import p_common
from rock4.softtest.common.datatrans import ExcelDpc


class LocustTemplate(ExcelDpc):
    
    def __init__(self,xls_file):
        ExcelDpc.__init__(self, xls_file)
        self.glob={}
        self.__filevars=[]
        self.__keys = {"precommand":("setvar","sethost","setfilevar"),
                       "transmission":("send"),
                       "verify":("contain")
                       }
    
    def set_template(self,sheet="Performance",alias_name=False):
        '''Samples:
        temp=LocustTemplate(r'D:\auto\python\app-autoApp\demoProject\data\locust_demo.xlsx')
        temp.set_template()
        print temp.get_template()   
        '''
        self.__template = """# -*- encoding: utf-8 -*-
import re
from locust import HttpLocust, TaskSet, task

def _itervar(ll):
    global g1
    
    if not ll:
        return {}
    
    try:
        v = g1.next()
    except:
        g1 = ll[1::].__iter__()    
        v = g1.next()
    return dict(zip(ll[0],v))

def _replace_itervar(ll,strs):
    if not strs:
        return strs
        
    dd = False
    if isinstance(strs, dict):        
        strs=str(strs)
        dd = True
        
    try:
        keys = re.findall('#(.*?)#', strs)
        if keys:
            kv=_itervar(ll)        
        for key in keys:
            var = kv.get(key)
            if var == None:
                continue
            strs = strs.replace('#' + key + '#', var)
    except Exception,e:
        print e
        pass
    finally:
        if dd:
            return eval(strs)
        return strs
"""
        self.__jobs=[]
    
        scene_data = self.get_scene_data(sheet,alias_name)            
        if not scene_data:           
            return
        
        scenex_keys = p_common.get_sorted_list(scene_data.keys())
        for x in scenex_keys:
            scene_x=x.lower()                                        
            
            jobs_keys = p_common.get_sorted_list(scene_data[x].keys())
            if jobs_keys:
                self.__template=self.__template + "\n\ndef jobs_%s(l):\n\tll=%s" %(scene_x,self.__filevars)
            else:
                continue
            
            for y in jobs_keys:
                job = scene_data[x][y]
                
                if job["verify"]:
                    self.__template=self.__template + "\n\t# '%s'\n\twith l.client.%s as resp:\n\t\tif '%s' in resp.content:\n\t\t\tresp.success()\n\t\telse:\n\t\t\tresp.failure('Do not contain: %s\\n%%r' %%resp.content)" %(job["name"], job["data"],job["verify"],job["verify"])
                else:
                    self.__template=self.__template + "\n\t# '%s'\n\tl.client.%s" %(job["name"], job["data"])
                
                self.__jobs.append((job["name"], job["job"]))
                
            self.__template=self.__template + "\n\nclass Root_%s(TaskSet):\n\ttasks = [jobs_%s]\n\nclass WebsiteUser_%s(HttpLocust):\n\ttask_set = Root_%s\n\tweight = 1\n\thost = '%s'\n\tmin_wait = 500\n\tmax_wait = 3000" %(scene_x,scene_x,scene_x,scene_x,self.host)
                
    def get_template(self):
        return self.__template
    
    def get_jobs(self):
        # just for requests test
        return self.__jobs
    
    def get_scene_data(self, sheet, alias_name=False):
        '''Sample:
            temp=LocustTemplate(r'D:\auto\python\app-autoApp\demoProject\data\locust_demo.xlsx')
            print temp.get_scene_data(sheet="Performance")
        '''
        scene_raw_data = self.get_scene_raw_data(sheet)
        
        keys = p_common.get_sorted_list(scene_raw_data.keys())        
        scene_data = {}
        scene_error = 0
        jobs = 0
        for key in keys:
            horizon_scene = scene_raw_data[key]["scene"]        
            if not horizon_scene:
                print "%s do not have Scene." %key
                return
            
            if not scene_data.get(horizon_scene):
                scene_data[horizon_scene] = {}
            
            #### translate data
            named = "%s[%s]" %(scene_raw_data[key]["name"],key)
            #print "======= %s" %named
            if scene_raw_data[key]["precommand"]:
                precommand = scene_raw_data[key]["precommand"]
                self.__precommand(precommand)
            
            url_method_type=None        
            if scene_raw_data[key]["transmission"]:
                transmission = scene_raw_data[key]["transmission"]
                self.__verify_keys(transmission,"transmission")
                url_method_type = eval("self.key_" + self.__replace_var(transmission))         
            
            head=None  
            if scene_raw_data[key]["head"]:
                head = self.__replace_var(scene_raw_data[key]["head"])                
            
            data=None
            if scene_raw_data[key]["data"]:
                # 无论是表单形式还是json形式，都采用dict来传递。
                data = self.__replace_var(scene_raw_data[key]["data"])
            
            expect_str=None            
            verify=scene_raw_data[key]["verify"].strip()            
            if verify:
                self.__verify_keys(verify,"verify")
                expect_str = eval("self.key_" + self.__replace_var(verify))            
            catch_resp=False
            if expect_str:
                catch_resp = True                           

            
            #### construct data
            if url_method_type:
                if self.__is_format_error(head):
                    scene_error = 1
                    print "%s --> %s format error." %(named,"head")                    
                if self.__is_format_error(data):
                    scene_error = 1
                    print "%s --> %s format error." %(named,"data")
                
                if scene_error:
                    continue
                
                if url_method_type[2] == "json":
                    # 格式化dict 为json形式
                    pdata = "json = _replace_itervar(ll,%s)" %data
                    jdata = "json = %s" %data
                else:
                    # 格式化dict 为表单形式
                    pdata = "data = _replace_itervar(ll,%s)" %data
                    jdata = "data = %s" %data
                
                jobs+=1
                if alias_name:
                    final_data = "%s(_replace_itervar(ll,'%s'),headers=_replace_itervar(ll,%s),%s,catch_response=%s,name=u'%s')" %(url_method_type[1],url_method_type[0],head,pdata,catch_resp,named)
                    final_job = "%s('%s',headers=%s,%s,name=u'%s')" %(url_method_type[1],url_method_type[0],head,jdata,named)
                else:
                    final_data = "%s(_replace_itervar(ll,'%s'),headers=_replace_itervar(ll,%s),%s,catch_response=%s)" %(url_method_type[1],url_method_type[0],head,pdata,catch_resp)
                    final_job = "%s('%s',headers=%s,%s)" %(url_method_type[1],url_method_type[0],head,jdata)
                
                scene_data[horizon_scene].update({"job%d" %jobs:{"name":named,
                                                                 "data":final_data,
                                                                 "job":final_job,
                                                                 "verify":expect_str
                                                                 }
                                                  })
#                 print horizon_scene,"job%d" %jobs,named,"%s('%s',headers=%s,%s)" %(url_method_type[1],url_method_type[0],head,pdata)
                    
        if scene_error:
            return        
        return scene_data
    
    def get_scene_raw_data(self, sheet):
        '''
字段设计说明:
1. ID唯一标识，对场景进行纵向分组
2. Scene为场景平行分组，
3. Precommand 使用序号，依次执行   set设置参数，sethost设置Locust host属性..
4. Translation执行 send(url,method,type),type默认为raw，指定发送json;
5. Head和Data要求是dict

如,200用户压测,
平行场景SA有纵向场景ID：test1,test2,test3
平行场景SB有纵向场景ID：test4,test5,test6
那么，
100用户执行SA场景：test1->test2->test3
100用户执行SB场景：test4->test5->test6

        Sample:
            temp=LocustTemplate(r'D:\auto\python\app-autoApp\demoProject\data\locust_demo.xlsx')
            print temp.get_scene_raw_data(sheet="Performance")            
        '''
        #sheet="Performance"
        step_feature=["PreCommand"]
        info_feature=["ID","Name","Transmission","Head","Data","Verify","Scene"]
        unique="ID"
        self.setXlsCasesFeature(sheet,step_feature,info_feature,unique)        
        scene_raw_data = self.getXlsCasesValue()
        return scene_raw_data
    
    def key_setvar(self,**kwargs):
        # keys for precommand
        self.glob.update(**kwargs)             
    
    def key_setfilevar(self,fp):
        '''keys for precommand
        test.txt:
uuu1   uuu2     uuu3
1           1   6            
2           2   5
3           3   4
4           4   3
5           5   2
6           6   

        key_setfilevar(test.txt)    
            self.__filevars --> [['uuu1', 'uuu2', 'uuu3'], ['1', '1', '6'], ['2', '2', '5'], ['3', '3', '4'], ['4', '4', '3'], ['5', '5', '2']]
        Test var:
            print _replace_itervar(self.__filevars,{"X-Device-Id":"#uuu2#","X-Device-Type":"1"})
            print _replace_itervar(self.__filevars,'/cms/educloud/eduDoLogin.json?loginYhmName=admin&loginMmWord=123456&loginSchool=&validCode=&autoLogin=0&test=#uuu1#-#uuu2#')
        '''
        
        filevars = []        
        with open(fp,'r') as f:
            lines = f.readlines()
        
        vlen = 0
        for line in lines:
            line = line.split()
            
            if vlen == 0:
                vlen = len(line)
            
            if line and len(line) == vlen:
                filevars.append(line)
        
        if not self.__filevars:
            self.__filevars = filevars
            return
        
        result = [] 
        for m,n in zip(self.__filevars, filevars):
            result.append(m+n)
        self.__filevars = result
            
        
    def key_sethost(self,host):
        # keys for precommand; rewrite the value for each call
        self.host=host
    
    def key_send(self, url, method="get", contype="raw"):
        # keys for transmission
        if not method.lower() in ('get','post'):
            return
        return url,method.lower(),contype.lower()
    
    def key_contain(self, expect=""):
        # keys for verify        
        return expect.strip()
    
    def __precommand(self,precommand):
        p_keys = p_common.get_sorted_list(precommand.keys())
        for p in p_keys:
            self.__verify_keys(precommand[p], "precommand")
            exec "self.key_" + self.__replace_var(precommand[p])   
    
    def __is_format_error(self,strs):
        try:
            if strs:
                isinstance(eval(strs), dict)
        except:
            return True
        return False
            
    def __replace_var(self, step):
        try:        
            keys = re.findall('#(.*?)#', step)
            for key in keys:
                var = self.glob.get(key)
                if var == None:
                    continue
                step = step.replace('#' + key + '#', var)
        except:
            pass
        finally:
            return step
        
    def __verify_keys(self,step,field):
        kuv = step.split("(")[0]
        keys = self.__keys.get(field)
        err_str = "invalid key '%s' in filed '%s'." %(kuv.encode("gbk"),field)
        if not keys:
            print err_str
            raise Exception(err_str)
        
        if not kuv in keys:
            print err_str
            raise Exception(err_str)
            

if __name__ == "__main__":
    sheet= "Performance"
    temp=LocustTemplate(r'D:\auto\python\app-autoApp\demoProject\data\locust_demo.xlsx')
    temp.set_template(sheet=sheet,alias_name=True)
#     print temp.get_template()
#     print temp.get_scene_data(sheet)
    print temp.get_jobs()
    


