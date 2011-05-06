from zope.interface import implements
from twisted.plugin import IPlugin
from icommand import ICommand

from lxml import objectify
import httplib2
import os
import time

class Network_Util(object):
    implements(IPlugin,ICommand)
    commands = {'ip':'ip'}
    name = "Network_Util"

    def ip( self , bundle ):
        h = httplib2.Http()
        resp, content = h.request("http://ifconfig.me/all/xml","GET")
        # kind of hackish. We need to wait for the popen to finish
        root = objectify.fromstring(content)
        ip = root['ip_addr']
        print "HERE"
        return "Dynamic plugins will dynamic reload."

nw_util = Network_Util()
