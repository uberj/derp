from zope.interface import implements
from twisted.plugin import IPlugin
from icommand import ICommand

class Command(object):
    implements(IPlugin,ICommand)

    def __init__(self):
        self.x=3
        self.command = "ping"
    def cmd(self,bundle):
        print bundle

bot_command = Command()
