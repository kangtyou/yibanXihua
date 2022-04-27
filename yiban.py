# -*- coding: utf-8 -*-
"""
@Time ： 2020/8/10 上午11:40
@Auth ： apecode.
@File ： yiban.py
@Software  ： PyCharm
@Blog ： https://liuyangxiong.cn
"""
import json
import re
import sys
import os
import base64
from crypter import aes_encrypt

try:
    import requests
except ModuleNotFoundError:
    print("缺少requests依赖！程序将尝试安装依赖！")
    os.system("pip3 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.execl(sys.executable, 'python3', __file__, *sys.argv)

try:
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey import RSA
except ModuleNotFoundError:
    print("缺少pycryptodome依赖！程序将尝试安装依赖！")
    os.system("pip3 install pycryptodome -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.execl(sys.executable, 'python3', __file__, *sys.argv)


def encryptPassword(pwd):
    # 密码加密
    PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
        MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
        Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
        XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
        KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
        A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
        AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
        d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
        7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
        mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
        AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
        uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
        ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
        -----END PUBLIC KEY-----'''
    cipher = PKCS1_v1_5.new(RSA.importKey(PUBLIC_KEY))
    cipher_text = base64.b64encode(cipher.encrypt(bytes(pwd, encoding="utf8")))
    return cipher_text.decode("utf-8")


class Yiban:
    CSRF = "64b5c616dc98779ee59733e63de00dd5"
    AES_KEY = '2knV5VGRTScU7pOq'
    AES_IV = 'UmNWaNtM0PUdtFCs'
    COOKIES = {}
    HEADERS = {}

    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password
        self.session = requests.session()
        self.name = ""
        self.TaskId = ""
        self.WFId = ""
        self.HEADERS = {"Origin": "'https://m.yiban.cn", 'AppVersion': '5.0.1', "User-Agent": "YiBan/5.0.1"}
        self.COOKIES = {"csrf_token": self.CSRF}

    def request(self, url, method="get", params=None, cookies=None):
        if method == "get":
            response = self.session.get(url=url, timeout=10, headers=self.HEADERS, params=params, cookies=cookies)
        else:
            response = self.session.post(url=url, timeout=10, headers=self.HEADERS, data=params, cookies=cookies)
        return response.json()

    def login(self):
        """
        登录
        :return:
        """
        params = {
            "mobile": self.mobile,
            "password": encryptPassword(self.password),
            "ct": "2",
            "identify": "0",
        }
        # 新的登录接口
        response = self.request("https://mobile.yiban.cn/api/v4/passport/login", method="post", params=params,
                                cookies=self.COOKIES)
        if response is not None and response["response"] == 100:
            self.access_token = response["data"]["access_token"]
            self.HEADERS["Authorization"] = "Bearer " + self.access_token
            # 增加cookie
            self.COOKIES["loginToken"] = self.access_token
            return response
        else:
            return response

    def auth(self) -> json:
        """
        登录验证
        :return:
        """
        act = self.session.get("https://f.yiban.cn/iapp/index?act=iapp7463", allow_redirects=False,
                               cookies=self.COOKIES).headers["Location"]
        verifyRequest = re.findall(r"verify_request=(.*?)&", act)[0]
        self.HEADERS.update({
            'origin': 'https://app.uyiban.com',
            'referer': 'https://app.uyiban.com/',
            'Host': 'api.uyiban.com',
            'user-agent': 'yiban'
        })
        response = self.request(
            "https://api.uyiban.com/base/c/auth/yiban?verifyRequest=" + verifyRequest + "&CSRF=" + self.CSRF,
            cookies=self.COOKIES)
        self.name = response["data"]["PersonName"]
        return response

    def getUncompletedList(self) -> json:
        """
        获取未完成的表单
        :return:
        """
        response = self.request("https://api.uyiban.com/officeTask/client/index/uncompletedList?CSRF=" + self.CSRF,
                                cookies=self.COOKIES)
        return response

    def getUncompletedListTime(self, st, et) -> json:
        """
        获取特定时间未完成的表单
        :return:
        """
        response = self.request(
            "https://api.uyiban.com/officeTask/client/index/uncompletedList?StartTime=" + st + "&EndTime=" + et + "&CSRF=" + self.CSRF,
            cookies=self.COOKIES)
        return response

    def getCompletedList(self) -> json:
        """
        获取已经完成的表单
        :return:
        """
        return self.request("https://api.uyiban.com/officeTask/client/index/completedList?CSRF=" + self.CSRF,
                            cookies=self.COOKIES)

    def getDetail(self, taskId) -> json:
        """
        获取表单WFId
        获取发布人信息,后面提交表单时要用到
        :param taskId:
        :return:
        """
        response = self.request(
            "https://api.uyiban.com/officeTask/client/index/detail?TaskId=" + taskId + "&CSRF=" + self.CSRF,
            cookies=self.COOKIES)
        self.WFId = response['data']['WFId']
        self.TaskId = taskId
        self.Title = response['data']["Title"]
        self.PubOrgName = response["data"]["PubOrgName"]
        self.PubPersonName = response["data"]["PubPersonName"]
        return response

    def get_upload_data(self, initiateId):
        return self.request(
            "https://api.uyiban.com/workFlow/c/work/show/view/%s?CSRF=%s" % (initiateId, self.CSRF),
            cookies=self.COOKIES)

    def getFormapi(self) -> json:
        """
        首次使用,需要创建提交表单用的数据
        此方法是用来创建表单数据的
        :return:
        """
        response = self.request("https://api.uyiban.com/workFlow/c/my/form/%s?CSRF=%s" % (self.WFId, self.CSRF),
                                cookies=self.COOKIES)
        return response

    def nightAttendance(self, reason) -> json:
        """
        晚点名签到
        :param reason: 坐标信息
        :return:
        """
        params = {
            "Code": "",
            "PhoneModel": "",
            "SignInfo": reason,
            "OutState": "1"
        }
        response = self.request("https://api.uyiban.com/nightAttendance/student/index/signIn?CSRF=" + self.CSRF,
                                method="post", params=params, cookies=self.COOKIES)
        return response

    def submitApply(self, data, extend) -> json:
        """
        提交表单
        :param data: 提交表单的参数
        :param extend: 发布人信息
        :return: 表单url
        """
        params = {
            "Data": json.dumps(data, ensure_ascii=False),
            "Extend": json.dumps(extend, ensure_ascii=False),
            "WFId": self.WFId
        }
        params = json.dumps(params, ensure_ascii=False)
        # formtest = {'data': {'WFName': '学生身体健康状况采集', 'Process': {'WFId': 'bce5f38f1140eb08e11885e667038f25', 'Flow': [], 'CCTrigger': 'success'}, 'Approved': [], 'HasEditionAccess': False, 'HasInitiateLog': False, 'Initiate': {'Id': '3643cd685ae80af601848cddfde96c64', 'SerialNo': '20220426020141007963', 'UniversityId': '1a388b1e3eb6620a26622e46a6d7b7ac', 'PersonId': 'eddd66b2f86c12d1cd4685db1a66b9df', 'PersonInfo': {'College': '研究生院', 'Profession': '电子信息工程学院', 'Specialty': '电子信息', 'Class': '2021级', 'Grade': 2021, 'Campus': None, 'EducationLevel': 3, 'StudyYear': '3.0', 'Number': '212021085400028', 'Name': '王攀', 'Gender': 1, 'PersonType': 'student', 'Mobile': None}, 'WFId': 'bce5f38f1140eb08e11885e667038f25', 'ProcessId': '961f90b982fcdb281d2cc283d2822131', 'FormDataJson': [{'id': '147371930756b00991e7bb9624f0d137', 'label': '今日你的体温多少？', 'value': '37.2℃及以下', 'component': 'Radio'}, {'id': 'e1237ee513e84575e4cba1b7f009b5f0', 'label': '今日你的身体状况是？', 'value': '健康', 'component': 'Radio'}, {'id': 'ef9f971b44c6a67b9dd5263a9aa57cbe', 'label': '近14天你或你共同居住的人是否有疫情中高风险区域人员接触史？', 'value': '否', 'component': 'Radio'}, {'id': 'a669262cc262cc42309afed5b456d845', 'label': '你或你的共同居住人目前是否正被医学隔离？', 'value': '否', 'component': 'Radio'}, {'id': '9289a17bd856f28e6f6f7bc8f941722b', 'label': '本人是否承诺以上所填信息全部属实。准确，不存在任何隐瞒与不实', 'value': '是', 'component': 'Radio'}, {'id': '02df1388a840d9224bdc00f35cdabce6', 'label': '获取定位', 'value': {'time': '2022-04-26 02:01', 'longitude': 106.069485, 'latitude': 30.812159, 'address': '四川省南充市顺庆区风华路2号靠近中国电信(西华师范大学店)'}, 'component': 'AutoTakePosition'}], 'ExtendDataJson': {'TaskId': '6212ae117ab9d4d975aebfce48c3b3ee', 'title': '任务信息', 'content': [{'label': '任务名称', 'value': '4月25日——4月26日健康打卡'}, {'label': '发布机构', 'value': '2021级'}, {'label': '发布人', 'value': '魏书君'}]}, 'WorkNode': 0, 'State': 2, 'StateTime': '02:01', 'CreateTime': 1650909701}}}
        # formtest['data']['Initiate']['ExtendDataJson']['TaskId'] = self.TaskId
        # params = json.dumps(formtest, ensure_ascii=False)
        

        return self.request(
            "https://api.uyiban.com/workFlow/c/my/apply/?CSRF=%s" % (self.CSRF), method="post",
            params={'Str': aes_encrypt(self.AES_KEY, self.AES_IV, params)},
            cookies=self.COOKIES)

    def getShareUrl(self, key) -> json:
        """
        待更新....
        Key是随机生成的
        """
        return self.request(
            "https://app.uyiban.com/workFlow/client/#/share?Key=%s" % key,
            cookies=self.COOKIES)

    def photoRequirements(self):
        """
        晚点名签到所需
        :return:
        """
        return self.request(
            url="https://api.uyiban.com/nightAttendance/student/index/photoRequirements?CSRF=" + self.CSRF,
            cookies=self.COOKIES)

    def deviceState(self):
        """
        晚点名签到所需
        :return:
        """
        return self.request(url="https://api.uyiban.com/nightAttendance/student/index/deviceState?CSRF=" + self.CSRF,
                            cookies=self.COOKIES)

    def signPostion(self):
        """
        晚点名签到所需
        :return:
        """
        return self.request(url="https://api.uyiban.com/nightAttendance/student/index/signPosition?CSRF=" + self.CSRF,
                            cookies=self.COOKIES)
