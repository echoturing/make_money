# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction

from account.models import UserProfile
from cash.models import CashRecord
from push.tools import unicast_push_manager, Body, Payload, DisplayType, AfterOpen


def generate_cash_record(user, money, phone, real_name, device_id, identity, machine_type, cash_type, device_brand,
                         channel, version_num):
    with transaction.atomic():
        user_profile = UserProfile.objects.select_for_update().get(user_id=user.id)
        if money > user_profile.balance:
            return 401, "提现金额大于已有金额"
        user_profile.balance -= money
        user_profile.cashed_balance += money
        user_profile.save()
        CashRecord.objects.create(user=user, money=money, phone=phone, real_name=real_name, device_brand=device_brand,
                                  device_id=device_id,
                                  identity=identity, machine_type=machine_type, cash_type=cash_type, channel=channel,
                                  version_num=version_num,
                                  )
        return 0, "提现记录生成成功"


def earn_gold(gold, user=None, user_profile=None):
    """
    获取金币的时候调用,除了金币增加以外,还会推送一条消息给别人
    :type user_profile UserProfile
    :type gold int
    :type user User
    """
    if user:
        user_profile = user.user_profile
    user_profile.gold += gold
    user_profile.save()
    device_token = user_profile.device_token
    ticker = "点击咨询奖励,{}金币已到手".format(gold)
    title = ticker
    text = " "

    builder_id = 1
    body = Body(payload_display_type=DisplayType.notification, after_open=AfterOpen.go_app, ticker=ticker, title=title,
                text=text, builder_id=builder_id)
    payload = Payload(display_type=DisplayType.notification, body=body)
    unicast_push_manager.push(payload, device_token=device_token)
