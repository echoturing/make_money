# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

from message_service.ccp.SendTemplateSMS import sendTemplateSMS
from message_service.santong.send import dahan_send_sms

TEMPLATE = "您的验证码是:{},{}分钟内有效"


def send_sms(phone, token, expire="10"):
    if settings.MESSAGE_USE == "1":
        # 老的短信接口
        content = TEMPLATE.format(token, expire)
        return dahan_send_sms(phone, content)
    else:
        # 新的
        sendTemplateSMS(phone, [token, ], "222280")
