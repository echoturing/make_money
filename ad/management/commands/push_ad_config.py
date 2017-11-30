# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.management.base import BaseCommand, CommandError

from ad.service import get_reward_cycle_json, get_current_filter, get_reward_cycle_count_json
from money.tool import need_push, get_current_minute, minutes_to_string_tuple
from push.tools import *

from django.utils import timezone


def get_current_body():
    reward_cycle_count_json = get_reward_cycle_count_json()
    reward_cycle_json = get_reward_cycle_json()
    cycle_minutes = reward_cycle_json["cycle"]
    hour_repr, minute_repr = minutes_to_string_tuple(cycle_minutes)
    cycle_count = reward_cycle_count_json["count"]
    ticker = "新红包来临,{}后过期,快抢!".format(hour_repr + minute_repr)
    title = "新红包来临,{}后过期,快抢!".format(hour_repr + minute_repr)
    text = "您有{}个红包待领取,快去领!".format(cycle_count)
    builder_id = 0
    return Body(payload_display_type=DisplayType.notification, after_open=AfterOpen.go_app, ticker=ticker, title=title,
                text=text, builder_id=builder_id)


def get_current_payload(body):
    return Payload(display_type=DisplayType.notification, body=body)


class Command(BaseCommand):
    help = "每分钟运行一次,看是否需要推送广告周期配置"

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', '-f', action='append', dest='force',
            help='是否强制推送',
        )

    def handle(self, *args, **options):
        force = options.get("force")
        utc_now = timezone.now()
        cycle = get_reward_cycle_json()["cycle"]
        if need_push(get_current_minute(utc_now), cycle) or force:
            # 推送
            _filter = get_current_filter()  # 屏蔽的省和渠道
            body = get_current_body()
            payload = get_current_payload(body)

            broad_cast_push_manager.push(payload=payload, _filter=_filter, description="")
