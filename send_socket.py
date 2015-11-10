#coding:utf-8
__author__ = 'Claude'

import urllib
import httplib
from settings import IDASHBOARD_ADDRESS
from settings import IDASHBOARD_PORT


def send_reply(data):
    """
    以POST的HTTP方法向iDashBoard服务器发送反馈消息
    :param data: 需要发送的数据
    :return: 无返回值
    """
    data_url_encode = urllib.urlencode(data)
    reply = httplib.HTTPConnection(IDASHBOARD_ADDRESS, IDASHBOARD_PORT, timeout=300)
    reply.request("POST", "/reply_vmHost/", data_url_encode,
                  {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"})
    http_response = reply.getresponse()
    print(http_response)
