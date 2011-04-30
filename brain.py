#! /usr/bin/env python
# Plugin design developed by Rob McGuire-Dale

from ip import get_ip
class Brain:
    def __init__(self):
        self.thoughts={}
        self.load_plugins()

    def load_plugins(self):
        self.thoughts['.ip'] = get_ip

    def contemplate(self,idea,sensory_input):
        if idea in self.thoughts:
            return self.thoughts[idea](sensory_input)
        else:
            return "Uhh..."
