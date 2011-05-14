from zope.interface import implements
from twisted.plugin import IPlugin
from icommand import ICommand


# Loading stuff
from derp.lib import libplugin
from twisted.plugin import getPlugins
from derp import plugins
from derp.plugins.isubroutine import ISubroutine

# Food for thought
from twisted.internet import reactor, task

class Oblangata( object ):
    implements(IPlugin,ICommand)
    commands = {'think':'think'}
    name = "Oblangata"

    def __init__( self ):
        print "INIT"
        # We should eventuall save state in here
        self.sub_routines = {}

    def think( self, bundle ):
        # Stop all tasks
        print bundle
        brain = bundle['brain']
        protocol = bundle['mouth']
        print self.sub_routines
        for name,sub in self.sub_routines.items():
            sub.stop()
            print sub
        # Restart all tasks
        for plugin in getPlugins(ISubroutine,plugins):
            l = task.LoopingCall( plugin.sub, protocol )
            self.sub_routines[plugin.name] = l
            l.start(5)

obl = Oblangata()
