# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.idleshell.diyrpc

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.common.dev.idleshell.diyrpc,v 2.0 2017年2月7日
    FROM:   2016年8月16日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import time,socket,sys,os,types
from code import InteractiveInterpreter
from idlelib import PyShell, rpc, IOBinding
from idlelib.configHandler import idleConf

HOST = "127.0.0.1"
PORT = 0

class TkAsyncUpdate:    
    ''' Update Tk UI when MyInterp.poll_subprocess get a response. '''
    
    def update(self, poll_response):
        ''' can be override '''
        if poll_response:
            how, what = poll_response
            if how == "OK":
                if what is not None:
                    print "ok:",repr(what)
            elif how == "EXCEPTION":
                print "exception:",repr(what)
            elif how == "ERROR":
                errmsg = "PyShell.ModifiedInterpreter: Subprocess ERROR:\n"
                print "error:",errmsg, what
            
class MyInterp(InteractiveInterpreter):
    
    def __init__(self, tkconsole, tkasyc=TkAsyncUpdate()):        
        self.tkconsole = tkconsole
        self.tkasyc = tkasyc
        now_locals = sys.modules['__main__'].__dict__
        InteractiveInterpreter.__init__(self, locals=now_locals)        
        self.subprocess_arglist = None
        self.active_seq = None
    
    ### subprocess method refer to PyShell. 
    def start_subprocess(self, api_file_path, addr=None):   
        ''' start a subprocess to run the RPC server '''
        self.p, self.m = self.__split_api_file(api_file_path)
        
        if not addr:
            addr = (HOST, PORT)
            
        for i in range(3):
            time.sleep(i)
            try:
                self.rpcclt = rpc.RPCClient(addr)
                break
            except socket.error, err:
                pass
        else:
            print "No connection with %s" %addr
            return None
            
        self.port = self.rpcclt.listening_sock.getsockname()[1]
        print "<MainCpyStart: %s>" %self.port
        if PORT != 0:
            self.rpcclt.listening_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # RPC Server
        # start run.main() in subprocess
        # It's a SocketServer which override some methods of SocketServer.TCPServer and write a loop to deal with the request of Queue.
        self.spawn_subprocess() 
        
        self.rpcclt.listening_sock.settimeout(10)
        try:
            # RPC Client
            # accept the connection of run.main()
            # It's a server of socket in main process and inherit SockIO which define the rules of sending request and polling response            
            self.rpcclt.accept()
        except socket.timeout, err:
            print "No subprocess connected."
            return None
        
        # out put will be directed to tkconsole
        self.set_output_direction(output_out=self.tkconsole, output_err= self.tkconsole)
        
        self.poll_subprocess()
        return self.rpcclt
    
    def spawn_subprocess(self):
        if self.subprocess_arglist is None:
            self.subprocess_arglist = self.build_subprocess_arglist()
        args = self.subprocess_arglist
        self.rpcpid = os.spawnv(os.P_NOWAIT, sys.executable, args)
        
    def build_subprocess_arglist(self):
        ''' Overwrite build_subprocess_arglist 
            Actually this method is to call a subprocess to run RPC server's main.
        '''
        
        assert (self.port!=0), (
            "Socket should have been assigned a port number.")
        w = ['-W' + s for s in sys.warnoptions]
        if 1/2 > 0: # account for new division
            w.append('-Qnew')
        # Maybe IDLE is installed and is being accessed via sys.path,
        # or maybe it's not installed and the idle.py script is being
        # run from the IDLE source directory.
        del_exitf = idleConf.GetOption('main', 'General', 'delete-exitfunc',
                                       default=False, type='bool')
#         command = "__import__('sys').path.append(%r);__import__('diyrun').main(%r)" % (os.path.dirname(os.path.abspath(__file__)), del_exitf,)                
        command = "__import__('sys').path.extend([%r,%r]);__import__('diyoid').oidmap.map_module_objs(%r);__import__('diyrun').main(%r)" %(os.path.dirname(os.path.abspath(__file__)), self.p, self.m, del_exitf,)
        
        if sys.platform[:3] == 'win' and ' ' in sys.executable:
            # handle embedded space in path by quoting the argument
            decorated_exec = '"%s"' % sys.executable
        else:
            decorated_exec = sys.executable
        return [decorated_exec] + w + ["-c", command, str(self.port)]
    
    def set_output_direction(self, output_in = sys.stdin, output_out = sys.stdout, output_err = sys.stderr):
        ''' redirecte the output '''
        self.rpcclt.register("stdin", output_in)        
        self.rpcclt.register("stdout", output_out)        
        self.rpcclt.register("stderr", output_err) 
    
    def poll_subprocess(self):
        clt = self.rpcclt
        if clt is None:
            return
        try:
            # idlelib.rpc.pollresponse will loop until a response message that received on the socket
            response = clt.pollresponse(self.active_seq, wait=0.05)
                
        except (EOFError, IOError, KeyboardInterrupt):
            response = None
            
        if response:
            self.active_seq = None            
        self.tkasyc.update(response)
            
        # 避免 ui 未响应， 使用  after命令-->  ui 'after' command is useful for avoiding the UI blocking.
        #self.text.after(50,self.poll_subprocess);# Tcl/tk after命令， text_ui对象，50毫秒 回调 
        self.tkconsole.text.after(self.tkconsole.pollinterval, self.poll_subprocess)
        
    ### override InteractiveInterpreter methods
    def runsource(self, source, symbol = "single"):
        "Extend base class method: encode the source"
        filename = '<diyrpc shell>'        
        if isinstance(source, types.UnicodeType):
            from idlelib import IOBinding
            try:
                source = source.encode(IOBinding.encoding)
            except UnicodeError:
                self.write("Unsupported characters in input\n")
                return
        try:          
            return InteractiveInterpreter.runsource(self, source, filename, symbol)
        finally:
            pass

    def runcode(self, code):
        "Override base class method, running code without block or hang UI."
        try:
            if self.rpcclt is not None:                
                self.active_seq = self.rpcclt.asyncqueue("exec", "runcode",
                                                        (code,), {})
            else:
                exec code in self.locals
        except Exception,e:
            print e
    
    def showsyntaxerror(self, filename=None):
        """Extend base class method """
        InteractiveInterpreter.showsyntaxerror(self, filename)
            
    def showtraceback(self):
        "Extend base class method to reset output properly"        
        InteractiveInterpreter.showtraceback(self)
            
    def write(self, s):
        "Override base class method"
        self.tkconsole.stderr.write(s)
        
    ###  others
    def extend_namespace(self, api_file_path):
        ''' Import module in RPC_Server's locals namespace, so that we can auto complete the string base on the module. '''
        p, m = self.__split_api_file(api_file_path)
        self.rpcclt.remotequeue('exec', 'runcode', ('''
import sys
if not "%s" in sys.path:
    sys.path.append("%s")
from %s import *''' %(p, p, m),
        ) , {})
        
    def __split_api_file(self,api_file_path):
        ''' split file to (path,module_name) '''
        if not os.path.isfile(api_file_path):
            raise Exception("Invalid file '%s'" %api_file_path)
        
        p,f = os.path.split(os.path.abspath(api_file_path))
        m,e =os.path.splitext(f)
        
        if not e in (".py",".pyc",".pyo"):
            raise Exception("Invalide file type: '%s'" %e)        
        return (p,m) 
    
class MyRpcClient():    
    def __init__(self, rpcclt):
        self.rpcclt = rpcclt
               
    def send_code_obj_req(self, filename,source = None):
        ''' execute the py program in RPC server '''
        if source is None:
            source = open(filename, "r").read()
        code = compile(source, filename, "exec")
        
        # idlelib.rpc.getresponse will wait for the funtion's result.
        return self.rpcclt.remotequeue("exec", "runcode", (code,), {})
    
    def register(self, oid ,obj):
        ''' register an alias to obj in the RPC client '''
        self.rpcclt.register(oid, obj)
    
    def remotequeue(self, oid, methodname, args, kwargs):
        ''' 'queue' requests are used for tasks (which may block or hang) to be processed in a different thread.
            Parameter:
                 oid is an alias of class which is lowwer of class name.
                 methodname is method name of class.
                 args and kwargs is methed parameters
            Return:
                process will be blocked until the function return a result
        '''
        
        # idlelib.rpc.getresponse will wait for the funtion's result.
        return self.rpcclt.remotequeue(oid, methodname, args, kwargs)
        
    def remotecall(self, oid, methodname, args, kwargs):
        ''' 'call' requests are passed to self.localcall() with the expectation of immediate execution, during which time the socket is not serviced.
            Parameter:
                 oid is an alias of class which is lowwer of class name.
                 methodname is method name of class.
                 args and kwargs is methed parameters
            Return:
                result of immediate execution, during which time the socket is not serviced. (which may also block or hang)
        '''
        
        # idlelib.rpc.getresponse will wait for the funtion's result.
        return self.rpcclt.remotecall(oid, methodname, args, kwargs)

class TkConsole():
    ''' In order to act as a output console with Tk-Text, this class is define some methods of "write writelines flush".'''
    def __init__(self, tk_text):
        self.text = tk_text
        self.pollinterval = 50
        self.stdout = PyShell.PseudoFile(shell = self, tags = "stdout", encoding = IOBinding.encoding)
        self.stderr = PyShell.PseudoFile(shell = self, tags = "stderr", encoding = IOBinding.encoding)
        self.console = PyShell.PseudoFile(shell = self, tags = "console", encoding = IOBinding.encoding)
    
    def write(self, s, tags = (), mark = "end"):
        ### if string is not using default system code.
        self.text.insert(mark, s, tags)
        
#         ### decode to unicode if string is using default system code.
#         if isinstance(s, str):            
#             try:
#                 s = unicode(s, IOBinding.encoding)
#             except UnicodeError:
#                 # some other encoding; let Tcl deal with it
#                 pass             
#         self.text.insert(mark, s, tags)
        
        self.text.see(mark)
        self.text.update()
        
    def writelines(self, lines):
        for line in lines:
            self.write(line)
    
    def flush(self):
        pass
    
    def isatty(self):
        return True

#### 示例一： RPC远程调用 runcode，并对输出重定向到 标准输入，输出，错误  
def start_example():
    ''' d:\auto\buffer\sdf.py:
            class Asdf:
                def __init__(self):
                    self.hh = "Now in Asdf()"
                             
                def sdfs2(self,*args,**kwargs):
                    print self.hh
                    print args,kwargs
        test2.py:
            print "Now in running file: test2.py"
            print "====呵呵"
    '''
    
    from Tkinter import Tk,Text    
    root = Tk()
    text = Text(root)
    text.pack()
    
    tkconsole = TkConsole(text)
    
    ### run code and not block the Tk
    api_file = r"d:\auto\buffer\sdf.py"
    intp = MyInterp(tkconsole)
    intp.start_subprocess(api_file)
    
    # 默认执行 一行命令
    intp.runsource("print +_+_+_+_语法错误信息的重定向示例'")
    intp.runsource("import time;time.sleep(3);print '你哈'")
    intp.runsource("time.sleep(3)")
    intp.runsource("print '+_+_+_+_哈哈哈'")
    # 执行多行命令, symbol = "exec"
    intp.runsource("""
a = 'hello world'
if True:
    print a
else:
    print "oh no"
""", symbol= "exec")
    
            
    ### run code and block the tk
#     run_file = r"d:\auto\buffer\test2.py"
#     clt = MyRpcClient(intp.rpcclt)
#     
#     # 获取定义的 var值
#     result = clt.remotequeue("exec", "poll_var", ('a'), {})
#     print "poll_var result:", result
#     
#     result1 = clt.send_code_obj_req(filename = "test-Text",source = u'print "running here"')
#     result2 = clt.send_code_obj_req(filename = run_file)
#     print "send_code_obj_req result: %r %r" %(result1,result2)
#     
#     result3 = clt.remotequeue("exec", "runcode", ("import time;time.sleep(3);print 'Block end'",), {})
#     print "runcode result:", result3
#     
#     result4 = clt.remotecall("asdf", "sdfs2", ("print 'remote call for Asdf'",), {})
#     print "sdfs2 result:", result4       
    
    root.mainloop()
    
if __name__ == "__main__":
    start_example()
