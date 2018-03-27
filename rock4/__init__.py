# -*- encoding: utf-8 -*-
'''
Current module: rock4.__init__

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.__init__,v 1.0 2017年3月11日
    FROM:   2017年3月11日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
__version__ = "2.0.0"

import sys

if sys.subversion[0].lower() == "cpython":    
    from .softtest.api.webservice.irequests.TestDriver import TestDriver as PacketTest  
    from .softtest.pc.uimfc.TestDriver import TestDriver as PcMfcTest
    from .softtest.pc.uiwpf.TestDriver import TestDriver as PcWpfTest
    from .softtest.web.TestDriver import TestDriver as WebTest, SelRemote as Grid
    from .softtest.pad.uiappium.TestDriver import TestDriver as PadTest
    from .softtest.common.ModelEntrance import test_start as shoot
    from .common.p_common import init_project_env as target
    
    # Selendroid
#     from .uiselendroid.driver import MobileApp as SimpleAndroid
#     from .uiselendroid.driver import MobileElement as SimpleApp
    
    # UiAutomator --> will start adb.exe when import this
#     from .uiautomator.driver import PadDevice as SimpleSDKAndroid
#     from .uiautomator.driver import PadUI as SimpleSDKApp

if sys.subversion[0].lower() == "ironpython":
    # IronPython; MUIA
    pass
 
if sys.subversion[0].lower() == "jython" and "tools\\lib" in sys.prefix:
    # Monkeyrunner-->Jython; Monkeyrunner + Hierarchy    
    pass


    



