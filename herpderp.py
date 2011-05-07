#!/usr/bin/env python
# Modified from Twisted Matrix Laboratories.
from twisted.internet import reactor, protocol
from twisted.python import log
from twisted.words.protocols import irc

# system imports
import time, sys, os
from derp import brain
GLOBAL_CONFIG = 'config.cfg'
from ConfigParser import ConfigParser
from derp.lib import irc_auth

class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file

    def get_log(self):
        return self.file
    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


class HerpBot(irc.IRCClient):
    """A herping IRC bot."""
    nickname="derpxes"

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.factory.config.read(GLOBAL_CONFIG)
        self.admin = self.factory.config.get('admin','nick')
        self.auth = irc_auth.admin_auth()
        self.logger.log("[connected at %s]" %
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" %
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def test(self,channel, msg):
        print "HERE"
        self.msg("uberjderp","internel message")
        print "THERE"
        return

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("[%s] <%s> %s" % (channel,user, msg))

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            if user == "NickServ":
                print user+" "+channel+" "+msg
                if not self.auth.q_auth(): # We haven't confirmed anything
                    self.auth.new_line(self.admin,msg)
                else:
                    print "No auth"

            con_msg = msg.split(' ')
            if con_msg[0] == "!loadplugins":
                self.msg("NickServ","info "+user)
                """
                self.factory.config.read(GLOBAL_CONFIG)
                if len(msg) is 2 and msg[1] == self.factory.config.get('plugin_control','pswd'):
                    print "Loading plugins"
                    self.factory.brain.load_plugins()
                    # I should work in an error message into the plugin loading process.
                    self.msg(user,"Loaded plugins, check the log for success/failure")
                    return
                """

            """
            if user == "NickServ":
                #We don't want to respond to NickServ or ChanServ. We get stuck in an infinite loop.
                # BUGGGGGGYYYYY HAAACKK MY FACE
                print "NickServ: "+msg
                return
            self.msg(user, msg)
            """
        return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            msg = "%s: I've been derping really hard lately. I can't respond." % user
            print channel
            self.msg(channel, msg)
            self.logger.log("<%s> %s" % (self.nickname, msg))

        # If it is not a pm and not an action, then it must be someone speaking. Pass
        # their words into the brain and write it's response to the wire.
        response = self.factory.brain.contemplate(self,user,channel,msg)
        if response:
            self.msg(channel,response)
        return

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'



class HerpBotFactory(protocol.ClientFactory):
    """A factory for HerpBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = HerpBot

    def __init__(self, channel, filename):
        self.channel = channel
        self.filename = filename
        self.brain = brain.Brain(channel)
        self.config = ConfigParser()

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)

    # create factory protocol and application
    f = HerpBotFactory(sys.argv[1], sys.argv[2])

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
