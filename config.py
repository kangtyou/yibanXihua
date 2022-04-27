# -*- coding: utf-8 -*-
"""
@Time ： 2021/8/24 12:28
@Auth ： apecode
@File ：config.py
@IDE ：PyCharm
@Blog：https://liuyangxiong.cn

"""

# ==========================================================

# Push Plus发信平台
# 官方网站：http://www.pushplus.plus
# 下方填写Token，微信扫码登录后一对一推送或一对多推送下面的token

# 推送优先级: 本地.log > 邮箱通知 > Push一对一推送

# 账号配置模板，多账号以逗号隔开
# {
#     "mobile": "易班账号(必要)",
#     "password": "易班密码(必要)",
#     "mail": "通知邮箱(非必要)",
#     "pushToken": "Push Plus Token(非必要)"
#     "notice": "local"(必要)    (通知方式，local：本地记录，mail：邮件通知，pp：Push Plus推送)，默认local
# },

# ==========================================================

import random

# 管理员设置
admin = {
    "mail": {
        "sendMail": "1573049371@qq.com",     # 发送人邮箱
        "authCode": "jhrjndjbpdomjfbe",     # 发送人邮箱授权码
        "smtpServer": "smtp.qq.com",
        "port": "465"
    }
}

# 账号设置
account = [
    {
        "mobile": "17683231030",
        "password": "patrick129",
        "mail": "1573049371@qq.com",
        "pushToken": "",
        "notice": ""
    }
]

# 表单：一天一次
task_once = {
    "6a2c48587652c472b625d612c03831eb": "是",
    "55e9aaf31b36aada75e4aa84f28827a4": str(round(random.uniform(36.1, 36.9), 1)),
    "8e62115236c4ec05c45daff18a6b0e1c": ["以上都无"],
    "0596b8e5dab5bbc35daea35e46a2fbfa": "好"
}

# 表单：早中晚
tasks = [
    # 晨检
    {
        "6a2c48587652c472b625d612c03831eb": "是",
         "55e9aaf31b36aada75e4aa84f28827a4": str(round(random.uniform(36.1, 36.9), 1)),
         "8e62115236c4ec05c45daff18a6b0e1c": ["以上都无"],
         "0596b8e5dab5bbc35daea35e46a2fbfa":"好"
    },
    # 午检
    {
        "fe92ae98382bd8107fdaebd40b87ac99": "是",
        "9c30f111dd364f6cac3c77eb57d8b1cc": str(round(random.uniform(36.1, 36.9), 1)),
        "0c57423a02438cba4aa3d8d36cce4f97": ["以上都无"],
        "f39426205cee2e3daaea202a62c98c0a": "好"
    },
    # 晚检
    {
        "1fc30eaae0d42b0b08bb76ac0bd54796": "是",
        "587168e43974c9f4e2657f40cc4f1090": str(round(random.uniform(36.1, 36.9), 1)),
        "25ba6951f05a36c89f289a905a83731b": ["以上都无"],
        "e6a93f2db5740f48d6d1a6f99133ad67":"好"
    }
]

xihua = {

    'Id': 'bce5f38f1140eb08e11885e667038f25',
    'WFName': '学生身体健康状况采集',
    'Form':[{
    '147371930756b00991e7bb9624f0d137': '37.2℃及以下',
    'e1237ee513e84575e4cba1b7f009b5f0': '健康',
    'ef9f971b44c6a67b9dd5263a9aa57cbe': '否',
    'a669262cc262cc42309afed5b456d845': '否',
    '9289a17bd856f28e6f6f7bc8f941722b': '是',
    '02df1388a840d9224bdc00f35cdabce6': {'time': '2022-04-26 02:01', 'longitude': 106.069485, 'latitude': 30.812159, 'address': '四川省南充市顺庆区风华路2号靠近中国电信(西华师范大学店)'}}]
}

xihua2 = {
    '147371930756b00991e7bb9624f0d137': '37.2℃及以下',
    'e1237ee513e84575e4cba1b7f009b5f0': '健康',
    'ef9f971b44c6a67b9dd5263a9aa57cbe': '否',
    'a669262cc262cc42309afed5b456d845': '否',
    '9289a17bd856f28e6f6f7bc8f941722b': '是',
    '02df1388a840d9224bdc00f35cdabce6': {'time': '2022-04-26 02:01', 'longitude': 106.069485, 'latitude': 30.812159, 'address': '四川省南充市顺庆区风华路2号靠近中国电信(西华师范大学店)'}}

# 地址
address = '{"Reason":"","AttachmentFileName":"","LngLat":"102.449018,24.875743","Address":"xxx省 xxx市 xxx学校 "}'
