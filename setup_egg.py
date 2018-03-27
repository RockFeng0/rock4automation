# -*- encoding: utf-8 -*-
'''
Current module: setup

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      setup,v 1.0 2017年3月11日
    FROM:   2017年3月11日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''
import sys,zipfile,os
from setuptools import setup,find_packages
VERSION = "2.0.0"

if sys.argv[1] == "bdist_egg":
    p = os.path.dirname(sys.argv[0])
    dst = os.path.join(p,r'rock4\softtest\support\appiumroot.zip')
    if not os.path.isfile(dst):
        src = os.path.join(p,r'rock4\softtest\support\appiumroot')
        zipf = zipfile.ZipFile(dst, 'w', zipfile.zlib.DEFLATED)
        pre_len = len(os.path.dirname(src))
        for parent, dirnames, filenames in os.walk(src):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep);#相对路径
                zipf.write(pathfile, arcname)
        zipf.close()
elif sys.argv[1] == "bdist_pyd":
    # 自定义的 bdist_pyd; 前提是，把生成的 distpyd_rock4 拷贝到 build/lib目录下，并且重命名为 rock4
    sys.argv[1] = "bdist_egg"

setup(
        name = "rock4",
        version=VERSION,
        packages = ['rock4'],
#         packages = find_packages(),      
#         package_data = {
#             "rock4.softtest.support" : [                
#                 "android/*",
#                 "java/*",
#                 "seleniumjar/*",
#                 "wpfdriver/*",
#                 "appiumroot.zip",
#                 ],
#             },
        include_package_data=True,
        zip_safe = True,        
        install_requires = ['selenium>=3.0.2','appium-python-client>=0.11','requests>=2.13.0','PyYAML>=3.12','xlrd>=0.9.3',"beautifulsoup4>=4.5.1","autoitpy==1.0.0"],        
        author = u"bruce luo(罗科峰)",
        author_email = "lkf20031988@163.com",
        description = "for automation test",
        long_description = "UI web test or UI pc test or web service test or android test",
        license = "MIT",
        keywords = "rock4",
        url = "",
    )

 
# 注意: 
#    打包的时候，support/appiumroot 是打包的zip 文件，而不是开启文件清单，打包整个目录; 因为，如果打包目录的话，安装的时候，会window error 206的错误--也就是appiumroot文件夹路径太深的错误
#    如果要使用appium的话，那么安装完成后，需要手动将        appiumroot.zip 解压到 当前目录
