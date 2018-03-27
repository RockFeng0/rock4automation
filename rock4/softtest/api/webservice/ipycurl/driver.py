# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.api.webservice.ipycurl.driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.api.webservice.ipycurl.driver,v 1.0 2017年3月8日
    FROM:   2017年3月8日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''



import os,inspect,cStringIO
from rock4.common import p_env
import pycurl

class WebHttp():
    ''' web service test.(pycurl) '''
    
    def __init__(self):
        ''' initialize the object for curl '''
        self.__info_script_webhttp = os.path.abspath(inspect.getfile(inspect.currentframe()))
        self.__curl_path = p_env.BUFFER_PATH
        self.curl = pycurl.Curl()
        self.buf = cStringIO.StringIO()
        self.buf_string = ""
        self.http_info = {"handle":self.curl,"work_path":self.__curl_path}
    
    def __on_buf(self):
        if self.buf.closed:
            self.buf = cStringIO.StringIO()
    
    def __off_buf(self):
        self.buf.close()
    
    def get_cwork_dir(self):
        ''' get the work path of this http request '''
        return self.__curl_path
    
    def set_cwork_dir(self,f_dir):
        ''' set the work path of this http request '''
        f_dir = os.path.abspath(f_dir)
        if os.path.isdir(f_dir):
            self.__curl_path = f_dir
            self.http_info["work_path"] = f_dir
        else:
            raise Exception("\n\tp_web_http exception 1.0: invalid director '%s'." %(f_dir))
        
    def start(self):
        ''' perform the http request '''
        try:
            self.curl.perform()
        except Exception,e:
            raise Exception("\n\tp_web_http exception 3.1: performing error '%s'." %(e))
        try:
            if self.http_info.has_key("resp_output_file"):
                self.buf_string = self.buf.getvalue()
                with open(self.http_info["resp_output_file"],'wb') as fh:
                    fh.write(self.buf_string)
        except Exception,e:
            raise Exception("\n\tp_web_http exception 3.2: writing the buffer to file error '%s'." %(e))
        finally:
            self.__off_buf()    
            
    def set_req_url(self,url):
        ''' just url address that you want accecc 
        Sample url: http://127.0.0.1/login.html
        '''
        url = str(url)
        if url in (None,"None"):            
            return 
        
        self.http_info["req_url"] = url
        self.curl.setopt(self.curl.URL, url)
        
    def set_req_method(self,method):
        ''' GET、POST、PUT、DELETE etc. 
        Sample method: POST
        '''
        method = str(method).upper()
        if method in (None,"None"):
            return
        self.http_info["req_method"] = method
        self.curl.setopt(self.curl.CUSTOMREQUEST, method)
        
    def set_req_data(self,req_data):
        ''' post data with you specify %转义->%% 
        Sample req_data
        req_data = 'loginId=%s&referUrl=http%%3A%%2F%%2F192.168.102.204%%3A8012%%2Fcloudzone%%2Flogin&userId=%s&password=%s' %(loginId,userId,password)        
        '''
        req_data = str(req_data)
        if req_data in (None,"None"):            
            return
        self.http_info["req_data"] = req_data
        self.curl.setopt(self.curl.POSTFIELDS, req_data)        
    
    def set_req_uploadfile(self,upload_file,**formdata):
        '''post form data when upload files
        Sample usage:
            set_req_uploadfile(r"d:\auto\buffer\test.png",dirType="1",unzip="0")
            req_data is: [('test.png', (10, 'd:\\auto\\buffer\\test.png')), ('dirType', (4, '1')), ('unzip', (4, '0'))]
        
        '''
        if not os.path.isfile(upload_file):
            return   
        textname        = os.path.basename(upload_file)
        form_file       = [(textname, (self.curl.FORM_FILE, upload_file))]        
        form_content    = zip(formdata.keys(),[(self.curl.FORM_CONTENTS,"%s" %v) for v in formdata.values()])
        req_data        = form_file + form_content
#         print "--->",req_data
        self.curl.setopt(self.curl.HTTPPOST,req_data)
        
    def set_req_header(self,header):
        ''' add headers for the datagram 
        Sample header:
            header = ['X-Uid: 005056C0000820150407113046691','X-Request-Time: 2015-04-07 11:30:46','X-Client-Agent: Tianwen_PC/1.0','X-PC-Authenticate-key: AAAAAAAAAA',\
                    'X-Device-Id: 005056C00008','X-Device-Type: 4','X-Request-Platform: 10001000','X-Client-Language: zh_CN']        
        '''
        
        if header in (None,"None"):            
            return
        
        if not isinstance(header, list):            
            raise Exception("\n\tp_web_http exception 4.1: 'header' should be a list type.")
            return
                
        self.http_info["req_header"] = header     
        self.curl.setopt(self.curl.HTTPHEADER, header)
    
    def set_req_cookie(self,f_name,mode="new"):
        ''' set cookies to use '''
        f_name = str(f_name)
        if f_name in (None,"None"):            
            return
            
        abs_path = os.path.join(self.__curl_path,os.path.basename(f_name))
        self.http_info["req_cookie_file"] = abs_path
        if mode == "new":
#                 the effection is same as curl option -c which write cookies to this file after operation
            self.curl.setopt(self.curl.COOKIEJAR, abs_path)
        else:
#                 the effection is same as curl option -b(base on) which cookie string or file to read cookies from
            self.curl.setopt(self.curl.COOKIEFILE, abs_path)
        
    def set_req_referer(self,url):
        ''' set the referer URL. 
        Sample url: http://127.0.0.1/home.html
        '''
        url = str(url)
        if url in (None,"None"):                  
            return
        self.http_info["req_referer"] = url        
        self.curl.setopt(self.curl.REFERER,url)
    
    def set_req_useragent(self,agent):
        ''' set the browser useragent  
        Sample agent: 
            Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)           
            Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)
            Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)
        '''
        agent = str(agent)
        if agent in (None,"None"):            
            return 
        self.http_info["req_agent"] = agent
        self.curl.setopt(self.curl.USERAGENT,agent)        
    
    def set_req_proxy(self,url,userpwd=None):
        ''' set the proxy URL 
        Sample url: http://127.0.0.1:5820/proxy
        Sampel userpwd: 
            'administrator:showme'
        '''
        self.http_info["req_proxy"] = [url,userpwd]
        self.curl.setopt(self.curl.PROXY, url)
        if userpwd != None:
            self.curl.setopt(self.curl.PROXYUSERPWD, userpwd) 
    
    def set_output_verbose(self,switch):
        ''' this is a switch. Whether output more infomation for the response or not 
        Sample switch:
            True of False
        '''        
        if isinstance(type(switch), bool):
            self.http_info["verbose"] = switch
            self.curl.setopt(self.curl.VERBOSE, switch)
        else:
            raise Exception("\n\tp_web_http exception 2.0: Should be a 'BOOL' value(True or False).")
        
    def set_output_function(self,f_name,mode="write"):
        ''' define your preference of the output functions.
        the effection is same as curl option -o which write output to <file> instead of stdout
        '''
        abs_path = os.path.join(self.__curl_path,os.path.basename(f_name))
        self.http_info["resp_output_file"] = abs_path
        self.__on_buf()
        
        if mode == "header":
            # write the response header to a file
            self.curl.setopt(self.curl.HEADERFUNCTION,self.buf.write)
        else:
            # write the response body to a file
            self.curl.setopt(self.curl.WRITEFUNCTION, self.buf.write)
            
    def get_resp_code(self):
        ''' HTTP-code'''
        self.http_info["resp_code"] = self.curl.getinfo(self.curl.HTTP_CODE)
        return self.http_info["resp_code"]
    
    def get_resp_cookielist(self):
        ''' will print the cookie list if you have call "save_resp_cookie". '''
        self.http_info["resp_cookielist"] = self.curl.getinfo(self.curl.INFO_COOKIELIST)
        return self.http_info["resp_cookielist"]

    def get_resp_contType(self):
        ''' Content-type '''
        self.http_info["resp_contype"] = self.curl.getinfo(self.curl.CONTENT_TYPE)
        return self.http_info["resp_contype"]
    
    def get_resp_totalTime(self):
        ''' Total-time '''
        self.http_info["resp_totaltime"] = self.curl.getinfo(self.curl.TOTAL_TIME)
        return self.http_info["resp_totaltime"]
        
    def get_resp_nsTime(self):
        ''' Namelookup-time '''        
        self.http_info["resp_nstime"] = self.curl.getinfo(self.curl.NAMELOOKUP_TIME)
        return self.http_info["resp_nstime"]
      
    def get_resp_dSpeed(self):
        ''' Download speed(bytes/second) '''
        self.http_info["resp_dspeed"] = self.curl.getinfo(self.curl.SPEED_DOWNLOAD)
        return self.http_info["resp_dspeed"]
    
    def get_resp_dSize(self):
        ''' Download document size(bytes) ''' 
        self.http_info["resp_dsize"] = self.curl.getinfo(self.curl.SIZE_DOWNLOAD)
        return self.http_info["resp_dsize"]
    
    def get_resp_uSpeed(self):
        ''' Upload speed(bytes/second) '''
        self.http_info["resp_uspeed"] = self.curl.getinfo(self.curl.SPEED_UPLOAD)
        return self.http_info["resp_uspeed"]
    
    def get_resp_uSize(self):
        ''' Upload document size(bytes) '''
        self.http_info["resp_usize"] = self.curl.getinfo(self.curl.SIZE_UPLOAD)
        return self.http_info["resp_usize"]
    
    def get_resp_eURL(self):
        ''' Effective URL '''
        self.http_info["resp_eURL"] = self.curl.getinfo(self.curl.EFFECTIVE_URL)
        return self.http_info["resp_eURL"]        
    
    def get_resp_reDirTime(self):
        ''' Redirect-time '''
        self.http_info["resp_redirectTime"] = self.curl.getinfo(self.curl.REDIRECT_TIME)
        return self.http_info["resp_redirectTime"]
    
    def get_resp_reDirCount(self):
        ''' Redirect-count '''
        self.http_info["resp_redirectCount"] = self.curl.getinfo(self.curl.REDIRECT_COUNT)
        return self.http_info["resp_redirectCount"]
    
def usage_for_webservice():
    # define
    method = 'POST'
    ip = "192.168.102.241"
    upload_url='http://%s:8008/dls/FileStorage/httpUploadFile' %ip    
    buffer_path = r"d:\auto\buffer"
    upload_file = r"%s\test.png" %buffer_path    
    
    loginId = 'YnJ1Y2V0ZWFjaGVy';#base64-> bruceteacher
    userId = 'bruceteacher'
    password = 'MTIzNDU2';#base64-> 123456
    req_data = 'loginId=%s&referUrl=http%%3A%%2F%%2F192.168.102.204%%3A8012%%2Fcloudzone%%2Flogin&userId=%s&password=%s' %(loginId,userId,password)
    
    # request
    a=WebHttp()
    #设置工作目录，buffer和其他文件，都会丢在这个目录下面
    a.set_cwork_dir(buffer_path)
    a.set_req_url(upload_url)
    a.set_req_method(method)
    a.set_req_data(req_data)
    a.set_req_cookie("cookie.tmp")    
    a.set_output_function("t.html","header")
    a.set_output_function("t.html")
    a.set_req_uploadfile(upload_file, dirType="1", unzip="0")
    
    
    # perform
    a.start()
    # response
    print "HTTP-code:", a.get_resp_code()
    print "Total-time:", a.get_resp_totalTime()
    print "Content-type:", a.get_resp_contType()   
    print "Download speed: %.2f bytes/second" %a.get_resp_dSpeed()    
    print "Document size: %d bytes" %a.get_resp_dSize()
    print "Effective URL:", a.get_resp_eURL()
    print "Namelookup-time:", a.get_resp_nsTime()
    print "Redirect-time:", a.get_resp_reDirTime()
    print "Redirect-count:", a.get_resp_reDirCount()
    
    print a.http_info
    print a.buf_string

def usage_for_webservice2():
    ####  curl SVN files
    # curl -u luokefeng:lkf890 http://192.168.111.244/svn/aischool/doc/02.%E7%BB%84%E7%BB%87%E6%96%87%E6%A1%A3/04.%E6%B5%8B%E8%AF%95%E7%BB%84/%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95/%E4%B8%AA%E4%BA%BA%E6%96%87%E4%BB%B6%E5%A4%B9/tools/instenv/
    
    import base64,urllib
        
    def quoteurl(url):
        '''Sample usage:
            quoteurl(u'http://192.168.111.244/svn/aischool/doc/02.组织文档/04.测试组/自动化测试/个人文件夹/tools/instenv/')
            Return: 'http://192.168.111.244/svn/aischool/doc/02.%E7%BB%84%E7%BB%87%E6%96%87%E6%A1%A3/04.%E6%B5%8B%E8%AF%95%E7%BB%84/%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95/%E4%B8%AA%E4%BA%BA%E6%96%87%E4%BB%B6%E5%A4%B9/tools/instenv/'
        '''
        if not isinstance(url, unicode):
            return
        s = url.encode("utf-8").split(":",1)
        s[1] = urllib.quote(s[1])
        url = ":".join(s)
        return url    
    
    u = base64.b64encode("luokefeng:lkf890")
    url = quoteurl(u'http://192.168.111.244/svn/aischool/doc/02.组织文档/04.测试组/自动化测试/个人文件夹/tools/instenv/')
    method = 'GET'
    
    # curl list
    a=WebHttp()    
    a.set_cwork_dir(r"d:\auto\buffer")
    a.set_req_method(method)
    a.set_req_header(['Authorization: Basic %s' %u])
    a.set_req_url(url)
    a.set_output_function("t.html","header")
    a.set_output_function("t.html")
    a.start()
    print a.buf_string
    print "HTTP-code:", a.get_resp_code()
    
    # download file
    url = quoteurl(u'http://192.168.111.244/svn/aischool/doc/02.组织文档/04.测试组/自动化测试/个人文件夹/tools/instenv/CCE-ECP环境自动安装工具使用手册.docx')
    a=WebHttp()
    a.set_cwork_dir(r"d:\auto\buffer")
    a.set_req_method(method)
    a.set_req_header(['Authorization: Basic %s' %u])
    a.set_req_url(url)
    a.set_output_function(u"CCE-ECP环境自动安装工具使用手册.docx")
    a.start()
    print "download file complete."
    print "HTTP-code:", a.get_resp_code()


if __name__ == '__main__':    
#     usage_for_webservice()
    usage_for_webservice2()