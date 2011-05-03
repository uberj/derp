# Fun stuff goes in here
import time
import random
import re
from lib import reverse_list,get_user

from twisted.internet import reactor

def troll(bundle):
    #protocol.msg(channel,"ponies")
    # I should try that call back thing...
    print "Befor the reactor call"
    reactor.callLater(3,re_troll,bundle)
    print "After the reactor call"

def re_troll(bundle):
    resp = ["Only loosers like ponnies","manatee: are you a ponie?","your mom is a ponie","lol","wtf","...well, someone is excited","o_0"]

    print "I've been called back with the bundle "+str(bundle)
