# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.management.base import BaseCommand, CommandError
from push.tools import *


class Command(BaseCommand):
    help = "推送给客户端"

    def handle(self, *args, **options):
        ticker = "测试ticker"
        title = "测试title"
        text = "测试text"
        broad_cast_push_manager.push(
            payload=Payload(Body(ticker=ticker, title=title, text=text, after_open=AfterOpen.go_activity)
                            ))
