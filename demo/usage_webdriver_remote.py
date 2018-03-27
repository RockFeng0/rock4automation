# -*- encoding: utf-8 -*-
'''
Current module: demo.usage_webdriver_remote

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.usage_webdriver_remote,v 1.0 2017年5月19日
    FROM:   2017年5月19日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


from rock4 import WebTest,Grid
# remote webdriver

# 创建网格对象；用于分布式的web测试，实际上就是对 selenium-server.jar的二次封装
grid = Grid()

#启动 server端;  port 默认是 4444端口; block 默认是True, False时,jar命令不会阻塞; 
grid.start_hub(port = 4444, block = False)

#启动client端连接至server;  port 为5555; hub_ip 默认是localhost; hub_port 默认是4444端口; block 默认是True, False时,jar命令不会阻塞;
grid.start_node(5555, block=False)


'''
WebTest remote parameter:
    browsers:      list of browser. all of these: firefox chrome opera safari internetexplorer edge htmlunit htmlunitwithjs  
    patch_with:    brwoser will be padding with, if not match the length of remote hosts              
    marionette:    False / True, firefox driver will get started if True
    download_path:    set default download path of firefox or chrome
'''
test = WebTest()

# find_driver 与 find_drivers  优先连接 Remote driver,连接不上再连接Local driver
# find_driver 返回第一个driver; find_drivers 返回dict; 返回的 driver 是 selenium 对象
drivers = test.find_drivers()
driver = drivers.items()[0][1]    
driver.get("http://www.baidu.com")
driver.quit()

# 关闭 server, kill java.exe  for windows
grid.stop()