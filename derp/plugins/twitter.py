from zope.interface import implements
from twisted.plugin import IPlugin
from icommand import ICommand

from twitter import TwitterHTTPError,oauth_dance
from ConfigParser import ConfigParser
config = "twitter.cfg"

class Twitter(object):
    implements(IPlugin,ICommand)
    commands = {'tweet':'tweet'}
    name = "Twitter"
    twitter = None
    def tweet(self, bundle):
        text = bundle['sensory_input']

    # Function taken from Rob McGuire-Dale
    # https://github.com/robatron/twitswarm/blob/master/twitswarm.py
    def authenticate(self):
        config = ConifgParser()
        config.read(config)
        app_name = "irc-bot-uberj"
        app_name = config.get('twitter','app_name')
        consumer_key = config.get('twitter','consumer_key')
        consumer_secret = config.get('twitter','consumer_secret')
        oauth = None
        print "Authenticating..."
        try:
            oauth_file = open("oauth.dat", 'r')
            oauth = pickle.load(oauth_file)
        except IOError:
            print "Oauth file not found. Starting twitter oauth dance."
            try:
                token_key, token_secret = oauth_dance.oauth_dance(
                        app_name, consumer_key,
                        consumer_secret)
                oauth = twitter.OAuth(token_key, token_secret,consumer_key, consumer_secret)
                oauth_file = open("oauth.dat",'w')
                pickle.dump(oauth, oauth_file)
            except TwitterHTTPError:
                print "Authentication error!"
                print "ding!"
                return
        self.oauth = Twitter(auth=oauth)
        print "Authenticated!"

    def authenticate(self):
        self.oauth = None
        print "Authenticating..."
        config = ConifgParser()
        config.read(config)
        app_name = "irc-bot-uberj"
        consumer_key = config.get('twitter','consumer_key')
        consumer_secret = config.get('twitter','consumer_secret')
        token_key = config.get('twitter','token_key')
        token_secret = config.get('twitter','token_secret')

        try:
            self.oauth = twitter.OAuth(token_key, token_secret,consumer_key, consumer_secret)
        except TwitterHTTPError:
            print "Authentication error!"
            return "ding!"

        self.twitter = Twitter(auth=oauth)
        print "Authenticated!"
