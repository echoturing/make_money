# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from account.models import UserProfile
from money.tool import get_rand_int, send_sms, get_obj_dict

EXPIRE = 600

TYPE_SIGN_UP = "SIGN_UP"
TYPE_RESET_PASSWORD = "RESET_PASSWORD"

SIGN_UP_PREFIX = "sign_up_"
RESET_PASSWORD_PREFIX = "reset_password_"


def get_reset_password_token(phone):
    """
    获取重置密码的验证码
    """
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
    """
    获取注册验证码
    """
    key = SIGN_UP_PREFIX + phone
    value = get_rand_int()
    cache.set(key, value, EXPIRE)
    content = "您的验证码是:{},10分钟内有效".format(value)
    response = send_sms(phone, content)
    return response


def validate_token(phone, token, typo):
    """
    验证码验证
    """
    key = ""
    if typo == TYPE_SIGN_UP:
        key = SIGN_UP_PREFIX + phone
    elif typo == TYPE_RESET_PASSWORD:
        key = RESET_PASSWORD_PREFIX + phone
    value = cache.get(key)
    if value == token:
        return True
    return False


def expire_token(phone, token, typo):
    """
    过期token
    """
    key = ""
    if typo == TYPE_SIGN_UP:
        key = SIGN_UP_PREFIX + phone
    elif typo == TYPE_RESET_PASSWORD:
        key = RESET_PASSWORD_PREFIX + phone
    cache.set(key, "", 0)


def actual_sign_up(phone, password, device_token):
    try:
        user = User.objects.get(username=phone)
        return user, 101, "该手机已经被注册"
    except ObjectDoesNotExist:
        user = User.objects.create_user(username=phone, password=password)
        user_profile, created = UserProfile.objects.get_or_create(user=user, device_token=device_token)
        user.save()
        user_profile.save()
        return user, 0, "注册成功"


def build_user_profile(user_profile):
    keys = ["gold", "balance", "cashed_balance", "total_get"]
    return get_obj_dict(user_profile, keys)


def build_user_info(user):
    keys = ["username", ]
    user_info = get_obj_dict(user, keys)
    try:
        user_profile = user.userprofile
        if user_profile:
            user_profile = build_user_profile(user_profile)
            user_info.update(user_profile)
    except ObjectDoesNotExist:
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        user_info.update(build_user_profile(user_profile))
    return user_info


def get_user_info(user_id):
    """
    获取用户首页信息
    """
    user = User.objects.select_related().get(id=user_id)
    return build_user_info(user)
