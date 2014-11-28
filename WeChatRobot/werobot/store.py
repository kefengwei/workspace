# -*- coding: utf-8 -*-

import time
import requests
import client


from requests.compat import json as _json
from werobot.utils import to_text
client = Client('wx1c61843daa556523','0798b663ac452fdc9ec8c76d99751a17')
token = client.grant_token()
print token

class ClientException(Exception):
    pass


def check_error(json):
    """
    检测微信公众平台返回值中是否包含错误的返回码。
    如果返回码提示有错误，抛出一个 :class:`ClientException` 异常。否则返回 True 。
    """
    if "errcode" in json and json["errcode"] != 0:
        raise ClientException("{}: {}".format(json["errcode"], json["errmsg"]))
    return json


class Store(object):
    def __init__(self, appid, appsecret):
        self.appid = appid
        self.appsecret = appsecret
        self._token = None
        self.token_expires_at = None

    def request(self, method, url, **kwargs):
        if "params" not in kwargs:
            kwargs["params"] = {"access_token": token}
        if isinstance(kwargs.get("data", ""), dict):
            body = _json.dumps(kwargs["data"], ensure_ascii=False)
#            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        json = r.json()
        if check_error(json):
            return json

    def get(self, url, **kwargs):
        return self.request(
            method="get",
            url=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self.request(
            method="post",
            url=url,
            **kwargs
        )

    def  add_shop(self,shopdata):
        return self.post("https://api.weixin.qq.com/merchant/create?access_token=",
                         data = shopdata)