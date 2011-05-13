from zope.interface import implements
from twisted.plugin import IPlugin
from isubroutine import ISubroutine
from icommand import ICommand

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

    def sub( self ):
        print "WORKS"
        #return str(self.rss_feeds)+"Downloading..."

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
        # Eventually migrate this to a db.
        return ['test.com']
rss = Rss()
