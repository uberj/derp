#! /usr/bin/env python
# Database logging
import sqlite3

# Twisted stuff
from twisted.python.rebuild import rebuild
from twisted.internet import reactor, task
from plugins.icommand import ICommand
from plugins.isubroutine import ISubroutine

# util libraries
import re
import time
from ConfigParser import ConfigParser
from lib import irc_auth

# Need to make this absolute eventually
PLUGIN_CONFIG = 'Herp/config/plugins.cfg'
GLOBAL_CONFIG = 'config.cfg'

class Brain:
    def __init__( self, channel):
        # Config
        self.config = ConfigParser()
        self.config.read(GLOBAL_CONFIG)

        # Random stuff
        self.c_token=self.config.get('command_token','token')
        # TODO migrate admin from str to list
        # Line ~30 of irc_auth will need to be modified.
        self.admin = self.config.get('admin','nick')

        # Database
        path = self.config.get('base_directory','dir')
        db = path+'Herp/derp/db/channel_log'
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        print "Going to use "+channel
        self.cursor.execute("""create table if not exists '%s'
                                (date text, channel text, user text, msg text)
                            """ % re.escape("#"+channel))
        # AUTHENTICATION
        self.irc_auth = irc_auth.admin_auth(self.admin)

        # LOAD THE PLUGINS OF DEATH!!!
        self.config = ConfigParser()
        self.thoughts={}
        self.load_plugins( ICommand, self.thoughts)

        # Subconscious
        # All the classes that implement ISubroutine
        self.subconscious = {}
        # All the functions that are called routinely
        self.sub_routines = {}
        # Populate sub_routines
        self.load_plugins( ISubroutine, self.subconscious )
        self.start_subconscious()

    def start_subconscious( self ):
        for command,function in self.subconscious.items():
            s_obj = function.__self__
            l = task.LoopingCall(s_obj.sub)
            self.sub_routines[s_obj.name] = l
            l.start(2)

    def contemplate(self,protocol,user,channel,msg):
        # We have a table for that channel. Write to it.

        if self.channel_exists( channel ):
            self.log_to_channel( channel, user, msg )
            # It is a command.
            if msg.startswith(self.c_token):
                print msg
                # Parse the raw user input.
                line = msg.split(' ')
                idea = line[0][1:] # Drop the c_token
                sensory_input = ' '.join(line[1:])
                # There is a lot of resources to pass to each subroutine.
                # If you need to pass something, just add it to the bundle.
                bundle = {
                    'mouth': protocol, # write to this
                    'user': user,
                    'channel': channel,
                    'msg': msg, # full message
                    'idea': idea, # The fist half of the parsed message
                    'sensory_input': sensory_input, # The second half of the parsed message
                    'conn': self.conn,
                    'cursor': self.cursor, # access to the channel log via sqlite3
                         }
                if idea in self.thoughts:
                    return self.thoughts[idea](bundle)
                elif re.match('s/',idea):
                    return self.thoughts['s'](bundle)
        else:
            print "message from unknown channel "+channel
            print msg
            return None

    def personal_message( self, protocol, user, channel, msg):

        if user == "NickServ":
            print user+" "+channel+" "+msg
            if not self.irc_auth.q_auth(): # We haven't confirmed anything
                self.irc_auth.new_line( msg )
            else:
                print "No auth yet, in phase: "+str(self.irc_auth.phase)

        con_msg = msg.split(' ')
        if con_msg[0] == "!loadcommands" or con_msg[0] == "!loadsub" or con_msg[0] == "!think":
            self.irc_auth.reset_auth()
            protocol.msg("NickServ","info "+user)
            self.config.read(GLOBAL_CONFIG)
            # This function will check for a succesful auth
            if con_msg[0] == "!loadcommands":
                reactor.callLater(3,self.load_plugins, ICommand)
            elif con_msg[0] == "!loadsub":
                reactor.callLater(3,self.load_plugins, ISubroutine)
            else:
                self.start_subconcious()


    # Credit Goes to dwestbrook on stack overflow
    # http://stackoverflow.com/questions/211100/pythons-import-doesnt-work-as-expected
    def my_import(self,name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def load_plugins( self, interface , dictionary ):
        from twisted.plugin import getPlugins
        import plugins
        #if not self.irc_auth.q_auth():
        if False:
            print "Plugins failed to load"
            return
        else:
            for plugin in getPlugins(interface,plugins):
                try:
                    for cmd,fun in plugin.commands.items():
                        object_path = plugin.__module__+"."+plugin.name
                        # Could be un-needed.
                        #p_module = rebuild(self.my_import(plugin.__module__))
                        rebuild(self.my_import(plugin.__module__))
                        print object_path
                        p_object = eval(object_path[5:])()
                        dictionary[cmd] = p_object.__getattribute__(fun)
                except AttributeError:
                    print "Error on importing plugins: "+str(plugin)
            for key,value in dictionary.items():
                print str(key)+" : "+str(value)

    def log_to_channel( self, channel, user, msg ):
        data = (str(time.time()),channel,user,msg)
        # It's safe to use channel because we already have a table called channel
        self.cursor.execute("insert into '%s' values (?,?,?,?)" %re.escape(channel),data)
        self.conn.commit()
        return

    def channel_exists( self, channel ):
        # We only want to log and response to messages for registered tables.
        self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='%s'""" % re.escape(channel))
        return self.cursor.fetchall()

    def do_plugin_error( self, module, idea, function ):
        print "Error importing %s%s function: %s" % (module,idea,function)
