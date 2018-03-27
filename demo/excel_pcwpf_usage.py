# -*- encoding: utf-8 -*-
'''
Current module: demo.excel_pcwpf_usage

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.excel_pcwpf_usage,v 1.0 2017年3月24日
    FROM:   2017年3月24日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import os
from rock4.common import p_common,p_env
from rock4.softtest.common.ModelEntrance import test_start
from rock4.softtest.pc.uiwpf.TestDriver import TestDriver

def case_detail(devdriver):
    test_start(devdriver = devdriver,modelfile = os.path.join(p_env.CASE_PKG_PATH, 'pc_wpf_excel_usage.xlsx'),modeltype="pcwpf")

if __name__ == "__main__":
    # 创建并初始化项目
    proj_path = r'D:\auto\env\testProject'    
    p_common.init_project_env("test", proj_path = proj_path, initdirs = True)
    
    print "----"
    # 实例一个测试
    test = TestDriver()
    test.run_model_case(case_detail)
