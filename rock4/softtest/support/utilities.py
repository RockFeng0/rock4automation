# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.support.utilities

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.support.utilities,v 1.0 2017年2月28日
    FROM:   2017年2月28日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import os

### utility path in support 
def get_utility_path(name):
    '''工具集的路径，有两种方式
    1.设置环境变量 rock4_home
    2.将工具集，放在utilities.py同路径下，但是这样的话，整个工程的大小，就会很大
    '''
    return os.path.join(os.getenv("rock4_home", os.path.dirname(os.path.realpath(__file__))),name)

### java
def get_java_path():
    java_exe = os.popen(os.path.join(get_utility_path("java"), 'find_java.exe')).read()
    return java_exe

### Android
def get_adb_path():
    adb_exe = os.path.join(get_utility_path("android"), 'adb.exe')
    if os.path.isfile(adb_exe):
        return adb_exe

def get_aapt_path():
    aapt_exe = os.path.join(get_utility_path("android"), 'aapt.exe')
    if os.path.isfile(aapt_exe):
        return aapt_exe

def get_appium_root_path():
    root = get_utility_path("appiumroot")
    if os.path.isdir(root):
        return root

### Selenium jar
def get_selenium_jar_path():
    jar = os.path.join(get_utility_path("seleniumjar"), 'selenium-server-standalone-3.0.1.jar')
    if os.path.isfile(jar):
        return jar
 
### Wpf driver
def get_wpfdriver_path():
    wpfdriver = os.path.join(get_utility_path("wpfdriver"), 'uiwpfdriver.exe')
    if os.path.isfile(wpfdriver):
        return wpfdriver

if __name__ == "__main__":
    print get_java_path()
    print get_adb_path()
    print get_aapt_path()
    print get_selenium_jar_path()
    print get_wpfdriver_path()