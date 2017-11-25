# -*- coding: utf-8 -*-
from __future__ import unicode_literals

APP_KEY = "5a030cc3aed179635800011c"
UMENG_MESSAGE_SECRET = "d27c252299d4656b338993a84800f8e6"
APP_MASTER_SECRET = "xw3nhtfhjudmp5byvbtydnyz2j6uhlsl"

MESSAGE_URL_TEMPLATE = "https://msgapi.umeng.com/api/send?sign={sign}"


class Payload(object):
    def __init__(self, display_type, body):
        """
        :type display_type:basestring     notification-通知，message-消息
        """
        pass


class PushMessage(object):
    def __init__(self, appkey, timestamp, payload, type="broadcast"):
        """
        :type appkey:basestring
        :type timestamp:int
        :type payload:Payload
        :type type:basestring
        """
