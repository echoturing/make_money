# -*- coding: utf-8 -*-
import random

from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from money.tool import get_rand_int, send_sms

EXPIRE = 600

TYPE_SIGN_UP = "SIGN_UP"
TYPE_RESET_PASSWORD = "RESET_PASSWORD"

SIGN_UP_PREFIX = "sign_up_"
RESET_PASSWORD_PREFIX = "reset_password_"


def get_reset_password_token(phone):
    key = RESET_PASSWORD_PREFIX + phone
    value = get_rand_int()
    cache.set(key, value, EXPIRE)
    content = "您的验证码是:{},10分钟内有效".format(value)
    response = send_sms(phone, content)
    return response


def actual_change_password(phone, password):
    try:
        user = User.objects.get(username=phone)
        user.set_password(password)
        user.save()
        return 0, "密码修改成功"
    except ObjectDoesNotExist:
        return 401, "账号不存在"


def get_sign_up_token(phone):
    key = SIGN_UP_PREFIX + phone
    value = get_rand_int()
    cache.set(key, value, EXPIRE)
    content = "您的验证码是:{},10分钟内有效".format(value)
    response = send_sms(phone, content)
    return response


def validate_token(phone, token, typo):
    key = ""
    if typo == TYPE_SIGN_UP:
        key = SIGN_UP_PREFIX + phone
    elif typo == TYPE_RESET_PASSWORD:
        key = RESET_PASSWORD_PREFIX + phone
    value = cache.get(key)
    if value == token:
        return True
    return False


def actual_sign_up(phone, password):
    try:
        user = User.objects.get(username=phone)
        return user, "该手机已经被注册"
    except ObjectDoesNotExist:
        user = User.objects.create_user(username=phone, password=password)
        user.save()
        return user, "注册成功"