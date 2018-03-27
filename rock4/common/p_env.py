# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.p_env

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com    
    RCS:      rock4.common.p_env,v 2.0 2017年2月7日
    FROM:   2015年5月11日
********************************************************************

======================================================================

Define some useful variables for testcases.

'''
__version__         = 1.0

# Path of java.exe in the system
JAVA_EXE            = ""

# Root path of the testing project.
PROJECT_PATH        = ""

# Configuration file of the testing project
PROJECT_CFG_FILE    = ""

# Path of test case packages 
CASE_PKG_PATH       = ""

# Path of data which is needed by datadriver
DATA_PATH           = ""

# Path of temporary files and buffer files
BUFFER_PATH         = ""

# Path of resources.  apk/mp3/pdf/mp4...  etc.
RESOURCE_PATH       = ""

# Path of tools.  batch/shell/exe/jar...  etc.
TOOLS_PATH          = ""

# Path of test result
RST_PATH            = ""
RST_SCR_SHOT_PATH   = ""
RST_CASE_LOG_PATH   = ""

# Test Case/Module variables.
CASE_START_TIME     = ""
CASE_STOP_TIME      = ""
CASE_NAME           = ""
CASE_PASS           = ""

MODULE_NAME         = ""
MODULE_START_TIME   = ""
MODULE_STOP_TIME    = ""

# Driver of win MFC UI, such as: autoit.WinMFCDriver()
WINMFC              = ""
WINWPF              = ""


# Web UI Case/Module variables.
TEST_URL            = ""

# Driver of android or IOS, such as: webdriver.Remote('http://localhost:4723/wd/hub', desired_caps={'platformName':'Android','platformVersion':'4.4.2','deviceName':'device','app':r'E:\ApiDemos-debug.apk'})
MOBILE              = ""
EMOBILE             = ""
HIERARCHY           = ""

# Driver of web browser, such as: webdriver.Firefox()
BROWSER             = ""

# RUNNING_BROWSER is one of TESTING_BROWSERS
RUNNING_BROWSER     = "Firefox"
TESTING_BROWSERS    = "Firefox|IE|Opera|Chrome|Safari"

# Data of test result, for generate report in excel or html.
REPORT_DATA   = []
REPORT_OUTPUT_ALL   = ""

EXECUTE_INTERRUPTER = False








