# 初衷

>  如何保持学到的技术，随着时间不被遗忘？ 需要用到的时候，又可以快速重拾旧业？这是我的初衷，我也这么做了.


- **把这些技术的使用方法，采用统一的框架架构，系统的，模块化的封装打包**
- 其实，在自动化测试方向，我使用过很多方案，也在企业不停的探索和实践，早期，也就是摒弃旧的落后的技术，选择新技术，后来发现，旧的依旧有它的优点
- 于是，就有了rock4项目，当你看到项目代码的时候，里边有些模块中使用的技术是落后的，也许你永远用不到，但是还是可以找到学习入口和调用入口
- 目前，整合的一些自动化框架，如 selenium、appium、autoitv3、Microsoft UI Automation等等，关于性能的测试，我这里整合了locust的一些用法
- 还有一些也许你用不到的效果不好的自动化框架，如，Android SDK自带的 hierarchy、selendroid、uiautomator等

> 下载下来后，您可以选择删除一些您使用不到的模块，因为它不会影响其他框架的运行，路径: rock4/softtest/...

* * *

# 介绍

> Rock4 是一款面向客户端(B/S、C/S、Android移动端) 和 HTTP 协议的通用测试框架，只需编写维护一份 Excel/Yaml伪代码测试用例，即可实现自动化测试、性能测试、持续集成等多种测试需求。


## 设计理念

- 采用优秀的开源项目，组成一个更贴近企业应用的项目，不重复造轮子，而是选择优秀的部件组装汽车.
- 遵循目前的关键字驱动和数据驱动，再框架中融入企业中的最佳实践
- 以最少的投入，产出更多的输出

## 逻辑流程图

![](https://github.com/RockFeng0/rock4automation/raw/master/doc/logic.png)
 
 
## Rock4工作原理

![](https://github.com/RockFeng0/rock4automation/raw/master/doc/principle.png) 
 
## 核心特性 
- 继承优秀开源项目全部特性，轻松实现客户端(browser、WinForm/MFC/WPF、Android)的各种测试需求
- 集成 Selenium Webdriver和Selenium Remote，轻松实现本地web自动化测试和分布式web测试
- 集成Appium，实现有线/无线模式的分布式app自动化测试，最多上限支持20台设备同时测试, **此特性依据adb.exe的最大支持量**
- 集成AutoItv3和Microsoft UI Automation API,实现支持客户端的本地自动化测试，主要客户端技术类型: MFC、WinForm、WPF
- 集成Requests，轻松实现HTTP(s)协议的测试，无缝支持Locust性能测试框架，可实现分布式性能测试
- 测试用例与代码进行了分离，支持EXCEL和Yaml的模型，组织测试数据，支持测试用例的复用、结构分层划分、功能模块划分等
- 测试用例支持参数化、关键字驱动、数据驱动机制
- 测试用例的执行拥有流程的控制，测试用例执行过程的失败，不会阻塞整体执行流程
- 测试用例的执行方式，支持命令行(CommandLine)调用,可与 Jenkins等持续集成工具完美结合
- 测试结果，以html报告的形式展示，简洁清晰，附带详尽统计信息、测试用例日志记录、步骤执行日志记录
- 具有可扩展性，用例组织内在形式是标准的python dict，便于扩展实现B/S模式 Web的平台化或者C/S模式PC客户端化

* * *

# Rock4用法简介 

## 安装说明（目前，仅Windows）

Rock4 是一个基于 Python 开发的测试框架，运行在Windows系统平台上(因为集成了win32，winform和wpf的测试框架)

Rock4 的开发环境为 Windows 7 + Python 2.7, 推荐使用Windows 7 + python2.7 的运行环境组合。

安装步骤，如下：
- 下载 [autoitpy_v1.0.0](https://github.com/RockFeng0/autoit-v3-py/releases)，解压后执行: python setup.py install
- 下载[rock4的zip包](https://github.com/RockFeng0/rock4automation/releases)，解压后执行: python setup_egg.py install
- 下载[rock4-support-tools.zip](https://github.com/RockFeng0/rock4automation/releases)，解压后，将该路径，添加为环境变量 ROCK4_HOME 
        

## 入门指南

- [快速上手](http://rockfeng0.github.io/hello-world/2018/04/02/rock4_project_init.html)
- [测试用例](http://rockfeng0.github.io/hello-world/2018/04/01/rock4_testcases.html)

## 进阶指南
    
- [高级特性](http://rockfeng0.github.io/hello-world/2018/03/31/rock4_module.html)








