# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.management.base import BaseCommand, CommandError

from message_service.service import send_sms
from push.tools import *


class Command(BaseCommand):
    help = "XXX"

    def handle(self, *args, **options):
        print send_sms("15680515010", "5566")
