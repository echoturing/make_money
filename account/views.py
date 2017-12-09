# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from functools import update_wrapper

from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import HttpResponse, HttpRequest

from account import service
from account.models import UserFeedback
from account.service import create_get_gold_record, judge_in_set, add_judge, get_judge_set, get_current_expire
from cash import service as cash_service
from money.tool import CommonResponse

CONTENT_TYPE_JSON = "application/json"


def current_session_id_desc(func):
    def wrapper(request, *args, **kwargs):
        print request.COOKIES
        user = request.user
        if not user.is_authenticated():
            return HttpResponse(CommonResponse(error_code=401, error_message="用户未登录").to_json(),
                                content_type=CONTENT_TYPE_JSON)
        user_profile = user.userprofile
        current_session_id = request.session.session_key
        if user_profile.current_session_id != "" and current_session_id != user_profile.current_session_id:
            return HttpResponse(CommonResponse(error_code=401, error_message="用户未登录").to_json(),
                                content_type=CONTENT_TYPE_JSON)
        return func(request, *args, **kwargs)

    return update_wrapper(wrapper, func)


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
    device_token = param["device_token"]
    success = service.validate_token(phone, token, service.TYPE_SIGN_UP)
    if success:
        user, code, message = service.actual_sign_up(phone, password, device_token)
        if message:
            code = 0
        user = authenticate(username=phone, password=password)
        login(request, user)
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        user.userprofile.device_token = device_token
        user.userprofile.current_session_id = session_id
        user.userprofile.save()
        return HttpResponse(
            CommonResponse(error_code=code, error_message=message, data={"sessionid": session_id}).to_json(),
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
    device_token = param["device_token"]
    user = authenticate(username=phone, password=password)
    if user is not None:
        login(request, user)
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        user.userprofile.device_token = device_token
        user.userprofile.current_session_id = session_id
        user.userprofile.save()
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


@current_session_id_desc
def get_user(request):
    """
    :type request HttpRequest
    """
    return HttpResponse(request.user.username)


@current_session_id_desc
def user_info(request):
    """
    获取用户主页信息
    """
    user = request.user

    if not user.is_authenticated():
        return HttpResponse(CommonResponse(error_code=401, error_message="用户未登录").to_json(),
                            content_type=CONTENT_TYPE_JSON)

    data = service.get_user_info(user.id)
    data["group_id_list"] = get_judge_set(user)
    return HttpResponse(CommonResponse(error_code=0, error_message="", data=data).to_json(),
                        content_type=CONTENT_TYPE_JSON)


def earn_gold(request):
    """
    用户获取金币
    """
    param = json.loads(request.body)
    user = request.user
    if not user.is_authenticated():
        return HttpResponse(CommonResponse(error_code=401, error_message="用户未登录").to_json(),
                            content_type=CONTENT_TYPE_JSON)
    gold = param["gold"]
    group_id = param["group_id"]
    # 看看有没有领取过
    in_set = judge_in_set(user, group_id)
    if in_set:
        return HttpResponse(CommonResponse(error_code=401, error_message="该广告位金币已经领取").to_json(),
                            content_type=CONTENT_TYPE_JSON)

    with transaction.atomic():
        # 增加获取记录
        create_get_gold_record(user=user, gold=gold, group_id=group_id)
        # 增加金币并推送
        cash_service.earn_gold(gold=gold, user=user)
        expire = get_current_expire()
        add_judge(user, group_id, expire)
    return HttpResponse(CommonResponse(error_code=0, error_message="", data={}).to_json(),
                        content_type=CONTENT_TYPE_JSON)


def feedback(request):
    param = json.loads(request.body)
    user = request.user
    description = param.get("description")
    pictures = param.get("pictures", [])
    contact = param.get("contact")
    phone = param.get("phone")
    UserFeedback.objects.create(user=user, description=description, pictures=json.dumps(pictures), contact=contact,
                                phone=phone)

    return HttpResponse(CommonResponse(error_code=0, error_message="", data={}).to_json(),
                        content_type=CONTENT_TYPE_JSON)
