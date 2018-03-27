# -*- encoding: utf-8 -*-
'''
Current module: rock4.common.p_report2

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.common.p_report2,v 1.0 2017年2月14日
    FROM:   2017年2月14日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


import p_env,p_common
import time,os

def _get_template_html_report(module_name, start_time, end_time, duration_seconds, total_case_num, pass_case_num, fail_cases_num, title_html, detail_html):    
    template_html_report = u"""
    <META HTTP-EQUIV='Content-Type' CONTENT='text/html; charset=utf8'>
    <HTML>
        <HEAD>
            <TITLE>TestCase Execution - Custom Report</TITLE>
            <STYLE>
                .textfont {font-weight: normal; font-size: 12px; color: #000000; font-family: verdana, arial, helvetica, sans-serif }
                .owner {width:100%%; border-right: #6d7683 1px solid; border-top: #6d7683 1px solid; border-left: #6d7683 1px solid; border-bottom: #6d7683 1px solid; background-color: #a3a9b1; padding-top: 3px; padding-left: 3px; padding-right: 3px; padding-bottom: 10px; }
                .product {color: white; font-size: 22px; font-family: Calibri, Arial, Helvetica, Geneva, Swiss, SunSans-Regular; background-color: #59A699; padding: 5px 10px; border-top: 5px solid #a9b2c5; border-right: 5px solid #a9b2c5; border-bottom: #293f6f; border-left: 5px solid #a9b2c5;}
                .rest {color: white; font-size: 24px; font-family: Calibri, Arial, Helvetica, Geneva, Swiss, SunSans-Regular; background-color: white; padding: 10px; border-right: 5px solid #a9b2c5; border-bottom: 5px solid #a9b2c5; border-left: 5px solid #a9b2c5 }
                .chl {font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; width: 17%%; height: 20px; border-bottom: 1px solid white }
                a {color: #336 }
                a:hover {color: #724e6d }
                .ctext {font-size: 11px; padding-right: 5px; padding-left: 5px; width: 80%%; height: 20px; border-bottom: 1px solid #eee }
                .hl {color: #724e6d; font-size: 12px; font-weight: bold; background-color: white; height: 20px; border-bottom: 2px dotted #a9b2c5 }
                .space {height: 10px;}
                h3 {font-weight: bold; font-size: 11px; color: white; font-family: verdana, arial, helvetica, sans-serif;}
                .tr_normal {font-size: 10px; font-weight: normal; background-color: #eee; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;}
                .tr_pass {font-size: 10px; font-weight: normal; background-color: #eee; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;}
                .tr_fail {font-size: 10px; font-weight: normal; background-color: #eee; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white; color: red;}
            </STYLE>
            <SCRIPT type="text/javascript">
            function showAll(opt) {
                tab = document.getElementsByClassName('textfont')[2]
                tab.style.display = 'table'
                trs = tab.getElementsByTagName("tr")
                if (opt == "Summary") {
                    tab.style.display = 'none'
                } else if(opt == "All") {
                    tab.style.display = 'table'
                    for (i=1;i<trs.length;i++) {trs[i].style.display = 'table-row'}
                } else if(opt == "Pass") {                
                    for (i=1;i<trs.length;i++) {trs[i].style.display = 'none'}
                    pass = document.getElementsByClassName("tr_pass")            
                    for (i=0;i<pass.length;i++) {pass[i].parentNode.style.display = 'table-row'}
                } else if(opt == "Fail") {
                    for (i=1;i<trs.length;i++) {trs[i].style.display = 'none'}
                    fail = document.getElementsByClassName("tr_fail")
                    for (i=0;i<fail.length;i++) {fail[i].parentNode.style.display = 'table-row'}
                }            
            }
            </SCRIPT>
            <META content='MSHTML 6.00.2800.1106'>
        </HEAD>
        <body onload="showAll('%s')" leftmargin='0' marginheight='0' marginwidth='0' topmargin='0'>
            <table width='100%%' border='0' cellspacing='0' cellpadding='0'>
                <tr>
                    <td class='product'>Quality Center</td>
                </tr>
                <tr>
                    <td class='rest'>
                        <table class='space' width='100%%' border='0' cellspacing='0' cellpadding='0'>
                            <tr>
                                <td></td>
                            </tr>
                        </table>                                                                        
                        <table class='textfont' cellspacing='0' cellpadding='0' width='100%%' align='center' border='0'>
                            <tbody>
                                <tr>
                                    <td>
                                        <table class='textfont' cellspacing='0' cellpadding='0' width='100%%' align='center' border='0'>
                                            <tbody>
                                                <tr>
                                                    <td class='chl' width='20%%'>Project Name</td>
                                                    <td class='ctext'>%s</td>
                                                </tr>
                                                <tr>
                                                    <td class='chl' width='20%%'>TestSet</td>
                                                    <td class='ctext'>%s</td>
                                                </tr>
                                                <tr>
                                                    <td class='chl' width='20%%'>Started</td>
                                                    <td class='ctext'>%s</td>
                                                </tr>
                                                <tr>
                                                    <td class='chl' width='20%%'>Finished</td>
                                                    <td class='ctext'>%s</td>
                                                </tr>
                                                <tr>
                                                    <td class='chl' width='20%%'>Duration</td>
                                                    <td class='ctext'>%s</td>
                                                </tr>
                                                <tr>
                                                    <td class='chl' width='20%%'>TotalCases</td>
                                                    <td class='ctext' style="text-decoration:underline" onclick="showAll('All')"><span style="cursor:pointer;">%s</span></td>
                                                </tr>
                                                <tr>
                                                    <td class='chl' width='20%%'>PassCases</td>
                                                    <td class='ctext' style="text-decoration:underline" onclick="showAll('Pass')"><span style="cursor:pointer;">%s</span></td>
                                                </tr>
                                                <tr>
                                                    <td class='chl' width='20%%'>FailCases</td>
                                                    <td class='ctext' style="text-decoration:underline" onclick="showAll('Fail')"><span style="cursor:pointer;">%s</span></td>
                                                </tr>
                                                <tr>
                                                    <td class='chl' width='20%%'>DesignBy</td>
                                                    <td class='ctext'>luokefeng@myweb.com</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td class='space'></td>
                                </tr>
                            </tbody>
                        </table>
                        <table class='textfont' cellspacing='0' cellpadding='0' width='100%%' align='center' border='0'>
                            <tbody>
                                %s
                                %s
                            </tbody>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
    </HTML>
    """ %(p_env.REPORT_OUTPUT_ALL,os.path.basename(p_env.PROJECT_PATH),module_name, start_time, end_time, duration_seconds, total_case_num, pass_case_num, fail_cases_num, title_html, detail_html)    
    return template_html_report

def add_report_data(list_all=[], module_name="TestModule", case_name="TestCase",  result="Pass", **kwargs):
    '''Usage:
        result = []
        p_env.CASE_START_TIME = time.time()
        result = add_report_data(result, case_name = 'test1', result = "Fail", RespTester="administrator", Tester = "tester1")
        result = add_report_data(result, case_name = 'test2', result = "Pass", RespTester="administrator", Tester = "tester2")
        result = add_report_data(result, module_name = "Module2", case_name = 'test1', result = "Fail", RespTester="administrator", Tester = "tester3")
        result = add_report_data(result, module_name = "Module2", case_name = 'test2', result = "Pass", RespTester="administrator", Tester = "tester4")
        print result
        result = add_report_data(result, module_name = "Module2", case_name = 'test1', result = "Pass", RespTester="administrator", Tester = "tester5")
        print result   
    '''
    exec_date_time = time.localtime(p_env.CASE_START_TIME)
    execdate = time.strftime("%Y-%m-%d",exec_date_time) 
    exectime = time.strftime("%H:%M:%S",exec_date_time)
    
    for module in list_all:
        if module_name != module["Name"]:
            continue
        
        for case in module["TestCases"]:
            if case_name == case["CaseName"]:
                case["Status"] = result
                case.update(kwargs)
                return list_all
        
        kwargs.update({"CaseName": case_name, "Status": result, "ExecDate":execdate, "ExecTime":exectime})
        module["TestCases"].append(kwargs)
        return list_all
    
    kwargs.update({"CaseName": case_name, "Status": result, "ExecDate":execdate, "ExecTime":exectime})
    list_all.append({"Name": module_name, "TestCases": [kwargs]})
    return list_all


def generate_result_html(titles_sequnce=["CaseName","Status","RespTester","Tester","ExecDate","ExecTime"]):  
    ''' Generate the report with HTML format.
    Sample usage:
        p_common.init_project_env("usage", proj_path = r'D:\auto\buffer\testProject', initdirs=True)
        p_env.MODULE_START_TIME = time.time()
        p_env.MODULE_STOP_TIME = p_env.MODULE_START_TIME + 60
        p_env.REPORT_DATA =[{'TestCases': [{'Status': 'Fail',
                                             'CaseName': 'ATest',
                                            'Tester': 'administrator',
                                             'ExecTime': '14:34:40',
                                              'RespTester': 'administrator',
                                               'ExecDate': '2015-05-15'}],
                                                'Name': 'PyDebug'}]
        generate_result_html()
        print "Complete."
    '''
    
    for module in p_env.REPORT_DATA:
        module_name = module['Name']
        total_case_num = len(module["TestCases"])
        
        title_html = ""        
        for i in titles_sequnce:
            title_html = title_html + "\n\t<td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>%s</td>" %i
        title_html = "<tr>" + title_html + "\n</tr>"
                
        detail_html = ""
        pass_case_num = 0
        fail_cases_num = 0
        for case in module["TestCases"]:
            linkurl = "./testcase/%s_%s.log" %(case["CaseName"],case["ExecDate"])
            if case["Status"].lower() == "pass":
                pass_case_num += 1
                c_style = "tr_pass"
            else:
                fail_cases_num = fail_cases_num + 1
                c_style = "tr_fail"
            
            for i in titles_sequnce:
                if i == "CaseName":
                    detail_html = detail_html + "\n\t<td class='tr_normal'><a target='_blank' href='%s'>%s</a></td>" %(linkurl, case["CaseName"])
                elif i == "Status":
                    detail_html = detail_html + "\n\t<td class='%s'>%s</td>" %(c_style, case["Status"])
                else:
                    detail_html = detail_html + "\n\t<td class='tr_normal'>%s</td>" %case[i]
            detail_html = "<tr>" + detail_html + "\n</tr>"
         
        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(p_env.MODULE_START_TIME))    
            end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(p_env.MODULE_STOP_TIME))        
            duration_seconds = float("%.2f" %(p_env.MODULE_STOP_TIME - p_env.MODULE_START_TIME))
        except Exception,e:
            print "\n\tWarning: didn't call 'project_start' or 'project_stop' functions"
            (start_time, end_time, duration_seconds) = (None,None,None)
        
        if fail_cases_num > 0:
            template_simple_dict_report = {"result":0,"message":"failure","pass":pass_case_num,"fail":fail_cases_num}
        else:
            template_simple_dict_report = {"result":1,"message":"success","pass":pass_case_num,"fail":fail_cases_num}
        
        template_html_report = _get_template_html_report(module_name, start_time, end_time, duration_seconds, total_case_num, pass_case_num, fail_cases_num, title_html, detail_html)
        
        html_report = os.path.join(p_env.RST_PATH,"result.html")
        simple_dict_report = os.path.join(p_env.RST_PATH,'result.json')
    #     p_common.force_delete_file(html_report) -->大量的该动作，可能引起 [IOError Errno 13] Permission denied
        print html_report
        with open(html_report,'w') as f:
            f.write(unicode(template_html_report).encode("utf-8"))
        with open(simple_dict_report,'w') as f:
            f.write(str(template_simple_dict_report))
            
if __name__ == "__main__":
    p_common.init_project_env("PyDebug", proj_path = r'D:\auto\buffer\testProject', initdirs=True)
    p_env.MODULE_START_TIME = time.time()
    p_env.MODULE_STOP_TIME = p_env.MODULE_START_TIME + 60
    p_env.REPORT_DATA =[{'TestCases': [{'Status': 'Fail',
                                         'CaseName': 'ATest',
                                        'Tester': 'administrator',
                                         'ExecTime': '14:34:40',
                                          'RespTester': 'administrator',
                                           'ExecDate': '2015-05-15'}],
                                            'Name': 'PyDebug'}]
    generate_result_html()
    print "Complete."


            