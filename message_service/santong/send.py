# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import json
import uuid

import datetime

import requests
from django.conf import settings


def dahan_send_sms(phone, content):
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
