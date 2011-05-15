from zope.interface import implements
from twisted.plugin import IPlugin
from isubroutine import ISubroutine
from icommand import ICommand

import feedparser

class Rss(object):
    implements(IPlugin,ISubroutine)
    commands = {'rss':'rss_util'}
    name = "Rss"

    """
    This should be where all the resources for this subroutine are stored.
    @ param grep_matter - any resources the brain passes to this object
      when creating it.
    """
    def __init__( self ):
        """
        We want state to be persistant over shut downs and reloads.
        Need a place to store where we are subscribing.
        One day it will be in a database wrapped in an ORM.
        """
        self.rss_feeds = self.get_feeds()
        # A list of channels to send rss updates to.
        # Manipulate this with rss_utils. Eventually let's save this to a config file/database
        self.channels = ["#uberj-test"]

    def sub( self, protocol ):
        print "THERE again again"
        #return str(self.rss_feeds)+"Downloading..."

    def send_to_channels( self ):

        for channel in self.channels:
            protocol.msg(channel, "ping")

    """
    Manipulate the RSS modules internal state.
    """
    def rss_util( self, bundle ):
        return "Rss Utility function"

    """
    Return a list of strings that point to rss feeds we are following.
    @return list
    """
    def get_feeds( self ):
        return ['test.com']

    def get_feed( self, url ):
        url = "http://feeds.arstechnica.com/arstechnica/security?format=xml"
        feeds = feedparser.parse(url)
        items = []
        for feed in feeds:
            items.extend(feed["items"])
        sorted = sorted(items, key=lambda item: item["date_parsed"])




rss = Rss()
