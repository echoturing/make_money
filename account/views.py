# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response

from account import service
from money.tool import CommonResponse

CONTENT_TYPE_JSON = "application/json"


def sign_up_token(request):
    """
    :type request HttpRequest
    """
    param = json.loads(request.body)
    phone = param["phone"]
    result = service.get_sign_up_token(phone)
    return HttpResponse(CommonResponse(error_code=0, error_message="", data=result).to_json(),
                        content_type=CONTENT_TYPE_JSON)


def sign_up(request):
    """
    :type request HttpRequest
    """
    param = json.loads(request.body)
    phone = param["phone"]
    token = param["token"]
    password = param["password"]
    code = 0
    success = service.validate_token(phone, token, service.TYPE_SIGN_UP)
    if success:
        user, message = service.actual_sign_up(phone, password)
        if message:
            code = 101
        return HttpResponse(CommonResponse(error_code=code, error_message=message).to_json(),
                            content_type=CONTENT_TYPE_JSON)
    message = "验证码错误"
    code = 401
    return HttpResponse(CommonResponse(error_code=code, error_message=message).to_json(),
                        content_type=CONTENT_TYPE_JSON)


def sign_in(request):
    """
    :type request HttpRequest
    """
    param = json.loads(request.body)
    phone = param["phone"]
    password = param["password"]
    user = authenticate(username=phone, password=password)
    if user is not None:
        login(request, user)
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        data = {"sessionid": session_id}
        return HttpResponse(CommonResponse(error_code=0, error_message="登录成功", data=data).to_json(),
                            content_type=CONTENT_TYPE_JSON)
    return HttpResponse(CommonResponse(error_code=401, error_message="用户名或密码错误").to_json(), status=401,
                        content_type=CONTENT_TYPE_JSON)


def sign_out(request):
    """
    :type request HttpRequest
    """
    logout(request)
    return HttpResponse(CommonResponse(error_code=0, error_message="登出成功").to_json(), content_type=CONTENT_TYPE_JSON)


def reset_password(request):
    """
    :type request HttpRequest
    """
    param = json.loads(request.body)
    phone = param["phone"]
    token = param["token"]
    password = param["password"]
    success = service.validate_token(phone, token, service.TYPE_RESET_PASSWORD)
    if success:
        code, message = service.actual_change_password(phone, password)
        return HttpResponse(CommonResponse(error_code=code, error_message=message).to_json(),
                            content_type=CONTENT_TYPE_JSON)
    return HttpResponse(CommonResponse(error_code=401, error_message="验证码错误").to_json(), content_type=CONTENT_TYPE_JSON)


def reset_password_token(request):
    """
    :type request HttpRequest
    """
    param = json.loads(request.body)
    phone = param["phone"]
    result = service.get_reset_password_token(phone)
    return HttpResponse(CommonResponse(error_code=0, error_message="", data=result).to_json(),
                        content_type=CONTENT_TYPE_JSON)


def change_password(request):
    """
    :type request HttpRequest
    """
    param = json.loads(request.body)
    phone = param["phone"]
    old_password = param["old_password"]
    new_password = param["new_password"]
    user = authenticate(username=phone, password=old_password)
    if user:
        code, message = service.actual_change_password(phone, new_password)
        return HttpResponse(CommonResponse(error_code=code, error_message=message).to_json(),
                            content_type=CONTENT_TYPE_JSON)
    return HttpResponse(CommonResponse(error_code=401, error_message="旧密码错误").to_json(), content_type=CONTENT_TYPE_JSON)


def get_user(request):
    """
    :type request HttpRequest
    """
    return HttpResponse(request.user.username)
