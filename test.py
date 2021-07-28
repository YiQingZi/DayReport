from flask import Flask
from flask import request
from flask import render_template
from hadata import get_client_data,str_Y_M_D
from hadata import send_get_day , send_day_report,send_cmd,send_day_report_mail
from hadata import send_put_day ,is_repeat ,get_id,send_del_report
import threading


app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template("test.html")

@app.route('/update.html')
def my_update():
    return render_template("update.html")

@app.route('/', methods=['POST'])
def my_form_post():

    error_page = """
    
                <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <title>错误界面</title>
                        <meta http-equiv="refresh" content="5;url=./">
                    </head>
                    <body align="center">
                        <div style="width: 56%;margin: 0 auto;">
                            
                            <header align="center" >
                                <div align="left" >
                                    <a href="./">
                                        <img src="https://www.meigsmart.com/userfiles/images/2020/03/23/2020032311354713.png" style="width: 200px;" alt="上海·美格" />
                                    </a>
                                </div>
                                <div align="center">
                                    <h1>日报系统</h1>
                                    <p><time pubdate datetime="2021-07-19"></time></p>
                                </div>
                            </header>
                            
                            
                            <div style="margin: 100px 0px 100px 0px;">
                                
                                
                                <h4 style="color: red;">{0} 失败！请重试，或者{1}！</h4>
                                <p>5 秒后自动跳转</p>
                                
                            </div>
                            
                            
                            
                            
                            <footer align="center" >
                                <p>美格 · 测试</p>
                                <p><dfn><abbr title="发布时间：2021-07-20">版本：v2.00</abbr><a href="./update.html">更新日志</a></dfn></p>
                                <p><time 发布日期时间="2021-07-20"></time></p>
                            </footer>
                            
                        </div>
                    </body>
                </html>
    
    """


    is_select = 0


    try:
        project_1 = request.form['my-day']
        is_select = 1
    except:
        try:
            project_1 = request.form['my-get-day']
            is_select = 2
        except:
            try:
                project_1 = request.form['my-mom']
                is_select = 3
            except:
                try:
                    project_1 = request.form['my-del-day']
                    is_select = 4
                except:
                    try:
                        project_1 = request.form['my-get-day-all']
                        is_select = 5
                    except:
                        try:
                            project_1 = request.form['my-get-project-all']
                            is_select = 6
                        except:
                            is_select = 0

    if is_select == 1:
        # '#@#@123@#@#|-|name|-|project|-|date|-|task|-|completion|-|introduce|-|remarks|-|time'
        # INSERT_DATA(self,tabName,name,project,time,task,completion,introduce,date=None,remarks='null'):
        A_REPORT_LIST = 'SLM755,SLM757,SLB742,SLM758,SLB748,SLM755L,SLB749,SLB741,SLM752,SLB760,SLM756,SLB761,SLB742W,SLB763,SLB765,SLB741W,SLB748W,SLB767,SLB769,SLB781,SLB788,SLB782,SLB783,SLB789,SLB765XQ,SLB761XQ,SLM758W,SLM759,SLT187,SLB786,MC510,SLB785,SLB787,SLM900,SLM755LE,SLM300,SLB763P,MC501,MC502,MC503,MC506,MC509,MC510,MT511,MT512,MC508,MC513,SLM758S,SLM310,SLM320,SLM500,MC518,MC519,MC521,MC520,MT523,MC565X,MC525,MC526,MC528,SLM500S,SLM500QC,SLM500QW,SLM330,MC529,MC901,SRM900,MC902,MC561,MC301,MT533,SLM326,MT903,MC531,MC532,SLM328,SLM920,SRM910,MC302,MT303,MT535,MC536,MT537,MC905,MC907,MC908,MC329,SLM550,MC538,SLM921,SM130,SLM322,SLM326S,SLM330S,SLM320S,SLM320P,SLM320PS,SLM326E,MC906,MC551,SLM320H,SLM326L,MC557,MC582,SRM930,SRM935,平台EVB项目,非自研项目,预研项目,其它'
        REPORT_LIST = A_REPORT_LIST.split(',')
        name, date , list_data = get_client_data()
        list_data = str(list_data).replace('),)',"").replace('),',"|-|").replace("(","").replace(")","").replace("'","")
        list_data1 = list_data.split("|-|")
        # (('MC529', '任务简介', '100', '工作简介', '暂无', '8'),)
        len_list = len(list_data1)
        if len(list_data1) == 1:
            list1 = list_data1[0].split(',')
            """
            if is_repeat(name, date, list1[0]):
                return f'<a href="./"><p>error 404,{list1[0]} 提交重复 ，先查询确认后，请删除后再次提交</p></a>'
            """
            project = list1[0].replace(" ","")
            isPass = False
            for x in REPORT_LIST:
                if x == project:
                    isPass = True
            if not isPass:
                return error_page.format(f"{project} 名称不正确","请向系统管理员要求新增项目！")
            completion = float(list1[2].replace(" ",""))/100
            time = list1[5].replace(" ","")
            cmd = f"#@#@123@#@#|-|{name}|-|{project}|-|{date}|-|{list1[1]}|-|{completion}|-|{list1[3]}|-|{list1[4]}|-|{time}"
            ispass = send_put_day(cmd,date)
            if not ispass:
                return error_page.format(f"{cmd} 执行失败","请排查输入情况")
        else:
            for x in list_data1:
                list1 = x.split(',')
                """
                if is_repeat(name, date, list1[0]):
                    return f'<a href="./"><p>error 404,{list1[0]} 提交重复 ，先查询确认后，请删除后再次提交</p></a>'
                """
                project = list1[0].replace(" ", "")
                isPass = False
                if project == "其他":
                    project = '其它'
                for y in REPORT_LIST:
                    if y == project:
                        isPass = True
                if not isPass:
                    return error_page.format(f"项目 ：{project} 名称不正确，请重新填写，其它已经提交！","请向系统管理员要求新增项目！")
                completion = float(list1[2].replace(" ", "")) / 100
                time = list1[5].replace(" ", "")
                cmd = f"#@#@123@#@#|-|{name}|-|{project}|-|{date}|-|{list1[1]}|-|{completion}|-|{list1[3]}|-|{list1[4]}|-|{time}"
                ispass = send_put_day(cmd, date)
                if not ispass:
                    return error_page.format(f"{cmd} 执行失败","请排查输入情况")
        # #@#@DAY@#@#|-|name|-|date
        if name == "陈慧英":
            cmd = f'#@#@DAY@#@#|-|{name}|-|{date}|-|1'
        else:
            cmd = f'#@#@DAY@#@#|-|{name}|-|{date}|-|0'
        #ispass = send_day_report(cmd,date)
        t = threading.Thread(target=send_day_report_mail, args=(cmd,date)) #子线程发送邮件
        t.start()
        """
        if not ispass:#TODO 邮件
            return f'<a href="./"><p>error 404, 发送邮件失败 ，请重试</p></a>'
        """
    elif is_select == 2:
        # '#@#@555@#@#|-|0|-|list-tab|-|list-key'
        # String get_data = "#@#@555@#@#|-|1|-|name='"+getTesterName+"'|*|Project='"+getTesterProject+"'|*|date='"+geteditText_date+"'";
        name, date, list_data = get_client_data()
        date = str(date)
        cmd = f"#@#@555@#@#|-|1|-|name='{name}'|*|date='{date}'"
        isPass , data = send_get_day(cmd,date)
        if isPass:
            list_data = data.replace('),)',"").replace('),',"|-|").replace("(","").replace(")","").replace("'","")
            list_data1 = list_data.split("|-|")
            if len(list_data1) == 1:
                list_data = list_data.split(',')
                del list_data[1]
                del list_data[2]
            else:
                y = ''
                a = 1
                z = len(list_data1)
                for x in list_data1:
                    list1 = x.split(',')
                    del list1[1]
                    del list1[2]
                    if a < z:
                        y += str(list1)+"|-|"
                    else:
                        y += str(list1)
                    a += 1
                list_data = y
            list_data = str(list_data).replace('[','').replace(']','').replace("'","")

            result1 = """
                    <!DOCTYPE html>
                        <html>
                            <head>
                                <meta charset="utf-8">
                                <title></title>
                                <style>
                                .longtext50{
                                    overflow: hidden;
                                    white-space: nowrap;
                                    text-overflow: ellipsis;
                                    width: 50px;
                                }
                                
                                .longtext150{
                                    overflow: hidden;
                                    white-space: nowrap;
                                    text-overflow: ellipsis;
                                    width: 150px;
                                }
                                
                                .longtext{
                                    overflow: hidden;
                                    white-space: nowrap;
                                    text-overflow: ellipsis;
                                }
            """
            result2 = f"""
                                </style>
                            </head>
                            <body align="center">
                                <div style="width: 56%;margin: 0 auto;">
                                    
                                    <header align="center" >
                                        <div align="left" >
                                            <a href="./">
                                                <img src="https://www.meigsmart.com/userfiles/images/2020/03/23/2020032311354713.png" style="width: 200px;" alt="上海·美格" />
                                            </a>
                                        </div>
                                        <div align="center">
                                            <h1>日报系统</h1>
                                            <p><time pubdate datetime="2021-07-19"></time></p>
                                        </div>
                                    </header>
                                    
                                    
                                    <fieldset>
                                        <legend>查询结果 - {name} - {date}</legend>
                                            <form action="." method="POST">
                                                <input type="text" style="display: none;" value="{date}" name="date"/>
                                                <script type="text/javascript">
                                                
                                                    var data = "{list_data}";
                            """
            result3 = """
                                                    var x;
                                                    var y;
                                                    var z;
                                                    var list_data;
                                                    list_data = data.split("|-|");
                                                    document.write('<div style="display: flex;justify-content: center;">')
                                                    document.write('<table border="1">')
                                                    document.write('<tr>')
                                                    document.write('<th class="longtext50">id</th>')
                                                    document.write('<th class="longtext50">项目</th>')
                                                    document.write('<th class="longtext150">任务</th>')
                                                    document.write('<th class="longtext50">进度%</th>')
                                                    document.write('<th class="longtext150">简介</th>')
                                                    document.write('<th class="longtext150">备注</th>')
                                                    document.write('<th class="longtext50">工时</th>')
                                                    document.write('<th class="longtext50">选取</th>')
                                                    document.write('</tr>')
                                                    var iii = 0;
                                                    for(y in list_data){
                                                        x = list_data[y].split(",");
                                                        document.write('<tr>')
                                                        for(z in x){
                                                            document.write("<td class='longtext'>"+x[z]+"</td>")
                                                        }
                                                        document.write("<td>"+'<input type="checkbox" name="vehicle'+iii+'" value="'+x[0]+'">'+"</td>")
                                                        iii++;
                                                        document.write('</tr>')
                                                    }
                                                    document.write("</table>")
                                                    document.write("</div>")
                                                </script>
                                                <input type="submit" style="margin: 5px 0px 0px 2px;" name="my-del-day" value="删除选项" />
                                            </form>
                                    </fieldset>
                                    
                                    
                                    <footer align="center" >
                                        <p>美格 · 测试</p>
                                        <p><dfn><abbr title="发布时间：2021-07-20">版本：v2.00</abbr><a href="./update.html">更新日志</a></dfn></p>
                                        <p><time 发布日期时间="2021-07-20"></time></p>
                                    </footer>
                                    
                                </div>
                            </body>
                        </html>
            """

            return result1 + result2 + result3
        else:
            return error_page.format(f"{data} 数据错误","向管理员反馈次问题。")
    elif is_select == 3:# #@#@MONTH@#@#|-|mon
        date = request.form['start_time']
        ispass = True
        try:
            d = date.split('-')
            mon = d[1]
            cmd = f'#@#@MONTH@#@#|-|{mon}'
            #ispass , tap = send_cmd(cmd,date)
            year = int(d[0])
            momy = int(d[1])
            if year > 2030:
                ispass = False
            elif year < 2021:
                ispass = False
            elif momy < 1:
                ispass = False
            elif momy > 12:
                ispass = False
            else:
                t = threading.Thread(target=send_cmd, args=(cmd,date)) #子线程发送邮件
                t.start()
        except:
            ispass = False
        mon_result = f"""
                    <!DOCTYPE html>
                        <html>
                            <head>
                                <meta charset="utf-8">
                                <title>月报</title>
                                <meta http-equiv="refresh" content="5;url=./">
                            </head>
                            <body align="center">
                                <div style="width: 56%;margin: 0 auto;">

                                    <header align="center" >
                                        <div align="left" >
                                            <a href="./">
                                                <img src="https://www.meigsmart.com/userfiles/images/2020/03/23/2020032311354713.png" style="width: 200px;" alt="上海·美格" />
                                            </a>
                                        </div>
                                        <div align="center">
                                            <h1>日报系统</h1>
                                            <p><time pubdate datetime="2021-07-19"></time></p>
                                        </div>
                                    </header>


                                    <div style="margin: 100px 0px 100px 0px;">


                                        <h4 style="color: forestgreen;">{mon} 月  报发送成功!</h4>
                                        <p>5 秒后自动跳转</p>

                                    </div>




                                    <footer align="center" >
                                        <p>美格 · 测试</p>
                                        <p><dfn><abbr title="发布时间：2021-07-20">版本：v2.00</abbr><a href="./update.html">更新日志</a></dfn></p>
                                        <p><time 发布日期时间="2021-07-20"></time></p>
                                    </footer>

                                </div>
                            </body>
                        </html>
        """

        if ispass:
            return mon_result
        else:
            return error_page.format(f"日期 {date} 所在月份 查询失败","向管理员反馈此问题。")
    elif is_select == 4:# '#@#@456@#@#|-|id'

        del_result = """
        
                    <!DOCTYPE html>
                    <html>
                        <head>
                            <meta charset="utf-8">
                            <title>删除界面</title>
                            <meta http-equiv="refresh" content="5;url=./">
                        </head>
                        <body align="center">
                            <div style="width: 56%;margin: 0 auto;">
                                
                                <header align="center" >
                                    <div align="left" >
                                        <a href="./">
                                            <img src="https://www.meigsmart.com/userfiles/images/2020/03/23/2020032311354713.png" style="width: 200px;" alt="上海·美格" />
                                        </a>
                                    </div>
                                    <div align="center">
                                        <h1>日报系统</h1>
                                        <p><time pubdate datetime="2021-07-19"></time></p>
                                    </div>
                                </header>
                                
                                
                                <div style="margin: 100px 0px 100px 0px;">
                                    
                                    
                                    <h4 style="color: red;">{0}！</h4>
                                    <p>5 秒后自动跳转</p>
                                    
                                </div>
                                
                                
                                
                                
                                <footer align="center" >
                                    <p>美格 · 测试</p>
                                    <p><dfn><abbr title="发布时间：2021-07-20">版本：v2.00</abbr><a href="./update.html">更新日志</a></dfn></p>
                                    <p><time 发布日期时间="2021-07-20"></time></p>
                                </footer>
                                
                            </div>
                        </body>
                    </html>
                            
        """

        data = get_id()
        date = request.form['date']
        list_data = data.split(',')
        for x in list_data:
            try:
                int_x = int(x)
                ispass = send_del_report(int_x,date)
                if not ispass:
                    return error_page.format(f"删除 {int_x} 执行失败","向管理员反馈此问题。")
            except ValueError:
                pass
        return del_result.format(f"ID {list_data}已经全部删除成功！")
    elif is_select == 5:
        date = request.form['start_time']
        cmd = f"#@#@555@#@#|-|1|-|date='{date}'"
        isPass, data = send_get_day(cmd, date)
        if isPass:
            list_data = data.replace('),)', "").replace('),', "|-|").replace("(", "").replace(")", "").replace("'", "")
            list_data1 = list_data.split("|-|")
            if len(list_data1) == 1:
                list_data = list_data.split(',')
                del list_data[1]
                del list_data[2]
            else:
                y = ''
                a = 1
                z = len(list_data1)
                for x in list_data1:
                    list1 = x.split(',')
                    del list1[0]
                    del list1[2]
                    if a < z:
                        y += str(list1) + "|-|"
                    else:
                        y += str(list1)
                    a += 1
                list_data = y
            list_data = str(list_data).replace('[', '').replace(']', '').replace("'", "")

            result1 = """
                    <!DOCTYPE html>
                        <html>
                            <head>
                                <meta charset="utf-8">
                                <title></title>
                                <style>
                                .longtext50{
                                    overflow: hidden;
                                    white-space: nowrap;
                                    text-overflow: ellipsis;
                                    width: 50px;
                                }

                                .longtext150{
                                    overflow: hidden;
                                    white-space: nowrap;
                                    text-overflow: ellipsis;
                                    width: 150px;
                                }

                                .longtext{
                                    overflow: hidden;
                                    white-space: nowrap;
                                    text-overflow: ellipsis;
                                }
            """
            result2 = f"""
                                </style>
                            </head>
                            <body align="center">
                                <div style="width: 56%;margin: 0 auto;">

                                    <header align="center" >
                                        <div align="left" >
                                            <a href="./">
                                                <img src="https://www.meigsmart.com/userfiles/images/2020/03/23/2020032311354713.png" style="width: 200px;" alt="上海·美格" />
                                            </a>
                                        </div>
                                        <div align="center">
                                            <h1>日报系统</h1>
                                            <p><time pubdate datetime="2021-07-19"></time></p>
                                        </div>
                                    </header>


                                    <fieldset>
                                        <legend>查询结果 - 部门日报 - {date}</legend>
                                            <form action="." method="POST">
                                                <input type="text" style="display: none;" value="{date}" name="date"/>
                                                <script type="text/javascript">

                                                    var data = "{list_data}";
                            """
            result3 = """
                                                    var x;
                                                    var y;
                                                    var z;
                                                    var list_data;
                                                    list_data = data.split("|-|");
                                                    document.write('<div style="display: flex;justify-content: center;">')
                                                    document.write('<table border="1">')
                                                    document.write('<tr>')
                                                    document.write('<th class="longtext50">姓名</th>')
                                                    document.write('<th class="longtext50">项目</th>')
                                                    document.write('<th class="longtext150">任务</th>')
                                                    document.write('<th class="longtext50">进度%</th>')
                                                    document.write('<th class="longtext150">简介</th>')
                                                    document.write('<th class="longtext150">备注</th>')
                                                    document.write('<th class="longtext50">工时</th>')
                                                    document.write('</tr>')
                                                    var iii = 0;
                                                    for(y in list_data){
                                                        x = list_data[y].split(",");
                                                        document.write('<tr>')
                                                        for(z in x){
                                                            document.write("<td class='longtext'>"+x[z]+"</td>")
                                                        }
                                                        iii++;
                                                        document.write('</tr>')
                                                    }
                                                    document.write("</table>")
                                                    document.write("</div>")
                                                </script>
                                            </form>
                                    </fieldset>


                                    <footer align="center" >
                                        <p>美格 · 测试</p>
                                        <p><dfn><abbr title="发布时间：2021-07-20">版本：v2.00</abbr><a href="./update.html">更新日志</a></dfn></p>
                                        <p><time 发布日期时间="2021-07-20"></time></p>
                                    </footer>

                                </div>
                            </body>
                        </html>
            """

            return result1 + result2 + result3
        else:
            return error_page.format(f"{data} 数据错误", "向管理员反馈次问题。")
    elif is_select == 6:# #@#@PROJECTALL@#@#|-|project

        project_result = """
        
                        <!DOCTYPE html>
                            <html>
                                <head>
                                    <meta charset="utf-8">
                                    <title>项目总结</title>
                                    <style>
                                    .longtext50{
                                        overflow: hidden;
                                        white-space: nowrap;
                                        text-overflow: ellipsis;
                                        width: 50px;
                                    }
                                    
                                    .longtext150{
                                        overflow: hidden;
                                        white-space: nowrap;
                                        text-overflow: ellipsis;
                                        width: 150px;
                                    }
                                    
                                    .longtext{
                                        overflow: hidden;
                                        white-space: nowrap;
                                        text-overflow: ellipsis;
                                    }
                                    
                                    </style>
                                </head>
                                <body align="center">
                                    <div style="width: 56%;margin: 0 auto;">
                                        
                                        <header align="center" >
                                            <div align="left" >
                                                <a href="./">
                                                    <img src="https://www.meigsmart.com/userfiles/images/2020/03/23/2020032311354713.png" style="width: 200px;" alt="上海·美格" />
                                                </a>
                                            </div>
                                            <div align="center">
                                                <h1>项目总结</h1>
                                                <p><time pubdate datetime="2021-07-19"></time></p>
                                            </div>
                                        </header>
                                        
        """

        end_end = """
                                                        for(y in list_data){
                                                            x = list_data[y].split(",");
                                                            document.write('<tr>')
                                                            for(z in x){
                                                                document.write("<td class='longtext'>"+x[z]+"</td>")
                                                            }
                                                            document.write('</tr>')
                                                        }
                                                        document.write("</table>")
                                                        document.write("</div>")
                                                    </script>
                                        </fieldset>
                                        
                                        
                                        <footer align="center" >
                                            <p>美格 · 测试</p>
                                            <p><dfn><abbr title="发布时间：2021-07-20">版本：v2.00</abbr><a href="./update.html">更新日志</a></dfn></p>
                                            <p><time 发布日期时间="2021-07-20"></time></p>
                                        </footer>
                                        
                                    </div>
                                </body>
                            </html>

        """


        project_1 = request.form['project_1']
        date = str_Y_M_D()
        cmd = f'#@#@PROJECTALL@#@#|-|{date}|-|{project_1}'
        ispass , data = send_cmd(cmd,date)
        list_data = data.split("|-|")
        if "1" not in list_data[1]:
            return error_page.format(f"{project_1} 项目总结失败","向管理员反馈此问题。")
        new_data = list_data[2].replace('),)', "").replace("(", "").replace("'", "").replace('),', "|-|").replace(' ', "").replace('))', "")
        if not ispass:
            return error_page.format(f"{project_1} 总结失败！","向管理员反馈此问题。")

        end_result = f"""
                                        <fieldset>
                                            <legend>查询结果 - {project_1} - 项目总结</legend>
                                                    <script type="text/javascript">

                                                        var data = "{new_data}";
                                                        var x;
                                                        var y;
                                                        var z;
                                                        var list_data;
                                                        list_data = data.split("|-|");
                                                        document.write('<div style="display: flex;justify-content: center;">')
                                                        document.write('<table border="1">')
                                                        document.write('<tr>')
                                                        document.write('<th class="longtext50">id</th>')
                                                        document.write('<th class="longtext50">姓名</th>')
                                                        document.write('<th class="longtext150">项目</th>')
                                                        document.write('<th class="longtext150">日期</th>')
                                                        document.write('<th class="longtext150">任务</th>')
                                                        document.write('<th class="longtext50">进度%</th>')
                                                        document.write('<th class="longtext150">简介</th>')
                                                        document.write('<th class="longtext150">备注</th>')
                                                        document.write('<th class="longtext50">工时</th>')
                                                        document.write('</tr>')
        """

        return project_result+end_result+end_end
    else:
        return error_page.format("未知指令错误","向管理员反馈此问题。")


    result = f"""
            <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <title>日报结果</title>
                        <meta http-equiv="refresh" content="5;url=./">
                    </head>
                    <body align="center">
                        <div style="width: 56%;margin: 0 auto;">
                            
                            <header align="center" >
                                <div align="left" >
                                    <a href="./">
                                        <img src="https://www.meigsmart.com/userfiles/images/2020/03/23/2020032311354713.png" style="width: 200px;" alt="上海·美格" />
                                    </a>
                                </div>
                                <div align="center">
                                    <h1>日报系统</h1>
                                    <p><time pubdate datetime="2021-07-19"></time></p>
                                </div>
                            </header>
                            
                            
                            <fieldset>
                                <legend>提交结果 - {name} - {date}</legend>
                                    <script type="text/javascript">
                                    
                                        var data = "{list_data}";
    """
    end = """
                                        var x;
                                        var y;
                                        var z;
                                        var list_data;
                                        list_data = data.split("|-|");
                                        document.write('<div style="display: flex;justify-content: center;">')
                                        document.write('<table border="1">')
                                        document.write('<tr>')
                                        document.write('<th>项目</th>')
                                        document.write('<th>任务</th>')
                                        document.write('<th>进度%</th>')
                                        document.write('<th>简介</th>')
                                        document.write('<th>备注</th>')
                                        document.write('<th>工时</th>')
                                        document.write('</tr>')
                                        for(y in list_data){
                                            x = list_data[y].split(",");
                                            document.write('<tr>')
                                            for(z in x){
                                                document.write("<td>"+x[z]+"</td>")
                                            }
                                            document.write('</tr>')
                                        }
                                        document.write("</table>")
                                        document.write("</div>")
                                    </script>
                            </fieldset>
                            
                            <div style="margin: 100px 0px 100px 0px;">
                            <p style="color: red;">5 秒后自动跳转</p>
                            </div>


                            <footer align="center" >
                                <p>美格 · 测试</p>
                                <p><dfn><abbr title="发布时间：2021-07-20">版本：v2.00</abbr><a href="./update.html">更新日志</a></dfn></p>
                                <p><time 发布日期时间="2021-07-20"></time></p>
                            </footer>

                        </div>
                    </body>
                </html>
    """

    return result + end


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)