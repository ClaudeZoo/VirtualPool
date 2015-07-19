__author__ = 'Claude'

import urllib
import httplib


def send_reply(data):
    data_url_encode = urllib.urlencode(data)
    reply = httplib.HTTPConnection("127.0.0.1", 8000, timeout=300)
    reply.request("POST", "/reply_vmHost", data_url_encode, {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"})
    http_response = reply.getresponse()
    print(http_response)