#! /usr/bin/env python
# Database logging
import sqlite3
# Plugin stuff
from twisted.python.rebuild import rebuild

# util libraries
import re
import time
from ConfigParser import ConfigParser
from plugins import lib

# Need to make this absolute eventually
PLUGIN_CONFIG = 'Herp/config/plugins.cfg'
GLOBAL_CONFIG = 'config.cfg'

class Brain:
    def __init__( self, channel ):
        self.config = ConfigParser()
        self.config.read(GLOBAL_CONFIG)
        #self.c_token = self.config.get('command_token','token')
        path = self.config.get('base_directory','dir')
        self.c_token=self.config.get('command_token','token')
        # This will need to be ported when we leave sqlite3
        #db = self.config.get('database','path')
        db = path+'Herp/derp/db/channel_log'
        print db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        print "Going to use "+channel
        # Why are these subs here?
        # Unfortunatly, some characters do not play nicely with sqlit3. You also cannot parameratize
        # table names. Right now the best alternative I have is to just ditch the troublesome characters.
        # IMPORTANT: This is bad. The channel name has to be passed into all the plugins so they can respond
        # messages. Because of this, ONLY WHEN INSERTING INTO THE DATABASE MUST YOU CHANGE THE CHANNEL NAME.
        # at all other times you have to use the ACTUAL channel name. i.e. osu-lug for plugins, osulug for database.
        # Plug one million brownie points to whoever fixes this bug.

        self.cursor.execute("""create table if not exists '%s'
                                (date text, channel text, user text, msg text)
                            """ % re.escape("#"+channel))
        # LOAD THE PLUGINS OF DEATH!!!
        self.config = ConfigParser()
        self.thoughts={}
        self.load_plugins()

    # Credit Goes to dwestbrook on stack overflow
    # http://stackoverflow.com/questions/211100/pythons-import-doesnt-work-as-expected
    def my_import(self,name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def load_plugins( self ):
        from twisted.plugin import getPlugins,IPlugin
        import plugins
        for plugin in getPlugins(IPlugin,plugins):
            try:
                for cmd,fun in plugin.commands.items():
                    object_path = plugin.__module__+"."+plugin.name
                    print "HERE"
                    p_module = rebuild(self.my_import(plugin.__module__))
                    p_object = eval(object_path[5:])()
                    self.thoughts[cmd] = p_object.__getattribute__(fun)
            except AttributeError:
                print "Error on importing plugins: "+str(plugin)
        for key,value in self.thoughts.items():
            print str(key)+" : "+str(value)

    def contemplate(self,protocol,user,channel,msg):
        # We only want to log and response to messages for registered tables.
        self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='%s'""" % re.escape(channel))
        # We have a table for that channel. Write to it.
        if self.cursor.fetchall():
            data = (str(time.time()),channel,user,msg)
            # It's safe to use channel because we already have a table called channel
            self.cursor.execute("insert into '%s' values (?,?,?,?)" %re.escape(channel),data)
            self.conn.commit()
            # It is a command.
            if msg.startswith(self.c_token):
                print msg
                line = msg.split(' ')
                idea = line[0]
                sensory_input = ' '.join(line[1:])
                # There is a lot of resources to pass to each subroutine.
                # If you need to pass it something just add it to the bundle.
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
                if idea[1:] in self.thoughts:
                    return self.thoughts[idea[1:]](bundle)
                elif re.match(self.c_token+'s/',idea):
                    print idea
                    # pass the whole message in
                    return self.thoughts['s'](bundle)
        else:
            print "message from unknown channel "+channel
            print msg
            return None

    def do_plugin_error( self, module, idea, function ):
        print "Error importing %s%s function: %s" % (module,idea,function)
