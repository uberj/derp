from zope.interface import implements
from twisted.plugin import IPlugin
from icommand import ICommand

from twisted.internet import reactor
import time,random,re

# Fun stuff goes in here

class Jokes(object):
    implements(IPlugin,ICommand)
    commands = {'troll':'troll'}
    name = "Jokes"

    def __init__( self ):
        print "Jokes object imported"

    def troll(self,bundle):
        #protocol.msg(channel,"ponies")
        # I should try that call back thing...
        microphone = bundle['mouth']
        channel = bundle['channel']

        reactor.callLater(4,self.re_troll,bundle)
        return "ponies"

    def re_troll(self,bundle):
        resp = ["Only loosers like ponies","manatee: are you a pony?","your mom is a pony","lol","wtf","...well, someone is excited","o_0"]

        microphone = bundle['mouth']
        channel = bundle['channel']
        print channel
        cursor = bundle['cursor']
        sql =  "select * from '%s'\
                where user='uberj' and\
                date>%s and\
                msg='OMG!!! Ponies!!!'" % (re.escape(channel),str(time.time()-10))
        print sql
        cursor.execute(sql)
        troll_again = cursor.fetchall()
        print troll_again
        if troll_again:
            print "HERE"
            print str(channel)
            microphone.msg( channel,random.choice(resp) )
        else:
            return

jokes = Jokes()
