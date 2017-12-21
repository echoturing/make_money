# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from account.models import UserProfile, GetGoldRecord
from account.tasks import send_sms
from ad.service import get_reward_cycle_json
from money.tool import get_rand_int, get_obj_dict, get_current_second
from django_redis import get_redis_connection

cache = get_redis_connection("default")
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
    send_sms.delay(phone, unicode(value))


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

    send_sms.delay(phone, unicode(value))


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


def get_user_by_username(username):
    try:
        user = User.objects.get(username=username)
        return user
    except ObjectDoesNotExist:
        return None


def create_get_gold_record(user, gold, group_id):
    return GetGoldRecord.objects.create(user=user, gold=gold, group_id=group_id)


JUDGE_KEY_PRE_FIX = "judge_key_pre_fix_"


def judge_in_set(user, group_id, reward_cycle):
    """
    判断这个group_id是不是这个用户已经领取过了
    """
    redis_key = JUDGE_KEY_PRE_FIX + str(user.id) + "_" + str(reward_cycle.id)
    in_set = cache.sismember(redis_key, group_id)
    return in_set


def add_judge(user, group_id, expire, reward_cycle):
    """
    把group_id弄进去,并且设置新的过期时间
    """
    redis_key = JUDGE_KEY_PRE_FIX + str(user.id) + "_" + str(reward_cycle.id)
    cache.sadd(redis_key, group_id)
    cache.expire(redis_key, expire)


def get_judge_set(user, reward_cycle):
    """
    获取用户的已领取的group_id
    """
    redis_key = JUDGE_KEY_PRE_FIX + str(user.id) + "_" + str(reward_cycle.id)
    result = cache.smembers(redis_key)
    if result:
        return list(map(lambda x: int(x), result))
    return []


def get_current_expire():
    """
    返回当前需要设置的过期时间
    秒
    """
    reward_cycle_json = get_reward_cycle_json()
    cycle_minutes = reward_cycle_json["cycle"]
    cycle_seconds = cycle_minutes * 60
    utc_now = timezone.now()
    current_seconds = get_current_second(utc_now)
    expire = cycle_seconds - (current_seconds % cycle_seconds)
    return expire
