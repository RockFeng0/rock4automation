# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.api.webservice.irequests.actions

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.api.webservice.irequests.actions,v 1.0 2017年3月8日
    FROM:   2017年3月8日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


import requests,os,re,json
from requests.auth import HTTPBasicAuth,HTTPDigestAuth

class WebHttp():
    head, data = None, None
    __glob = {}
    __resp = None
    __auth = None
    
    @classmethod
    def SetVar(cls, name, value):
        ''' set static value
        :param name: glob parameter name
        :param value: parameter value
        '''
        cls.__glob.update({name:value})
    
    @classmethod
    def DyStrData(cls,name, regx, index = 0):
        ''' set dynamic value from the string data of response  
        :param name: glob parameter name
        :param regx: regular expression
        '''
        if not cls.__resp:
            return
        comp = re.compile(regx)
        values = comp.findall(cls.__resp)
        result = ""
        if len(all)>index:
            result = values[index]        
        cls.__glob.update({name:result})
    
    @classmethod
    def DyJsonData(cls,name, sequence=[]):
        ''' set dynamic value from the json data of response  
        :param name: glob parameter name
        :param sequence: sequence for the json
        '''
        if not cls.__resp:
            return
        resp = json.loads(cls.__resp)
        for i in sequence:            
            resp = resp.get(i)
            if not resp:
                break
        cls.__glob.update({name:json.dumps(resp)})
            
    @classmethod
    def GetVar(cls, name):
        return cls.__glob.get(name)
    
    @classmethod
    def LoginAuth(cls,username,password,auth):
        '''
        :auth: [basic/digest] encrypt to base64 or md5
        '''
                
        if auth == "basic":
            cls.__auth = HTTPBasicAuth(username, password)
        elif auth == "digest":
            cls.__auth = HTTPDigestAuth(username, password)    
    
    @classmethod
    def GET(cls, url):
        '''
        :简化get
        :param url: request url 
        '''        
        cls.__resp = requests.get(url, auth = cls.__auth)
        cls.__auth = None
        
    @classmethod
    def POST(cls, url, datatype="raw"):
        '''
        :简化post
        :param datatype: [raw/json] request the data with Content-type[x-www-form-urlencoded] or Content-type[json]         
        '''
        # cls.head type is dict 
        if cls.head and not isinstance(cls.head, dict):
            try:
                cls.head = json.loads(cls.head)
            except:
                cls.head = None
        
        if datatype.lower() == "raw":
            cls.__resp = requests.post(url, headers = cls.head, data = cls.data, auth = cls.__auth)
        elif datatype.lower() == "json":
            cls.__resp = requests.post(url, headers = cls.head, json = cls.data, auth = cls.__auth)
        cls.head, cls.data = None, None
        cls.__auth = None

    @classmethod
    def Download(cls, url, dst, stream = None):
        ''' save response body/content/text to a file
        :param url: download url
        :param stream: True/False or None, if False or None, response body will be immediately download; if True, will be hung up untill the all data in Response.content is read.
        :param dst: the full path or the full path file  
        '''                
        cls.__resp = requests.get(url,stream = stream, auth = cls.__auth)
        cls.__auth = None
        
        if os.path.isdir(dst):
            f_abspath = os.path.join(dst, os.path.basename(url))
        else:
            f_abspath = dst
        with open(f_abspath, 'wb') as fd:
            if stream: 
                for chunk in cls.__resp.iter_content():
                    fd.write(chunk)
            else:
                fd.write(cls.__resp.text.encode(cls.__resp.encoding))   
    
    @classmethod
    def Upload(cls,url, upload_files, **formdata):
        '''usage:
            url = 'http://192.168.102.241:8008/dls/FileStorage/httpUploadFile'
            upload_files = [r'd:\auto\buffer\t.jpg',r'd:\auto\buffer\t.zip']
            upload(url, upload_files, dirType = 1, unzip = 0)
        '''                
        multiple_files = {}
        for f in upload_files:
            if not os.path.isfile(f):
                continue
            multiple_files.update({os.path.basename(f):open(f, 'rb')})
                            
        if not formdata:
            formdata = None                    
        cls.__resp = requests.post(url, data = formdata, files = multiple_files, auth = cls.__auth)
        cls.__auth = None   
    
    
    @classmethod
    def VerifyContain(cls, strs):
        if strs in cls.GetRespText():
            return True
        else:
            return False
    
    @classmethod
    def VerifyCode(cls, code):
        try:
            code = int(code)
        except:
            return False
        
        if cls.GetRespCode() == code:
            return True
        else:
            return False
        
    @classmethod
    def GetRespCode(cls):
        ''' HTTP-code'''
        return cls.__resp.status_code
    
    @classmethod
    def GetRespReason(cls):
        '''Textual reason of responded HTTP Status, e.g. "Not Found" or "OK". '''
        return cls.__resp.reason
    
    @classmethod
    def GetRespCookie(cls):
        ''' will print the cookie dict '''
        return dict(cls.__resp.cookies.items())

    @classmethod
    def GetRespHeaders(cls):
        ''' response headers '''
        return cls.__resp.headers
    
    @classmethod
    def GetRespEncoding(cls):
        ''' response encoding '''
        return cls.__resp.encoding
    
    @classmethod
    def GetRespText(cls):
        ''' Content of the response, in unicode '''
        return cls.__resp.text
    
    @classmethod
    def GetRespContent(cls):
        ''' Content of the response, in bytes '''
        return cls.__resp.text
    
    @classmethod
    def GetRespElapsed(cls):
        ''' the time between sending request and the arrival of the response '''
        return cls.__resp.elapsed
    
    @classmethod
    def GetReqMethod(cls):
        ''' request method'''
        return cls.__resp.request.method
     
    @classmethod
    def GetReqUrl(cls):
        ''' request url'''
        return cls.__resp.request.url
    
    @classmethod
    def GetReqHeaders(cls):
        ''' request headers '''
        return cls.__resp.request.headers
    
    @classmethod
    def GetReqData(cls):
        ''' request body '''
        return cls.__resp.request.body   
                
       
#### not suggest to use
from rock4.common import p_env
class SimpleWebHttp():
    ''' web service test.(requests) '''
    
    def __init__(self,keep_session = False):
        self.__curl_path = p_env.BUFFER_PATH
        self.__req = {}
        self.__resp = None
        self.session = None
        if keep_session:
            self.session = requests.Session()        
        
    def get_cwork_dir(self):
        ''' get the work path of this http request '''
        return self.__curl_path
    
    def set_cwork_dir(self,f_dir):
        ''' set the work path of this http request '''
        f_dir = os.path.abspath(f_dir)
        if os.path.isdir(f_dir):
            self.__curl_path = f_dir            
        else:
            raise Exception("\n\tSimpleWebHttp exception 1.0: invalid director '%s'." %(f_dir))
    
    def set_http_base_auth(self, username,password):
        ''' Username and password send data with Base64 encoding. e.g. SVN is HttpBaseAuth '''
        self.__req["auth"] = HTTPBasicAuth(username, password)
            
    def set_http_digest_auth(self, username, password):
        ''' Username and password send data with hash MD5 encoding. '''
        self.__req["auth"] = HTTPDigestAuth(username, password)    
     
    def get(self,url,verify = True, cert = None, cookies=None, stream = None):
        '''usage:
            s = SimpleWebHttp()
            url= 'http://www.baidu.com'
            url2 = 'https://www.baidu.com'
            print s.get(url)            
            print s.get(url2,verify = True);# https SSL验证            
            print s.get(url2,verify = False, );# https 跳过SSL验证            
            # print s.get(url2,cert=r'C:\license\CNSHYY5_20161011.cer');# https, 单个文件，包含证书和密钥            
            # print s.get(url2,cert=(r'C:\license\CNSHYY5_20161011.cer',r'C:\license\CNSHYY5_20161011.key'));# https, #两个文件，tuple(cer,key)
            print s.get(url, cookies={'testCookies_1': 'Hello_Python3', 'testCookies_2': 'Hello_Requests'})
        '''
        self.__req.update({"verify":verify,
                           "cert":cert,
                           "cookies":cookies,
                           "stream":stream,
                           })
        return self.__requests("get", url, **self.__req)    
        
    def post(self,url,headers=None,data=None, cookies=None):
        self.__req["headers"] = headers
        self.__req["data"] = data
        self.__req["cookies"] = cookies        
            
        return self.__requests("post", url, **self.__req)
        
    def download(self,url, stream = None, name=None):
        ''' save response body/content/text to a file
            if stream is False or None, then response body will be immediately download
            if stream is True, then will be hung up untill the all data in Response.content is read.   
        '''        
        if name:
            f_name = name
        else:
            f_name = os.path.basename(url)                    
        f_abspath = os.path.join(self.__curl_path,f_name)   
        print f_abspath
        self.get(url,stream = stream)        
        with open(f_abspath, 'wb') as fd:
            if stream: 
                for chunk in self.__resp.iter_content():
                    fd.write(chunk)
            else:
                fd.write(self.__resp.text.encode(self.__resp.encoding))  
    
    def upload(self,url, upload_files, **formdata):
        '''usage:
            url = 'http://192.168.102.241:8008/dls/FileStorage/httpUploadFile'
            upload_files = [r'd:\auto\buffer\t.jpg',r'd:\auto\buffer\t.zip']
            upload(url, upload_files, dirType = 1, unzip = 0)
        '''
        multiple_files = {}
        for f in upload_files:
            if not os.path.isfile(f):
                continue
            multiple_files.update({os.path.basename(f):open(f, 'rb')})
                            
        if not formdata:
            formdata = None
        
        self.__req["files"] = multiple_files
        return self.post(url, data = formdata)           
        
    def get_resp_code(self):
        ''' HTTP-code'''
        return self.__resp.status_code
    
    def get_resp_reason(self):
        '''Textual reason of responded HTTP Status, e.g. "Not Found" or "OK". '''
        return self.__resp.reason
    
    def get_resp_cookie(self):
        ''' will print the cookie dict '''
        return dict(self.__resp.cookies.items())

    def get_resp_headers(self):
        ''' response headers '''
        return self.__resp.headers
        
    def get_resp_encoding(self):
        ''' response encoding '''
        return self.__resp.encoding
    
    def get_resp_text(self):
        ''' Content of the response, in unicode '''
        return self.__resp.text
    
    def get_resp_content(self):
        ''' Content of the response, in bytes '''
        return self.__resp.text
    
    def get_resp_elapsed(self):
        ''' the time between sending request and the arrival of the response '''
        return self.__resp.elapsed
    
    def get_req_method(self):
        ''' request method'''
        return self.__resp.request.method
     
    def get_req_url(self):
        ''' request url'''
        return self.__resp.request.url
       
    def get_req_headers(self):
        ''' request headers '''
        return self.__resp.request.headers
    
    def get_req_data(self):
        ''' request body '''
        return self.__resp.request.body    
    
    def __requests(self,obj,*args,**kwargs):
        if self.session:
            self.__resp = getattr(self.session, obj)(*args,**kwargs)
        else:
            self.__resp = getattr(requests, obj)(*args,**kwargs)
        print self.__req
        self.__req = {}
        return self.__resp
    
    def close(self):
        if not self.session:
            return
        self.session.close()

def usage_SimpleWebHttp():
    s = SimpleWebHttp()
    
    ### get
    print "============= get"
    url= 'http://www.baidu.com'
    url2 = 'https://www.baidu.com'
    print s.get(url)
    print s.get(url2,verify = False)
    print s.get(url, cookies={'testCookies_1': 'Hello_Python3', 'testCookies_2': 'Hello_Requests'})
    try:
        print s.get('https://www.baidu.com',verify = True)
        # print s.get(url2,cert=r'C:\license\CNSHYY5_20161011.cer');# https, 单个文件，包含证书和密钥            
        # print s.get(url2,cert=(r'C:\license\CNSHYY5_20161011.cer',r'C:\license\CNSHYY5_20161011.key'));# https, #两个文件，tuple(cer,key)
    except Exception,e:
        print e
        
    ### post
    print "============= post"
    url = 'http://192.168.102.241:8003/manager/eeducation/BaseService'
    head = {"Content-Type": "text/x-gwt-rpc; charset=utf-8","x-gwt-permutation": "9FE14770B4D552EFFB9CE5571ACACFDE"}
    logindata = '7|0|18|http://192.168.102.241:8003/manager/eeducation/|A6B7631C6D018783FF117FDE78D1672B|com.tianwen.Base.client.service.BaseManagerService|doLogin|com.tianwen.Base.client.model.LoginModel/1269075523|com.extjs.gxt.ui.client.data.RpcMap/3441186752|userName|java.lang.String/2004016611|administrator|password|123456|orgId||checkCode|0000|locale|isFirstLogin|1|1|2|3|4|1|5|5|1|6|6|7|8|9|10|8|11|12|8|13|14|8|15|16|-5|17|8|18|'
    #logoutdata = '7|0|4|http://192.168.102.241:8003/manager/eeducation/|A6B7631C6D018783FF117FDE78D1672B|com.tianwen.Base.client.service.BaseManagerService|doLogout|1|2|3|4|0|'
    
    print s.post(url,data = logindata,headers = head)    
    print "response text: %s" %s.get_resp_text()
    print 'response content: %r' %s.get_resp_content()
    print "return code: %s" %s.get_resp_code()
    print "return reason: %s" %s.get_resp_reason()
    print "response head: %s" %s.get_resp_headers()    
    print 'response elapsed: %r' %s.get_resp_elapsed()
    print 'response encoding: %r' %s.get_resp_encoding()
    print 'cookies: %r' %s.get_resp_cookie()
    
    ### upload
    print "============= upload"
    upload_url='http://192.168.102.241:8008/dls/FileStorage/httpUploadFile'
    upload_file1 = r"d:\auto\buffer\test.xml"
    upload_file2 = r"d:\auto\buffer\t.html"    
    print s.upload(upload_url, [upload_file1,upload_file2], dirType = 1, unzip = 0)
    print s.get_resp_code()

    ### download
    print "============= download svn"
    url = u'http://192.168.111.244/svn/aischool/doc/02.组织文档/04.测试组/自动化测试/个人文件夹/tools/instenv/CCE-ECP环境自动安装工具使用手册.docx'
    s.set_cwork_dir(r"d:\auto\buffer")
    s.set_http_base_auth("luokefeng", "lkf890")       
    s.download(url,stream=True)
    print s.get_resp_code(), s.get_resp_reason()
    
    print "============= download normal"
    url = "http://www.baidu.com"
    s.download(url,name = 'baidu.html')
    print s.get_resp_code()
    
    ### session
    s = SimpleWebHttp(keep_session=True)
    s.get("http://www.baidu.com")
    print s.get_resp_cookie()
    s.get("http://www.baidu.com/baidu?wd=你好&tn=cnopera&ie=utf-8")
    print s.get_resp_cookie()
    
def usage_WebHttp():    
    ### get
    print "============= get"    
    WebHttp.GET("http://www.baidu.com")
    print WebHttp.GetRespCode()
            
    ### post
    print "============= post"
    url = 'http://192.168.102.241:8003/manager/eeducation/BaseService'
    head = {"Content-Type": "text/x-gwt-rpc; charset=utf-8","x-gwt-permutation": "9FE14770B4D552EFFB9CE5571ACACFDE"}
    logindata = '7|0|18|http://192.168.102.241:8003/manager/eeducation/|A6B7631C6D018783FF117FDE78D1672B|com.tianwen.Base.client.service.BaseManagerService|doLogin|com.tianwen.Base.client.model.LoginModel/1269075523|com.extjs.gxt.ui.client.data.RpcMap/3441186752|userName|java.lang.String/2004016611|administrator|password|123456|orgId||checkCode|0000|locale|isFirstLogin|1|1|2|3|4|1|5|5|1|6|6|7|8|9|10|8|11|12|8|13|14|8|15|16|-5|17|8|18|'
    #logoutdata = '7|0|4|http://192.168.102.241:8003/manager/eeducation/|A6B7631C6D018783FF117FDE78D1672B|com.tianwen.Base.client.service.BaseManagerService|doLogout|1|2|3|4|0|'
    
    WebHttp.head = head
    WebHttp.data = logindata
    WebHttp.POST(url, datatype="raw")
    print "response text: ", WebHttp.GetRespText()
    print 'response content: ', WebHttp.GetRespContent()
    print "return code: ", WebHttp.GetRespCode()
    print "return reason: ", WebHttp.GetRespReason()
    print "response head: ", WebHttp.GetRespHeaders()    
    print 'response elapsed: ', WebHttp.GetRespElapsed()
    print 'response encoding: ', WebHttp.GetRespEncoding()
    print 'cookies: ', WebHttp.GetRespCookie()
    
    ### upload
    print "============= upload"
    upload_url='http://192.168.102.241:8008/dls/FileStorage/httpUploadFile'
    upload_file1 = r"d:\auto\buffer\test.xml"
    upload_file2 = r"d:\auto\buffer\t.html"
    WebHttp.Upload(upload_url, [upload_file1,upload_file2], dirType = 1, unzip = 0)
    print WebHttp.GetRespCode()

    ### download
    print "============= download svn"
    url = u'http://192.168.111.244/svn/aischool/doc/02.组织文档/04.测试组/自动化测试/个人文件夹/tools/instenv/CCE-ECP环境自动安装工具使用手册.docx'
    
    WebHttp.LoginAuth("luokefeng", "lkf890", "basic")       
    WebHttp.Download(url, r'd:\auto\buffer', stream=True)
    print WebHttp.GetRespCode(), WebHttp.GetRespReason()
    
    print "============= download normal"
    url = "http://www.baidu.com"
    WebHttp.Download(url,r'd:\auto\buffer\baidu.html')
    print WebHttp.GetRespCode()
    
    ### parameterization
    WebHttp.SetVar("url", "http://www.baidu.com")
    WebHttp.GET("#url#")
    print WebHttp.GetRespCode()
    
if __name__ == "__main__":
    usage_WebHttp()

    
    
    