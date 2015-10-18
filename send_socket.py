__author__ = 'Claude'

import urllib
import httplib
from settings import IDASHBOARD_ADDRESS
from settings import IDASHBOARD_PORT


def send_reply(data):
    data_url_encode = urllib.urlencode(data)
    reply = httplib.HTTPConnection(IDASHBOARD_ADDRESS, IDASHBOARD_PORT, timeout=300)
    reply.request("POST", "/reply_vmHost/", data_url_encode,
                  {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"})
    http_response = reply.getresponse()
    print(http_response)
