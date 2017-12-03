# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from account.views import CONTENT_TYPE_JSON, current_session_id_desc
from cash import service
from money.tool import CommonResponse


@current_session_id_desc
def generate_cash_record(request):
    """
    生成提现记录
    """
    param = json.loads(request.body)
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(CommonResponse(error_code=401, error_message="用户未登录").to_json(),
                            content_type=CONTENT_TYPE_JSON)

    money = param["money"]  # 提现金额
    phone = param["phone"]  # 提现人填写的手机号
    real_name = param.get("real_name", "")  # 真是姓名
    device_id = param.get("device_id", "")  # 设备id
    identity = param["identity"]  # 身份证号
    machine_type = param.get("machine_type", "")  # 机型  米6什么的
    device_brand = param.get("device_brand", "")  # 手机品牌
    cash_type = param.get("cash_type", "")  # 提现类型
    channel = param.get("channel", "")  # 渠道

    version_num = param.get("version_num", "")  # 版本号
    code, message = service.generate_cash_record(user=user, money=money, phone=phone, real_name=real_name,
                                                 device_id=device_id, channel=channel,
                                                 identity=identity, version_num=version_num,
                                                 machine_type=machine_type, cash_type=cash_type,
                                                 device_brand=device_brand)
    return HttpResponse(CommonResponse(error_code=code, error_message=message).to_json(),
                        content_type=CONTENT_TYPE_JSON)


def get_cash_config_view(request):
    cash_category_list = service.get_cash_config()
    return HttpResponse(
        CommonResponse(error_code=0, error_message="", data={"cash_category_list": cash_category_list}).to_json(),
        content_type=CONTENT_TYPE_JSON)
