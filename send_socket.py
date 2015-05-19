__author__ = 'Claude'

import urllib
import httplib


def send_reply(data):
    data_url_encode = urllib.urlencode(data)
    reply = httplib.HTTPConnection("10.10.43.104", 8000, timeout=300)
    reply.request("POST", "/vmHost_reply", data_url_encode, {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"})
    http_response = reply.getresponse()
    print(http_response)