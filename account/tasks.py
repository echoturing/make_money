# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from message_service import service  as message_service
from push.tools import unicast_push_manager


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_sms(phone, token, expire="10"):
    message_service.send_sms(phone, token, expire)


@shared_task
def push(payload, _filter=None, device_token="", description=""):
    unicast_push_manager.push(payload=payload, _filter=_filter, device_token=device_token, description=description)
