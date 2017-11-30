# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import json

import time

import requests

APP_KEY = "5a030cc3aed179635800011c"
UMENG_MESSAGE_SECRET = "d27c252299d4656b338993a84800f8e6"  # 这好像没什么卵用?


class PushType(object):
    unicast = "unicast"
    broadcast = "broadcast"


class DisplayType(object):
    notification = "notification"
    message = "message"


class AfterOpen(object):
    go_app = "go_app"
    go_url = "go_url"
    go_activity = "go_activity"
    go_custom = "go_custom"


def get_time_stamp():
    return int(time.time())


def md5(s):
    m = hashlib.md5(s)
    return m.hexdigest()


class Body(object):
    def __init__(self, payload_display_type, after_open="", ticker="", title="", text="", url="", builder_id=0,
                 custom=""):

        if payload_display_type == DisplayType.message:
            assert custom != "", "display_type is {},custom should not be empty ".format(DisplayType.message)
        else:
            assert ticker != "" and title != "" and text != "" and after_open != "", \
                "display_type is notification,ticker title text should not be empty"
        if after_open == AfterOpen.go_url:
            assert url != "", "after open is {},url should not be empty!".format(AfterOpen.go_url)
        self.after_open = after_open
        self.payload_display_type = payload_display_type
        self.ticker = ticker
        self.title = title
        self.text = text
        self.url = url
        self.builder_id = builder_id
        self.custom = custom

    def to_dict(self):
        if self.payload_display_type == DisplayType.message:
            return {
                "custom": self.custom
            }
        return {
            "ticker": self.ticker,
            "title": self.title,
            "text": self.text,
            "after_open": self.after_open,
            "builder_id": self.builder_id,
        }


class Filter(object):
    def __init__(self, channels, provinces):
        """
        需要屏蔽的channel

        """

        self.channels = channels
        self.provinces = provinces

    def to_dict(self):
        channel_list = []
        province_list = []
        for channel in self.channels:
            channel_list.append(
                {
                    "not": {
                        "channel": channel,
                    }
                }
            )
        for province in self.provinces:
            province_list.append(
                {
                    "not": {
                        "province": province,
                    }
                }
            )

        return {
            "where": {
                "and": [
                    {
                        "and": channel_list,
                    },
                    {
                        "and": province_list
                    }
                ]
            }
        }


class Payload(object):
    def __init__(self, body, display_type):
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


class PushMessage(object):
    # base_url = "https://msgapi.umeng.com/api/send"
    base_url = "http://msg.umeng.com/api/send"
    method = "POST"
    app_master_secret = "xw3nhtfhjudmp5byvbtydnyz2j6uhlsl"
    type = "broadcast"
    session = requests.session()

    def __init__(self, appkey, type):
        """
        :type appkey:basestring
        """
        self.appkey = appkey
        self.type = type

    def sign(self, post_body, url):
        return md5('%s%s%s%s' % (self.method, url, post_body, self.app_master_secret))

    def push(self, payload, _filter=None, device_token="", description=""):
        """
        :type payload Payload
        :type _filter Filter
        :type device_token basestring
        :type description basestring
        """
        if self.type == PushType.broadcast:
            body_dict = {
                "appkey": self.appkey,
                "timestamp": get_time_stamp(),
                "type": self.type,
                "payload": payload.to_dict(),
            }
        else:
            body_dict = {
                "appkey": self.appkey,
                "device_tokens": device_token,
                "timestamp": get_time_stamp(),
                "type": self.type,
                "payload": payload.to_dict(),
            }
        if _filter:
            body_dict["filter"] = _filter.to_dict()

        body_dict["description"] = description

        post_body = json.dumps(body_dict)
        url = self.base_url + "?sign=" + self.sign(post_body, self.base_url)
        response = self.session.post(url, json=body_dict)
        print post_body
        print response.content

    def get_task_status(self, task_id):

        url = "http://msg.umeng.com/api/status"
        body_dict = {
            "appkey": self.appkey,
            "timestamp": get_time_stamp(),
            "task_id": task_id,
        }
        post_body = json.dumps(body_dict)
        url = url + "?sign=" + self.sign(post_body, url)
        response = self.session.post(url, json=body_dict)
        print response.content


broad_cast_push_manager = PushMessage(appkey=APP_KEY, type=PushType.broadcast)
unicast_push_manager = PushMessage(appkey=APP_KEY, type=PushType.unicast)
