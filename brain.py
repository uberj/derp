#! /usr/bin/env python
# Plugin design developed by Rob McGuire-Dale

from ip import get_ip
from utils import s,spell

import re
class Brain:
    def __init__(self,channel_log):
        self.thoughts={}
        self.channel_log=channel_log
        self.load_plugins()

    def load_plugins(self):
        self.thoughts['.ip']    = get_ip
        self.thoughts['.s']     = s
        self.thoughts['.spell'] = spell

    def contemplate(self,user,channel,msg):
        line = msg.split(' ')
        idea = line[0]
        sensory_input = ' '.join(line[1:])
        if idea in self.thoughts:
            return self.thoughts[idea](user,channel,sensory_input,self.channel_log)
        elif re.match('.s/',idea):
            # pass the whole messag in
            return self.thoughts['.s'](user,channel,msg,self.channel_log)
