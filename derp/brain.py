#! /usr/bin/env python
# Database logging
import sqlite3
# Plugin stuff
from twisted.python.rebuild import rebuild

# util libraries
import re
import time
from ConfigParser import ConfigParser

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
        self.cursor.execute("""create table if not exists %s
                                (date text, channel text, user text, msg text)
                            """ % (channel))
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

            for cmd,fun in plugin.commands.items():
                object_path = plugin.__module__+"."+plugin.name
                print plugin.__module__
                print object_path
                p_module = rebuild(self.my_import(plugin.__module__))
                p_object = eval(object_path[5:])()
                print cmd
                print fun
                self.thoughts[cmd] = p_object.__getattribute__(fun)
        print self.thoughts

    def contemplate(self,protocol,user,channel,msg):
        channel = re.sub('#+','',channel)
        # We only want to log and response to messages for registered tables.
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",[channel])
        # We have a table for that channel. Write to it.
        if self.cursor.fetchall():
            print self.c_token
            data = (str(time.time()),channel,user,msg)
            # It's safe to use channel because we already have a table called channel
            self.cursor.execute('insert into '+channel+' values (?,?,?,?)',data)
            self.conn.commit()
            # It is a command.
            if msg.startswith(self.c_token):
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
                print idea
                if idea[1:] in self.thoughts:
                    return self.thoughts[idea[1:]](bundle)
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
