# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.idleshell.diyrun

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.common.dev.idleshell.diyrun,v 2.0 2017年2月7日
    FROM:   2016年8月16日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import time,socket,sys,thread,threading,Queue,traceback
from diyoid import oidmap
from idlelib import run,rpc
from SimpleAutoComplete import SimpleAutoComplete


class MyExecuteve(run.Executive):
    def __init__(self,rpchandler):
        run.Executive.__init__(self, rpchandler)
        self.autocomplete = SimpleAutoComplete(debug = False)
    
    def poll_var(self, item, subobj=""):        
        if not item in self.locals:
            return
               
        var = self.locals.get(item)
        if not subobj:
            return var
        
        # poll_var("obj", "getValue()")
        return eval("var.%s" %subobj)
    
    
class MyHandler(rpc.RPCHandler):
        
    def handle(self):
        """Override base method"""
        oid_map_class = oidmap.get_oid_map()
        oid_map_class["exec"] = MyExecuteve(self)   
        for k,v in oid_map_class.items():
            self.register(k, v)
        
        # reload sys module. and set encoding to utf-8 
        reload(sys);getattr(sys,"setdefaultencoding")("utf-8")
        
        # 在线程中，请求代理，获取远端， 注册的信息。 这里 请求远端 注册 的 标准输入输出和错误。
        sys.stdin = self.console = self.get_remote_proxy("stdin")
        sys.stdout = self.get_remote_proxy("stdout")
        sys.stderr = self.get_remote_proxy("stderr")
        from idlelib import IOBinding
        sys.stdin.encoding = sys.stdout.encoding = \
                             sys.stderr.encoding = IOBinding.encoding
        self.interp = self.get_remote_proxy("interp")
        rpc.RPCHandler.getresponse(self, myseq=None, wait=0.05)

    def exithook(self):
        "override SocketIO method - wait for MainThread to shut us down"
        time.sleep(10)

    def EOFhook(self):
        "Override SocketIO method - terminate wait on callback and exit thread"
        global quitting
        quitting = True
        thread.interrupt_main()

    def decode_interrupthook(self):
        "interrupt awakened thread"
        global quitting
        quitting = True
        thread.interrupt_main()
        
def manage_socket(address):
    for i in range(3):
        time.sleep(i)
        try:
            server = run.MyRPCServer(address, MyHandler)            
            break
        except socket.error, err:
            print>>sys.__stderr__,"IDLE Subprocess: socket error: "\
                                        + err.args[1] + ", retrying...."
    else:
        print>>sys.__stderr__, "IDLE Subprocess: Connection to "\
                               "IDLE GUI failed, exiting."
        run.show_socket_error(err, address)
        global exit_now
        exit_now = True
        return
    server.handle_request() # A single request only

exit_now = False
quitting = False
interruptable = False
def main(del_exitfunc=False):
    
    global exit_now
    global quitting
    global no_exitfunc
    no_exitfunc = del_exitfunc
    #time.sleep(15) # test subprocess not responding
    try:
        assert(len(sys.argv) > 1)
        port = int(sys.argv[-1])
    except:
        print>>sys.stderr, "IDLE Subprocess: no IP port passed in sys.argv."
        return
    sys.argv[:] = [""]
    sockthread = threading.Thread(target=manage_socket,
                                  name='SockThread',
                                  args=((run.LOCALHOST, port),))
    sockthread.setDaemon(True)
    sockthread.start()
    while 1:
        try:
            if exit_now:
                try:
                    exit()
                except KeyboardInterrupt:
                    # exiting but got an extra KBI? Try again!
                    continue
            try:
                seq, request = rpc.request_queue.get(block=True, timeout=0.05)
#                 print "request:",request
            except Queue.Empty:
                continue
            method, args, kwargs = request
            ret = method(*args, **kwargs)
#             print "respone:",ret
            rpc.response_queue.put((seq, ret))
        except KeyboardInterrupt:
            if quitting:
                exit_now = True
            continue
        except SystemExit:
            raise
        except:
            type, value, tb = sys.exc_info()
            try:
                run.print_exception()
                rpc.response_queue.put((seq, None))
            except:
                # Link didn't work, print same exception to __stderr__
                traceback.print_exception(type, value, tb, file=sys.__stderr__)
                exit()
            else:
                continue

