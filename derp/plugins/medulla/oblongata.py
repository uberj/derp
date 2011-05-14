from zope.interface import implements
from twisted.plugin import IPlugin
from icommand import ICommand

# Loading stuff
from derp.lib import libplugin
from twisted.plugin import getPlugins
from derp import plugins
from derp.plugins.isubroutine import ISubroutine

class Oblangata( object ):
    implements(IPlugin,ICommand)
    commands = {'think':'think'}
    name = "Oblangata"

    def __init__( self ):
        print "INIT"

    def think( self, bundle ):
        # Stop all tasks
        brain = bundle['brain']
        for name,sub in brain.sub_routines.items():
            sub.stop()
        # Restart all tasks
        for plugin in getPlugins(ISubroutine,plugins):
            l = task.LoopingCall( plugin.sub, protocol )
            brain.sub_routines[plugin.name] = l
            l.start(5)

obl = Oblangata()
