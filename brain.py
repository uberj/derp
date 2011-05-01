#! /usr/bin/env python
# Plugin design developed by Rob McGuire-Dale

from ip import get_ip
from utils import s

import re
class Brain:
    def __init__(self,channel_log):
        self.thoughts={}
        self.channel_log=channel_log
        self.load_plugins()

    def load_plugins(self):
        self.thoughts['.ip'] = get_ip
        self.thoughts['.s']  = s

    def contemplate(self,idea,sensory_input):
        if idea in self.thoughts:
            return self.thoughts[idea](sensory_input)
        elif re.match('.s/',idea):
            return self.thoughts['.s'](idea,self.channel_log)
