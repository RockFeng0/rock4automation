# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.common

Rough version history:
v1.0    Original version to use
v2.0    Classify some useful functions 
v2.1    define this module for common functions
v3.0    delete the class of WebBasic 
        use this module instead of the class named WebBasic        

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:    rock4.common.p_common,v 3.0 2017年2月7日
    FROM:   2015年4月14日
********************************************************************
            
======================================================================

Frequently used package and functions.
'''
from urllib import localhost
import locale,codecs,glob,zipfile
import sys,os,time,re,subprocess,inspect,ConfigParser,hashlib,socket
import p_env

config = ""
filesystemencoding = sys.getfilesystemencoding()
encoding = "ascii"
if sys.platform == 'win32':
    # Part code of IOBinding 
    try:
        encoding = locale.getdefaultlocale()[1]
        codecs.lookup(encoding)
    except LookupError:
        pass
else:
    print "Waring: not window system.encoding is not setted."
encoding = encoding.lower()

def init_project_env(subject='Automation', proj_path = None, initdirs=True, verify=False, sysencoding = "utf-8"):
    ''' Set the environment for pyrunner '''
    #########
    if sysencoding:
        set_sys_encode(sysencoding)
    
    ##### 测试项目初始化
    
    if proj_path:
        p_env.PROJECT_PATH = proj_path        
    else: 
        try:
            executable_file_path = os.path.dirname(os.path.abspath(inspect.stack()[-1][1]))
        except:
            executable_file_path = os.path.dirname(sys.path[0])
        finally:
            p_env.PROJECT_PATH = os.path.join(executable_file_path,subject)
            
    p_env.MODULE_NAME       = os.path.splitext(os.path.basename(subject))[0]
    p_env.PROJECT_CFG_FILE  = os.path.join(p_env.PROJECT_PATH,"config.ini")
    p_env.CASE_PKG_PATH     = os.path.join(p_env.PROJECT_PATH,"testcase")
    p_env.DATA_PATH         = os.path.join(p_env.PROJECT_PATH,"data")
    
    p_env.BUFFER_PATH       = os.path.join(p_env.PROJECT_PATH,"buffer")
    p_env.RESOURCE_PATH     = os.path.join(p_env.PROJECT_PATH,"resource")
    p_env.TOOLS_PATH        = os.path.join(p_env.PROJECT_PATH,"tools")
    
    p_env.RST_PATH          = os.path.join(p_env.PROJECT_PATH,"result")
    p_env.RST_CASE_LOG_PATH = os.path.join(p_env.PROJECT_PATH,"result","testcase")
    p_env.RST_SCR_SHOT_PATH = os.path.join(p_env.PROJECT_PATH,"result","screenshots")
    
    #### 创建项目结构
    if initdirs:
        mkdirs(p_env.CASE_PKG_PATH)
        mkdirs(p_env.DATA_PATH)
        
        mkdirs(p_env.BUFFER_PATH)
        mkdirs(p_env.RESOURCE_PATH)
        mkdirs(p_env.TOOLS_PATH)
        
        mkdirs(p_env.RST_PATH)
        mkdirs(p_env.RST_CASE_LOG_PATH)
        mkdirs(p_env.RST_SCR_SHOT_PATH)
        
    ##### 验证项目测试所需的路径
    if not verify:
        return    
    
    if os.path.isdir(p_env.PROJECT_PATH):
        sys.path.append(p_env.PROJECT_PATH)
        
    if not os.path.isdir(p_env.CASE_PKG_PATH):
        raise Exception("Can't find 'testcase' directory in this project(%s)." %p_env.PROJECT_PATH)
    
    if not os.path.isdir(p_env.DATA_PATH):
        raise Exception("Can't find 'data' directory in this project(%s)." %p_env.PROJECT_PATH)
    
def set_sys_encode(code):
    import sys;reload(sys)
    getattr(sys, "setdefaultencoding")(code)

###  Common functions    
def get_stamp_date():
    ''' Return the current date '''
    return time.strftime("%Y-%m-%d")

def get_stamp_datetime():
    ''' Return the current date time '''
    return time.strftime("%Y-%m-%d %H:%M:%S")

def get_stamp_datetime_coherent():
    ''' Return the current date time '''
    return time.strftime("%Y-%m-%d_%H_%M_%S")

def add_unique_postfix(fn):
    ''' Return an unique postfix 
    Sample usage:
        add_unique_postfix("test.txt")    
    '''
    fn = unicode(fn)
    
    if not os.path.exists(fn):
        return fn

    path, name = os.path.split(fn)
    name, ext = os.path.splitext(name)

    make_fn = lambda i: os.path.join(path, '%s_%d%s' % (name, i, ext))

    for i in xrange(2, sys.maxint):        
        uni_fn = make_fn(i)
        if not os.path.exists(uni_fn):            
            return uni_fn    
    return None

def get_legal_filename(fn):
    '''
    Sample usage:
    print get_legal_filename("你好&-|他*")
    print get_legal_filename("\n你好&-|他*")
    '''
    prog=re.compile(r"[\n\\/:*?\"<>|]")
    return prog.sub("",fn)

def force_delete_file(file_path):
    ''' force delete a file '''
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            return file_path
        except:           
            return add_unique_postfix(file_path)
    else:
        return file_path

def mkdirs(dir_path):
    ''' make a directory if it not exists'''
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)        

def mkzip(source_dir, output_filename):
    '''Usage:
        p = r'D:\auto\env\ttest\ins\build\lib\rock4\softtest\support'
        mkzip(os.path.join(p, "appiumroot"),os.path.join(p, "appiumroot.zip"))
        unzip(os.path.join(p, "appiumroot.zip"),os.path.join(p, "appiumroot2"))  
    '''
    zipf = zipfile.ZipFile(output_filename, 'w', zipfile.zlib.DEFLATED)
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep);#相对路径
            zipf.write(pathfile, arcname)
    zipf.close()

def unzip(zipfilename, unziptodir):    
    if not os.path.exists(unziptodir): os.mkdir(unziptodir)
    
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        #name = name.replace('\\','/')
       
        if name.endswith(os.sep):
            os.mkdir(os.path.join(unziptodir, name))
        else:            
            ext_filename = os.path.join(unziptodir, name)
            ext_dir= os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):   
                os.makedirs(ext_dir)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()
 
def getFileMd5(filePath):
    if not os.path.isfile(filePath):
        return
    myhash=hashlib.md5()
    f=file(filePath,'rb')
    while True:
        b=f.read(8096)
        if not b:
            break;
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def getFileSize(filePath):
    if not os.path.isfile(filePath):
        return
    else:
        return os.path.getsize(filePath)
       
def get_value_from_cfg():
    ''' initial the configuration with file that you specify 
        Sample usage:            
            config = get_value_from_cfg()            
        return:
            return a dict        -->config[section][option]  such as config["twsm"]["dut_ip"]                
    '''    
    
    if not os.path.isfile(p_env.PROJECT_CFG_FILE):        
        #raise Exception("\n\tcommon exception 1.1: file not exists '%s'." %(cfg_abspath))
        return ""

    cfg = {}   
    config = ConfigParser.RawConfigParser()
    
    try:
        config.read(p_env.PROJECT_CFG_FILE)
    except Exception,e:
#         raise Exception("\n\tcommon exception 1.2: Not a well format configuration file. error: '%s'" %(e))
        return ""
    sections = config.sections()
    
    for section in sections:
        cfg[section] = {}
        options = config.options(section)
        for option in options: 
            cfg[section][option]=config.get(section,option)
#             print "cfg[%s][%s]\t=\t%s" %(section,option,cfg[section][option])
    return cfg

def get_current_config(section):    
    return get_value_from_cfg().get(section)

def get_sorted_list(ll):
    '''按数字排序
    Sample usage:        
        get_sort_list(["t1","t11","t2","t22","t3ss","t4gg"])
    '''
    
    if not isinstance(ll, list):
        return ll
    
    re_digits = re.compile(r'(\d+)')
    def emb_numbers(s):        
        pieces=re_digits.split(s)  
        pieces[1::2]=map(int,pieces[1::2])      
        return pieces
    
    return sorted(ll,key=emb_numbers) 

def get_class_method_names(testClass):
    isInstanceMethod = lambda attrname: hasattr(getattr(testClass, attrname), '__call__')            
    return filter(isInstanceMethod, dir(testClass))

def get_callable_class_method_names(testClass):
    '''
    all = p_common.get_class_method_names(WebBrowser)
    print len(all)
    all = p_common.get_callable_class_method_names(WebElement)
    print all
    print len(all)
    '''
    isInstanceMethod = lambda attrname: not attrname.startswith("_") and hasattr(getattr(testClass, attrname), '__call__')            
    return filter(isInstanceMethod, dir(testClass))

def exec_sys_cmd(listcmd, end_expects=None, save2logfile=None, coding = encoding):
    ''' 执行系统命令,并等待执行完
    Parameter:
        listcmd - 执行的命令，列表格式
        end_expects - 命令执行结束，在输出的最后一行，正则搜素期望值，并设置 结果标志
        save2logfile - 设置执行过程，保存的日志
        
    Sample usage:
        cmd = ["ping","127.0.0.1","-n","1"]
        print exec_sys_cmd(cmd)
        print exec_sys_cmd(cmd, save2logfile= r"d:\auto\buffer\t.tmp")
        print exec_sys_cmd(cmd, end_expects=u"平均 = 0ms", save2logfile= r"d:\auto\buffer\t.tmp") 
    '''
    
    if save2logfile and not os.path.isfile(save2logfile):
        raise Exception("invalide file: %s" %save2logfile)
    
    if end_expects and not isinstance(end_expects, unicode):
        raise Exception("invalide unicode string: '%s'" %end_expects)
    
#     result = False
    subp = subprocess.Popen(listcmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    while subp.poll()==None:
        next_line = subp.stdout.readline().decode(coding)
        if next_line:
            print next_line
            
            if save2logfile:
                with open(save2logfile, 'a') as f:
                    f.write(next_line.encode(filesystemencoding))
            
            if end_expects and re.search(end_expects, next_line):
                result = True
            else:
                result = False
                
    if subp.returncode:
        result = False
        if save2logfile:
            with open(save2logfile, 'a') as f:
                f.write("sub command error code: %s" %subp.returncode)
                
    return result

def until(method, timeout = 30, message=''):
    """Calls the method until the return value is not False."""
    end_time = time.time() + timeout
    while True:
        try:
            value = method()
            if value:
                return value
        except:
            pass            
        time.sleep(1)
        if time.time() > end_time:
            break
    raise Exception(message)

def until_not(method, timeout = 30, message=''):
    """Calls the method until the return value is False."""
    end_time = time.time() + timeout
    while True:
        try:
            value = method()
            if not value:
                return value
        except:
            return True
        time.sleep(1)
        if time.time() > end_time:
            break
    raise Exception(message)

#### Process string
def seqfy(strs):
    ''' 序列化 字符串--->实际效果是，为字符串，添加行号，返回字符串
    Sampe usage:
        strs = ["", None, u"First-line\nSecond-line\nThird-line", u"没有换行符"]
        for s in strs:
            print "---"
            result = seqfy(s)
            print result
            print unseqfy(result)
    '''
    
    if not strs:
        return
    
    result = ""
    seq = 1
    ss = strs.split("\n")
    for i in ss:
        if i:
            result = "".join([result, str(seq), ".", i, "\n"])
            seq = seq + 1            
    return result

def unseqfy(strs):
    ### 反序列化字符串--->实际效果是，去掉每行字符串前面的行号， 返回字符串
    if not strs:
        return
    
    result = ""   
    ss = strs.split("\n")
    for i in ss:
        raw = i.split(".",1)
        if len(raw) == 2:
            try:
                int(raw[0])
            except:
                result = "".join([result, i, "\n"])                    
            else:
                result = "".join([result, raw[1], "\n"])
        else:
            result = "".join([result, raw[0], "\n"])                
             
    return result

def stepfy(strs):
    ''' 步骤化 字符串 --->实际效果是, 依据 序列化的字符串，转换为 Step_%s_info 的字典， 返回字典
    Sample usage:
        test_strs = [
        "",
        None,
        u"First-line\nSecond-line\nThird-line",
        u'1.First-line\n2.Second-line\n3.Third-line\n',
        u'3.没有换行符',
        u'3.有换行符\n',
        "asdfasdfsdf",    
        "1.asdfasdfsdf\n2.sodfi",
        "1.1.dfasdfahttp://192.168.1.1sdfsdf2.1.1.1.1\n",
        "dfasdfahttp://192.168.1.1sdfsdf2.1.1.1.1\n",
        ]
        for i in test_strs:
            steps = stepfy(i)
            un = unstepfy(steps)
            print "string: %r" %i
            print "stepfy: %s" %steps
            print "unstepfy: %r\n" %un
    '''
    
#     result = {}
#     prog_step   = re.compile("(\d+)\.(.*)")
#       
#     if not strs:
#         return result
#       
#     step_string = prog_step.findall(strs)
#     if step_string:
#         for step in step_string:
#             result["Step_%s_info" %step[0]] = step[1]         
#     else:
#         result["Step_1_info"] = strs
#       
#     return result
    result = {}
    prog_step   = re.compile("^\d+\.")
      
    if not strs:
        return result
      
    raws = strs.split("\n")
    for raw in raws:
        step_num = raws.index(raw) + 1
        raw = prog_step.sub("",raw)       
        if raw:
            result["Step_%s_info" %step_num] = raw
    return result

def unstepfy(sdict):
    ### 反步骤化 字符串--->实际效果是, 依据 stepfy返回的字典数据，进行反步骤化，还原数据
    if not sdict:
        return ""
    
    if not isinstance(sdict, dict):
        return sdict
    
    result = []
    for k,v in sdict.items():
        num = k.split("_")[1]
        result.append("%s.%s\n" %(num,v))
    
    if result: 
        tmp = get_sorted_list(result)    
        f = lambda x,y: x + y
        return reduce(f, tmp)  

#### Others

def find_data_files(source,target,patterns,isiter=False):
    """Locates the specified data-files and returns the matches; 
        filesystem tree for setup's data_files in setup.py
        Usage:
            data_files = find_data_files(r"C:\Python27\Lib\site-packages\numpy\core","numpy/core",["*.dll","*.pyd"])
            data_files = find_data_files(r"d:\auto\buffer\test\test","buffer/test/test",["*"],True)
        :param source -a full path directory which you want to find data from
        :param target -a relative path directory which you want to pack data to
        :param patterns -glob patterns, such as "*dll", "*pyd"  etc.
        :param isiter - True/Fase, Will traverse path if True when patterns equal ["*"] 
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
            elif isiter and os.path.isdir(filename):
                source2 = os.path.join(source,filename)
                targetpath2 = "%s/%s" %(target,os.path.basename(filename))
                # iter_target = os.path.dirname(targetpath2)
                ret.update(find_data_files(source2,targetpath2,patterns,isiter))
             
    return sorted(ret.items())

def simple_progress_bar(transferred, toBeTransferred, suffix=''):
    ''' usage:
        for i in range(100):
            simple_progress_bar(i,100)    
    '''
    bar_len = 60
    bar_info = "[%s] %s%s ...%s"        
    rate = transferred/float(toBeTransferred)
    
    filled_len = int(round(bar_len * rate))
    percents = round(100.0 * rate, 1)
    
    bar = '=' * filled_len + '-' * (bar_len - filled_len)        
    print bar_info %(bar, percents, '%', suffix),"\r",
        
class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0,    unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"        
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info
            
    def refreshinfo(self, count=1, status=None):
        '''Sample usage:
            f=lambda x,y:x+y
            ldata = range(10)
            total = reduce(f,range(10))
            progress = ProgressBar("refresh", total=total, unit="KB", chunk_size=1.0, run_status="正在下载", fin_status="下载完成")
            
            import time
            for  i in ldata:
                time.sleep(0.2)
                progress.refreshinfo(count=i)
        '''
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count == self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print self.__get_info(), end_str,
    
    def __get_bar(self):
        # 【名称】状态 进度 百分号 进度符号
        rate = float(self.count) / float(self.total)
        tag="="
        _bar = "[%s] %s %.2f%s %s" %(self.title, self.status, rate * 100, "%" ,tag * int(rate * 50))
        return _bar
    
    def refreshbar(self,count=1, status=None):
        '''Sample usage:
            import time
            progress = ProgressBar("viewbar", total=45, run_status="正在下载", fin_status="下载完成")    
            for i in range(46):  
                time.sleep(0.1)  
                progress.refreshbar(i)
        '''
        self.count = count
        self.status = status or self.status
        end_str = "\r"
        if self.count == self.total:
            end_str = '\n'
            self.status = status or self.fin_status
#         print '%d' %rate_num + "%" + "%s" %bar_word,'\r',
#         sys.stdout.write('\r' + '%d' %rate_num + "%" + "%s" %bar_word)
#         sys.stdout.flush()
        print self.__get_bar(), end_str,
    
def wait_for_connection(ip="localhost",port=4444,wait_time=30):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_time = time.time() + wait_time
    while True:
        try:
            sk.connect((ip,port))
            sk.close()
            return True            
        except:
            time.sleep(1)            
            continue   
        if(time.time() > end_time):
            break
    raise Exception("Connect(%s:%s) timeout.") %(localhost,port)

def map_function(func_str, fw_action_addtion=None,bw_action_addtion=None, alias_func=None):
    ''' Sample usage:
        print map_function('set',alias_func = "ini_items")
        print map_function('set',fw_action_addtion="action_steps_",bw_action_addtion="_for_upd",alias_func = "ini_items")
        print map_function('set(a=1,b=2,c=Test())',"action_steps_","_for_upd","ini_items")
        print map_function('set("login",a="good",b=Test())',"action_steps_","_for_upd")
    '''
    
    split_action_value = re.compile("^(\w+)(\((.*)\)$)?")
    matched   = split_action_value.match(func_str)    
     
    if matched:
        action = matched.group(1).lower()
        value = matched.group(2)
        #params = matched.group(3)
        
        if alias_func:
            action = alias_func
        if fw_action_addtion:
            action = fw_action_addtion + action        
        if fw_action_addtion:
            action = action + bw_action_addtion
        
        if value:
            return action+value
        else:
            return action
        
def get_exception_error():
    ''' Get the exception info
    Sample usage:
        try:
            raise Exception("asdfsdfsdf")
        except:
            print common.get_exception_error()
    Return:
        return the exception infomation.
    '''
    error_message = ""
    for i in range(len(inspect.trace())):
        error_line = u"""
File:      %s - [%s]
Function:  %s
Statement: %s
-------------------------------------------------------------------------------------------""" % (
        inspect.trace()[i][1], 
        inspect.trace()[i][2], 
        inspect.trace()[i][3], 
        inspect.trace()[i][4])
        
        error_message = "%s%s" % (error_message, error_line)    
    
    error_message = """Error!
%s
%s
======================================== Error Message ====================================%s

======================================== Error Message ======================================================""" % (sys.exc_info()[0], sys.exc_info()[1], error_message)
    
    return error_message

if __name__=="__main__":    
    print map_function('set',alias_func = "ini_items")
    print map_function('set',fw_action_addtion="action_steps_",bw_action_addtion="_for_upd",alias_func = "ini_items")
    print map_function('set(a=1,b=2,c=Test())',"action_steps_","_for_upd","ini_items")
    print map_function('set("login",a="good",b=Test())',"action_steps_","_for_upd")  
    
    print find_data_files(r'E:\network\script_language\Python\test\py2pyd_Cython\usage2\pkg1', "pkg1", ["*"], True)