from zope.interface import implements
from twisted.plugin import IPlugin
from icommand import ICommand

import twitter
from ConfigParser import ConfigParser
TWIT_CONFIG = "/home/uberj/Herp/derp/derp/plugins/twitter.cfg"

class Tweet(object):
    implements(IPlugin,ICommand)
    commands = {'tweet':'tweet'}
    name = "Tweet"
    def __init__( self ):
        self.authenticate()

    def tweet(self, bundle):
        text = bundle['sensory_input']
        user = bundle['user']
        if user == self.user:
            twitter.Twitter(auth=self.oauth).statuses.update(status=text)
        else:
            return "Nice try "+user

    def authenticate( self ):
        self.oauth = None
        print "Authenticating..."
        config = ConfigParser()
        config.read(TWIT_CONFIG)
        self.user = config.get('twitter','user')
        consumer_key = config.get('twitter','consumer_key')
        consumer_secret = config.get('twitter','consumer_secret')
        token_key = config.get('twitter','token_key')
        token_secret = config.get('twitter','token_secret')

        self.oauth = twitter.OAuth(token_key, token_secret,consumer_key, consumer_secret)

        print "Authenticated!"
        return

tweet = Tweet()
