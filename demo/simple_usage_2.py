#! python3
# -*- encoding: utf-8 -*-
'''
Current module: test_s

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      test_s,v 1.0 2018年7月14日
    FROM:   2018年7月14日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from rock4.common.p_executer import TestRunner
from rock4.common.apirunner import ApiRunner
from rock4.common.p_applog import logger

runner = TestRunner(runner = ApiRunner()).run(r'tests\api.yaml')
