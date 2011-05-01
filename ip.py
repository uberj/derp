from lxml import objectify
import httplib2
import os
import time

def get_ip(user,channel, random_string ):
    h = httplib2.Http("myip")
    resp, content = h.request("http://ifconfig.me/all/xml","GET")
    # kind of hackish. We need to wait for the popen to finish
    root = objectify.fromstring(content)
    ip = root['ip_addr']
    print ip
    return ip
