import re
from lxml import objectify
import httplib2

def auto(user,channel,word,channel_log):
    file = open(channel_log)
    lines = file.readlines()

    # Clean up input
    lines = _reverse_list(lines)
    # Take the file and reverse the list. This will help us
    # match the first instance of string
    lines = lines[1:] # get rid of the .autoc line
    auto_line=""
    for line in lines:
        # first check if this line was said by the user
        line_un = _get_user(line)
        print line_un
        print user
        if user == line_un:
            print line
            auto_line = re.sub('.*<.*> ','',line)
            break

    return spell(user,channel,auto_line,channel_log)

def spell(user,channel,word,channel_log):
    h = httplib2.Http()
    troll = re.match('^[ ]*$',word)
    if troll:
        return "The empty set contains the empty set"
    # strip extra spaces
    word = re.sub('^[ ]*','',word)

    # split+the+word+for+search+format
    words = word.split(' ')
    query = ""
    for bit in words:
        query=query+"+"+bit
    search = "http://www.google.com/base/feeds/snippets?q=%s" % query[1:] # There's and extra +
    print search
    resp, content = h.request( search ,"GET")
    m = re.search(r"spell=1' title='([ a-zA-Z'\"\[\]]*)'",content)
    if m:
        print m.groups()[0]
        return m.groups()[0]
    else:
        return user+", sounds right to me"
    # kind of hackish. We need to wait for the popen to finish

def s(user,channel,string,channel_log):
    print string
    file = open(channel_log)
    lines = file.readlines()

    expr = string.split('/')[1:] # Just get the /<search>/<replace. Put in list
    lines = _reverse_list(lines)
    # Short circuit to find if we need to look at a
    # specific line. They did a .s/xx/yy/4 to replace 4 lines up.
    if len(expr) > 2 and re.search('^\d*\d$',expr[2]):
        i = int(expr[2])
        while i > 0:
            username =_get_user(lines[0])
            if username == user:
                lines = lines[1:]
                i= i-1
            else:
                # We want to drop any cruft.
                lines = lines[1:]
    else:
        lines = lines[1:]

    # Take the file and reverse the list. This will help us
    # match the first instance of string
    for line in lines:
        # first check if this line was said by the user
        line_un = _get_user(line)
        if user is line_un:
            continue
        # get rid of the stupid time stamp. We don't want to match that.
        line = re.sub('.*<.*> ','',line)
        if re.search(expr[0],line):
            break

    print re.sub(expr[0],expr[1],line).strip()
    return user+" meant to say: "+re.sub(expr[0],expr[1],line).strip()

def _reverse_list(lst):
    r_lst=[]
    for line in lst:
        r_lst = [line] + r_lst
    return r_lst

def _get_user(line):
    #remeber the user
    m = re.match('.*<(.*)> ',line)
    if not m:
        return False
    user = m.groups()
    return user[0].strip()
