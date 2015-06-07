__author__ = 'Claude'

import urllib
import httplib


def send_reply(data):
    data_url_encode = urllib.urlencode(data)
    reply = httplib.HTTPConnection("10.0.0.120", 8777, timeout=300)
    reply.request("POST", "/vmHost_reply", data_url_encode, {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"})
    http_response = reply.getresponse()
    print(http_response)