# -*- encoding: utf-8 -*-
'''
Current module: demo.excel_pcmfc_usage

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.excel_pcmfc_usage,v 1.0 2017年3月11日
    FROM:   2017年3月11日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from rock4.common import p_common
from rock4.softtest.common.ModelEntrance import test_start
from rock4.softtest.pc.uimfc.TestDriver import TestDriver

# 创建并初始化项目 
p_common.init_project_env("test", proj_path = r'D:\auto\env\testProject', initdirs = True)

def case_detail(devdriver):
    test_start(devdriver = devdriver,modelfile = r'D:\auto\env\testProject\testcase\pc_mfc_excel_usage.xlsx',modeltype="pcmfc")

if __name__ == "__main__":
    # 实例一个测试
    test = TestDriver()
    test.run_model_case(case_detail)
