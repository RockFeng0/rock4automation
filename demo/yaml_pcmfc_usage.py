# -*- encoding: utf-8 -*-
'''
Current module: demo.yaml_pcmfc_usage

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      demo.yaml_pcmfc_usage,v 1.0 2017年5月18日
    FROM:   2017年5月18日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
from rock4 import shoot,target,PcMfcTest

# 创建并初始化项目 
target("test", proj_path = r'D:\auto\env\testProject', initdirs = True)

def case_detail(devdriver):
    shoot(devdriver = devdriver,modelfile = r'D:\auto\env\testProject\testcase\pc_mfc_yaml_usage.yaml',modeltype="pcmfc")

if __name__ == "__main__":
    # 实例一个测试
    test = PcMfcTest()
    test.run_model_case(case_detail)
    