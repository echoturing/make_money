# -*- coding: utf-8 -*-
import hashlib
import json
import random
import uuid

import datetime
import re
import requests
from django.conf import settings

PHONE_REG = re.compile("^(13[0-9]|14[579]|15[0-3,5-9]|17[0135678]|18[0-9])\\d{8}$")


def send_sms(phone, content):
    if settings.TEST:
        return {"msgid": "xxxxxxxxxxxxxx", "result": "0", "desc": "提交成功", "failPhones": ""}
    url = "http://www.dh3t.com/json/sms/Submit"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    message_id = uuid.uuid1().get_hex()
    password = hashlib.md5("2c052CH7")
    md5password = password.hexdigest()
    payload = {"account": "dh83501",
               "password": md5password,
               "msgid": message_id,
               "phones": phone,
               "content": content,
               "sign": "【资讯赚】",
               "subcode": "",
               "sendtime": datetime.datetime.now().strftime("%Y%m%d%H%M")
               }
    response = requests.post(url, json=payload, headers=headers)
    return json.loads(response.content)


def get_rand_int():
    if settings.TEST:
        return "1111"
    return str(random.randrange(1000, 9999))
