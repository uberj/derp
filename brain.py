#! /usr/bin/env python
# Database logging
import sqlite3
# Plugin design by Rob McGuire-Dale
from ip import get_ip
from utils import s,spell,auto
from jokes import troll
# util libraries
import re
import time

# This should eventually be migrated to a config file
DATABASE = "/home/uberj/derp/db/channel_logs_db"
class Brain:
    def __init__(self,channel_log,channel):
        self.thoughts={}
        self.channel_log=channel_log
        self.load_plugins()
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()
        print "Going to use "+channel
        self.cursor.execute("""create table if not exists %s
                                (date text, channel text, user text, msg text)
                            """%(channel))

    def load_plugins(self):
        self.thoughts['.ip']    = get_ip
        self.thoughts['.s']     = s
        self.thoughts['.spell'] = spell
        self.thoughts['.autoc'] = auto

    def contemplate(self,mouth,user,channel,msg):
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
                if idea == '.troll':
                    return troll(user,channel,sensory_input,mouth,self.channel_log)
                if idea in self.thoughts:
                    return self.thoughts[idea](user,channel,sensory_input,self.channel_log)
                elif re.match('.s/',idea):
                    # pass the whole messag in
                    return self.thoughts['.s'](user,channel,msg,self.channel_log)
        else:
            print "unknown message from channel "+channel
            return None
