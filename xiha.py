import json
import os
import time
import util
from yiban import Yiban
import config
from notice import Notice
from datetime import datetime, timedelta



for ac in config.account:
    yb = Yiban(ac.get("mobile"), ac.get("password"))
    notice = Notice(config.admin, ac)
    login = yb.login()
    if (login["response"]) != 100:
        print(login["message"])
        notice.send_mail(login["message"])

    else:       
        auth = yb.auth()
        if auth["code"] == 0:
            now_task = yb.getUncompletedListTime(datetime.now().strftime("%Y-%m-%d"),(datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d"))
            if not len(now_task["data"]):
                    print("没有找到要提交的表单")
                    notice.send_mail("没有找到要提交的表单")
            else:
                now_task_id = now_task["data"][0]["TaskId"]
                detail = yb.getDetail(now_task_id)
                extend = {
                        "TaskId": now_task_id,
                        "title": "任务信息",
                        "content": [
                            {"label": "任务名称", "value": detail["data"]["Title"]},
                            {"label": "发布机构", "value": detail["data"]["PubOrgName"]},
                            {"label": "发布人", "value": detail["data"]["PubPersonName"]}
                        ]
                    }
                form = config.xihua2
                #form['Id'] = yb.WFId
                #form['Form'][0]['02df1388a840d9224bdc00f35cdabce6']['time'] = datetime.now().strftime("%Y-%m-%d  %H:%M")
                form['02df1388a840d9224bdc00f35cdabce6']['time'] = datetime.now().strftime("%Y-%m-%d  %H:%M")
                sb_result = yb.submitApply(form, extend)
                if(sb_result['code'] == 0):
                    notice.send_mail('打卡成功!!!')
                else:
                    notice.send_mail('Something wrong!!!')
        else:
            print('认证失败')
            notice.send_mail('认证失败')
            