# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8a216da86010e69001602b081d750a67'

# 主帐号Token
accountToken = 'ccf1609d6a094c7383adcf140b1035b3'

# 应用Id
appId = '8aaf07086010a0eb01602b1ef4f60a7b'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.iteritems():

        if k == 'templateSMS':
            for k, s in v.iteritems():
                print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)


            # sendTemplateSMS(手机号码,内容数据,模板Id)
