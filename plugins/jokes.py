# Fun stuff goes in here
import time
import random
import re
from lib import reverse_list,get_user

def troll(user,channel,word,protocol,channel_log):
    file = open(channel_log)
    lines = file.readlines()

    troll_more = 0
    resp = ["Only loosers like ponnies","manatee: are you a ponie?","your mom is a ponie","lol","wtf","...well, someone is excited","o_0"]
    protocol.msg(channel,"ponies")
    # OMG OMG I'M COMMITING THE ULTIMATE TWISTED SIN!!!
    # I should try that call back thing...
    time.sleep(2)

    # Clean up input
    lines = reverse_list(lines)
    # Take the file and reverse the list. This will help us
    # match the first instance of string
    for line in lines[:10]: #Only go 10 lines back.
        # first check if this line was said by the user
        line_un = get_user(line)
        print line_un
        print user
        if "manatee" == line_un:
            ponie_line = re.sub('.*<.*> ','',line)
            if re.search("PONIES",ponie_line):
                troll_more = 1

    if troll_more:
        return random.choice(resp)
    else:
        return "Where is the cow?"

