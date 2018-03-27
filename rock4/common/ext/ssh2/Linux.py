# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.ssh2.Linux

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      pyrunner.ext.ssh2.Linux,v 1.0 2016年10月10日
    FROM:   2016年10月10日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import paramiko
import sys,os,re,time

def get_info_script():
    fp = os.path.abspath(sys.path[0])
    if os.path.isfile(fp):
        fp = os.path.dirname(fp)
    return fp
 
class Linux:
    def __init__(self, kw):
        self._ssh = None
        self.ip = kw['ip']
        self.username = kw['user']
        self.password = kw['passwd']
        self.port = int(kw['port'])
        
    def get_ssh(self):
        ''' Establish connection
            Return ssh connection object
        '''
        if self.is_connected():
            return self._ssh
        
        for i in range(6)[::-1]:
            print "Establish connection(%d) with %s %s" %(i,self.ip,self.port)
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            try:
                self._ssh.connect(self.ip, self.port, username = self.username, password = self.password, timeout=5)
            except Exception,e:                
                if i == 0:
                    raise Exception("Linux connection error: %s" %e)
                time.sleep(30)
            else:
                return self._ssh
    
    def is_connected(self):
        ''' Judge the self._ssh and judge the session of self._ssh.get_transport() and judge the session is active
            True if the session is still active (open)
            False if the session is closed
            None if not has a connection object.(self._ssh)        
        '''
        transport = self._ssh.get_transport() if self._ssh else None
        connected = transport and transport.is_active()
        return connected

    def exec_cmd(self, cmd):
        ''' Sample usage:
                cfg = {'ip':'192.168.109.222', 'user':'root',  'passwd':'TWSM@test222', 'port':8822}
                l = Linux(cfg)
                print l.exec_cmd('ls\n')
        '''
        ssh = self.get_ssh()                
        std_in, std_out, std_err = ssh.exec_command(cmd)
        out_info = std_out.readlines()
        ssh.close()
        return out_info
    
    def exec_cmds(self, commands_list, timeout=30, file_name='temp.txt', ps1 = r'[\u@\h \W]\$', ps1_regx = '\[.*@.*\][#\$]$'):
        r''' Sample usage:
                cfg = {'ip':'192.168.109.222', 'user':'root',  'passwd':'TWSM@test222', 'port':8822}
                l = Linux(cfg)
                # 执行命令序列， 在  ifconfig | more 的命令的时候，挂起了，超时后， 敲空格符号\x20继续, 这里 示例敲了两次..最后等待超时结束
                cmds = ['ll\n', 'ls\n','ping 127.0.0.1 -c 3\n', 'cat /usr/twsm/aicloud-install.sh | more \n', '\x20','\x20']
                l.exec_cmds(cmds,timeout = 5)
                cmds2 = ['reboot\n','sleep 10\n','sh /usr/twsm/upgrade-tool/upgradetool.sh restart\n','sleep 10','service iptables stop\n']    
                l.exec_cmds(cmds2)
            parameter:
                commands_list    --> List commands which will be send to linux. ['ls\n','ping 127.0.0.1 -c 3\n'] etc.
                timeout        --> Every read(recv etc.) or write(send etc.) operations must have completed during the timeout. Otherwise, will raise a timeout exception 
                ps1        --> Linux's prompt. The value is the return of command: echo $PS1                
                            Such as:  [\u@\h \W]\$  -> [root@aicloud ~]# 
                            
                            linux下PS1命令提示符设置: 
                                \d ：代表日期，格式为weekday month date，例如："Mon Aug 1"
                                \H ：完整的主机名称。例如：我的机器名称为：fc4.linux，则这个名称就是fc4.linux
                                \h ：仅取主机的第一个名字，如上例，则为fc4，.linux则被省略
                                \t ：显示时间为24小时格式，如：HH：MM：SS
                                \T ：显示时间为12小时格式
                                \A ：显示时间为24小时格式：HH：MM
                                \u ：当前用户的账号名称
                                \v ：BASH的版本信息
                                \w ：完整的工作目录名称。家目录会以 ~代替
                                \W ：利用basename取得工作目录名称，所以只会列出最后一个目录
                                \# ：下达的第几个命令
                                \$ ：提示字符，如果是root时，提示符为：# ，普通用户则为：$ 
                ps1_regx    --> the regular expression of ps1's parameter. Such as: '\[.*@.*\][#\$]$'
                file_name   --> executing logs will be save to this file
        '''
        shell = None
        # 设置等待命令输入 标识的正则
        ps = re.compile(ps1_regx)
        # 设置linux提示符标志
        commands = ["PS1='%s'\n" %ps1]        
        commands.extend(commands_list)        
        for cmd in commands:
            if not shell or not self.is_connected():      
                shell = self.get_ssh().invoke_shell()
                shell.settimeout(timeout)
                
            print '#### Executing: %s' % cmd
            try:
                shell.send(cmd + "\n")
            except Exception,e:
                # socket.timeout
                print "#### Send command error: %s." %e
            
            while True:                
                try:
                    str_inf = shell.recv(1024)                    
                    if str_inf:
                        print str_inf
                                            
                    with open(get_info_script()+'/%s' % file_name, 'a') as f:
                        f.write(str_inf)
                    
                    # 搜索等待命令输入的标识
                    if ps.search(str_inf.strip()):                        
                        break
                    
                    if not self.is_connected():
                        break                    
                                   
                except Exception,e:
                    info = sys.exc_info()
                    if "socket.timeout" in str(info[0]):
                        print '#### Complete.'
                    else:
                        print "#### Recv exception: %s", e
                    break    
                
    def upload(self, localpath, remotepath):
        ''' Sample usage:
                cfg = {'ip':'192.168.109.222', 'user':'root',  'passwd':'TWSM@test222', 'port':8822}
                remotepath = '/usr/twsm/'
                localpath =  get_info_script() + '/'
                file_name = "temp.txt"
                l = Linux(cfg)    
                l.exec_cmds(['mkdir -p %s' %remotepath,'chmod -R 777 %s' %remotepath])
                print u'开始上传 文件: %s' % file_name
                l.upload(localpath+file_name, remotepath+file_name)
                result = l.exec_cmd('ls /usr/twsm/\n')
                print result         
                print u'上传 完成。'
        '''
        t = paramiko.Transport((self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(localpath, remotepath)
        t.close()
    
    def download(self, remotepath, localpath):
        ''' Sample usage:
               cfg = {'ip':'192.168.109.222', 'user':'root',  'passwd':'TWSM@test222', 'port':8822}
                remotepath = '/usr/twsm/'
                localpath =  'd:/auto/buffer/'
                file_name = "temp.txt"
                l = Linux(cfg)    
            
                print u'开始下载 文件: %s' % file_name
                l.download(remotepath + file_name, localpath+file_name, )    
                print u'下载完成。'
        '''
        t = paramiko.Transport((self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
#         print sftp.listdir('/usr/twsm')
        sftp.get(remotepath, localpath)
        t.close()                    
    
                
if __name__ == '__main__':
    cfg = {'ip':'192.168.102.203', 'user':'root',  'passwd':'TWSM@admin', 'port':22}
    l = Linux(cfg)
    cmds = ['ll\n', 'ls\n','ping 127.0.0.1 -c 3\n', 'cat /usr/twsm/aicloud-install.sh | more \n', '\x20','\x20']
    l.exec_cmds(cmds,timeout = 5)
    print "================="
    cmds2 = ['reboot\n','sleep 10\n','sh /usr/twsm/upgrade-tool/upgradetool.sh restart\n','sleep 10','service iptables stop\n']
    l.exec_cmds(cmds2)
    print "================="
    print l.exec_cmd("ping 127.0.0.1 -c 3")
    print l.exec_cmd("ping 127.0.0.1 -c 3")
    print l.exec_cmd("top -b -d 1 -n 10 >/usr/twsm/top01.txt &")
