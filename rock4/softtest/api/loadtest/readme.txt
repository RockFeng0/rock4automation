示例项目：
参见工程 loperf

1.执行
    命令行->D:\auto\python\loperf\httpload.py 200 10 100
    会初始化创建项目目录结构，并执行性能测试(200用户总数，每秒生成并发10个用户，持续100秒)
2.查看帮助
    命令行->D:\auto\python\loperf\httpload.py -h
3.测试用例编写
    首先配置项目目录下的config.ini文件，如下
        [Xdata]
        name = test.xlsx        --> 配置测试Excel的名字test.xlsx，这个文件放在项目目录的data下面
        sheet = test            --> 配置测试Excel的sheet页面，会执行这里的用例
        
        [Linux]
        ip = 192.168.109.247        -->配置测试的Linux服务器IP
        user = root                 -->ssh连接服务器的用户名
        passwd = TWSM@test247       -->ssh连接服务器的密码
        port = 22                   -->ssh连接服务器的端口
    
    其次，写用例：
        指定的sheet页面中，首行title：ID	Name	PreCommand	Transmission	Head	Data	Verify	Scene
            ID性能测试用例唯一编号，如 PTC-1,ATP-1等
            Name性能测试用例的名称，如 查询作业 等
            PreCommand用于初始化变量，有三个关键字，进行参数化：
                1.sethost("http://192.168.109.247") --> 每个 Scene 使用一次，定义该场景的host
                2.setvar(l_num="1") --> excel中使用 #l_num#用户参数化
                3.setfilevar('d:/auto/buffer/t.txt')
其中t.txt，那么a和b依次取值1和2 ...并循环:
a   b
1   2
2   3
            Transmission用于发送请求，一个关键字:
                send("/portal/ClientApi/getPublishResultList","post","json") -->这里指定post请求，json形式
                send("/portal/ClientApi/getPublishResultList") -->默认 get请求,表单形式
            
            Head和Data 填写json数据
            Verify 一个关键字:
                contain('resultCode\":0') -->检查性能测试，每个vuser的结果，包含resultCode\":0事务成功
            Scene场景编号，编号一致的，依据ID进行纵向场景；编号不一致，识别为平行场景
4. 写完用例，参数化之前，
    使用命令--> D:\auto\python\loperf\httpload.py 200 10 100 -t 1 进行测试，如果，达到预期，进行参数化

5.测试结束，项目路径下的result目录下result.html生成报告。注意：在resource中，添加bokeh的两个离线文件(js及css)