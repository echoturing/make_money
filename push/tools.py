# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import json

import time

import requests

APP_KEY = "5a030cc3aed179635800011c"
UMENG_MESSAGE_SECRET = "d27c252299d4656b338993a84800f8e6"  # 这好像没什么卵用?


class DisplayType(object):
    notification = "notification"
    message = "message"


def get_time_stamp():
    return int(time.time())


def md5(s):
    m = hashlib.md5(s)
    return m.hexdigest()


class Body(object):
    def __init__(self, ticker, title, text, after_open="go_app"):
        self.ticker = ticker
        self.title = title
        self.text = text
        self.after_open = after_open

    def to_dict(self):
        return {
            "ticker": self.ticker,
            "title": self.title,
            "text": self.text,
            "after_open": self.after_open,
        }


class Payload(object):
    def __init__(self, body, display_type=DisplayType.notification):
        """
        :type body Body
        :type display_type:basestring     notification-通知，message-消息

        """
        self.body = body
        self.display_type = display_type

    def to_dict(self):
        return {
            "display_type": self.display_type,
            "body": self.body.to_dict()
        }


class BroadCastPushMessage(object):
    base_url = "https://msgapi.umeng.com/api/send"
    method = "POST"
    app_master_secret = "xw3nhtfhjudmp5byvbtydnyz2j6uhlsl"
    type = "broadcast"
    session = requests.session()

    def __init__(self, appkey):
        """
        :type appkey:basestring
        :type timestamp:int
        :type payload:Payload
        """
        self.appkey = appkey

    def sign(self, post_body, ):
        return md5('%s%s%s%s' % (self.method, self.base_url, post_body, self.app_master_secret))

    def push(self, payload):
        body_dict = {
            "appkey": self.appkey,
            "timestamp": get_time_stamp(),
            "type": self.type,
            "payload": payload.to_dict()
        }
        post_body = json.dumps(body_dict)
        url = self.base_url + "?sign=" + self.sign(post_body)
        response = self.session.post(url, json=body_dict)
        print response.content


broad_cast_push_manager = BroadCastPushMessage(appkey=APP_KEY)
