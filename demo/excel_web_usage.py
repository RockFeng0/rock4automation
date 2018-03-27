# -*- encoding: utf-8 -*-
'''
Current module: demo.excel_web_usage

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.excel_web_usage,v 1.0 2017年3月11日
    FROM:   2017年3月11日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''



from rock4.common import p_common
from rock4.softtest.common.ModelEntrance import test_start
from rock4.softtest.web.TestDriver import TestDriver,SelRemote

# 创建并初始化项目 
p_common.init_project_env("web_excel_usage", proj_path = r'D:\auto\env\testProject', initdirs = False)

def case_detail(devdriver):
    test_start(devdriver = devdriver,modelfile = r'D:\auto\env\testProject\testcase\web_excel_usage.xlsx',modeltype="web")


def local_web_test():
    # defaultly will grab the remote host and connect them. if no remote host, local webdriver will be started
    return TestDriver(hub_ip="127.0.0.1", hub_port=4444)
    
def remote_web_test():
    '''
        Before test:
            # PC1 -> start hub 
                SelRemote().start_hub()
            # PC2 -> start node 
                SelRemote().start_node(5555, hub_ip="127.0.0.1", hub_port=4444)
    '''
    # using block=False to start hub and node without block on the same PC 
    SelRemote().start_hub(block=False)
    SelRemote().start_node(5555, hub_ip="127.0.0.1", hub_port=4444, block=False)
    return TestDriver(hub_ip="127.0.0.1", hub_port=4444, browsers = ["firefox","chrome"])
    
def remote_web_test2():
    '''
        Before test:
            # PC1 -> start hub 
                SelRemote().start_hub()
            # PC2 -> start node 
                SelRemote().start_node(5555, hub_ip="127.0.0.1", hub_port=4444)
    '''
    # defaultly will grab the remote host and connect them.
    return TestDriver(hub_ip="127.0.0.1", hub_port=4444, browsers = ["firefox","chrome"])

if __name__ == "__main__":
    # 实例一个测试      
    test = local_web_test()
#     test = remote_web_test()
#     test = remote_web_test2()
    
    # 执行测试模型的用例
    if test.is_server_running:
        test.run_model_case(case_detail)
        