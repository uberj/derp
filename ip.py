from lxml import objectify
import os
import time

def get_ip( random_string ):
    ip = os.popen('curl ifconfig.me/all/xml > myip')
    # kind of hackish. We need to wait for the popen to finish
    time.sleep(1)
    f = open('myip','r')
    root = objectify.fromstring(f.read())
    ip = root['ip_addr']
    os.popen('rm myip')
    f.close()
    print ip
    return ip
