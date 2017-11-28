# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.management.base import BaseCommand, CommandError
from push.tools import *


class Command(BaseCommand):
    help = "推送给客户端"

    def handle(self, *args, **options):
        # self.unicast_push()
        self.unicast_push_message()

    def broad_cast_push_notification(self):
        ticker = "测试ticker"
        title = "测试title"
        text = "测试text"
        body = Body(ticker=ticker, title=title, text=text, after_open=AfterOpen.go_app, builder_id=0,
                    payload_display_type=DisplayType.notification)
        payload = Payload(body=body, display_type=DisplayType.notification)
        broad_cast_push_manager.push(payload=payload, _filter=None, device_token="")

    def unicast_push_message(self):
        body = Body(payload_display_type=DisplayType.message, custom="狗日的!")
        payload = Payload(body=body, display_type=DisplayType.message)
        unicast_push_manager.push(payload=payload, _filter=None,
                                  device_token="AlzA_cb8S5EG5FZfxUgCxfVrPiSqAgaZx3GhQpHDDfcB",
                                  description="这是测试单点message")

    def unicast_push_notification(self):
        ticker = "测试ticker1"
        title = "测试title1"
        text = "测试text1"
        body = Body(ticker=ticker, title=title, text=text, after_open=AfterOpen.go_app, builder_id=0,
                    payload_display_type=DisplayType.notification)
        payload = Payload(body=body, display_type=DisplayType.notification)
        unicast_push_manager.push(payload=payload, _filter=None,
                                  device_token="AlzA_cb8S5EG5FZfxUgCxfVrPiSqAgaZx3GhQpHDDfcB")

    def get_status(self):
        unicast_push_manager.get_task_status("")
