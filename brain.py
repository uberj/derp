#! /usr/bin/env python
# Database logging
import sqlite3
from plugins.ip import get_ip
from plugins.utils import s,spell,auto
from plugins.jokes import troll

# util libraries
import re
import time
from ConfigParser import ConfigParser

# Need to make this absolute eventually
PLUGIN_CONFIG = 'config/plugins.cfg'
GLOBAL_CONFIG = 'config/config.cfg'

class Brain:
    def __init__( self, channel ):
        self.config = ConfigParser()
        self.config.read(GLOBAL_CONFIG)
        self.c_token = self.config.get('command_token','token')
        # This will need to be ported when we leave sqlite3
        #db = self.config.get('database','path')
        db = 'db/channel_log'
        print db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        print "Going to use "+channel
        self.cursor.execute("""create table if not exists %s
                                (date text, channel text, user text, msg text)
                            """ % (channel))
        # LOAD THE PLUGINS OF DEATH!!!
        self.config = ConfigParser()
        self.thoughts={}
        self.load_plugins()

    def load_plugins( self ):
        self.config.read(PLUGIN_CONFIG)
        plugins = self.config.sections()
        p = __import__('plugins')
        reload(p)
        for plugin in plugins:
            # What's the lib function to just return the config as a dictionary?
            module = self.config.get(plugin,'file')[:-3]
            idea = self.c_token+self.config.get(plugin,'cmd')
            function = self.config.get(plugin,'fun')
            try:
                plugin = getattr( p, module )
                reload(plugin)
                action = getattr( plugin, function )
                self.thoughts[idea] = action
            except AttributeError:
                self.do_plugin_error(module,idea,function)
        print self.thoughts

    def contemplate(self,protocol,user,channel,msg):
        channel = re.sub('#+','',channel)
        # We only want to log and response to messages for registered tables.
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",[channel])
        # We have a table for that channel. Write to it.
        if self.cursor.fetchall():
            data = (str(time.time()),channel,user,msg)
            # It's safe to use channel because we already have a table called channel
            self.cursor.execute('insert into '+channel+' values (?,?,?,?)',data)
            self.conn.commit()
            # It is a command.
            if msg.startswith('.'):
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
                if idea in self.thoughts:
                    return self.thoughts[idea](bundle)
                elif re.match('.s/',idea):
                    print idea
                    # pass the whole message in
                    return self.thoughts['.s'](bundle)
        else:
            print "message from unknown channel "+channel
            print msg
            return None

    def do_plugin_error( self, module, idea, function ):
        print "Error importing %s%s function: %s" % (module,idea,function)
