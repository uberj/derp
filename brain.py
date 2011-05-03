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

class Brain:
    def __init__(self,channel_log,channel):
        self.thoughts={}
        self.plugins={}
        self.p_config = ConfigParser()
        print self.p_config
        #self.channel_log=channel_log
        #self.load_plugins()
        #self.conn = sqlite3.connect(DATABASE)
        #self.cursor = self.conn.cursor()
        #print "Going to use "+channel
        #self.cursor.execute("""create table if not exists %s
        #                        (date text, channel text, user text, msg text)
        #                    """%(channel))

    def parse_config(self):
        self.p_config.read(PLUGIN_CONFIG)
        plugins = self.p_config.sections()
        for plugin in plugins:
            # function called for plugin command
            action = self.p_config.options(plugin)
            self.plugins[plugin]=[action[0],self.p_config.get(plugin,action[0])]

        print self.plugins
        self.load_plugins()




    def load_plugins(self):
        for idea,action in self.plugins.items():
            __import__('plugins.ip',fromlist=['get_ip'])
            module = action[1][:-3]
            function = action[0]
            module_path = "plugins.%s." % module
            print module
            print function
            print module_path
            self.thoughs[idea] = __import__(module_path).module.function
        """
        self.thoughts['.ip']    = get_ip
        self.thoughts['.s']     = s
        self.thoughts['.spell'] = spell
        self.thoughts['.autoc'] = auto
        self.thoughts['.troll'] = troll
        """

    def contemplate(self,protocol,user,channel,msg):
        channel = re.sub('#+','',channel)
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
                            'mouth': protocol,
                            'user': user,
                            'channel': channel,
                            'msg': msg, # full message
                            'idea': idea, # The fist half of the parsed message
                            'sensory_input': sensory_input, # The second half of the parsed message
                            'conn': self.conn,
                            'cursor': self.cursor,
                            'log': self.channel_log # legacy code already?
                         }
                if idea in self.thoughts:
                    return self.thoughts[idea](bundle)
                elif re.match('.s/',idea):
                    print idea
                    # pass the whole message in
                    return self.thoughts['.s'](bundle)
        else:
            print "unknown message from channel "+channel
            return None
