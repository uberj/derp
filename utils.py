import re

def s(string,channel_log):
    file = open(channel_log)
    lines = file.readlines()

    username = _get_username(lines.pop())
    if not username:
        return "i'm confused"
    expr = string.split('/')[1:] # Just get the /<search>/<replace. Put in list
    # Short circuit to find if we need to look at a
    # specific line
    if len(expr) > 2 and re.search('^\d*\d$',expr[2]):
        for i in range(int(expr[2])-1):
            print "pop"
            if lines:
                lines.pop()

    # We don't want to match what they just said ( derp will match .s/herp/derp )

    # Take the file and reverse the list. This will help us
    # match the first instance of string
    lines = _reverse_list(lines)
    s_line=""

    for line in lines:
        # first check if this line was said by the user
        line_un = _get_username(line)
        if username is line_un:
            continue
        # get rid of the stupid time stamp. We don't want to match that.
        line = re.sub('.*<.*> ','',line)
        if re.search(expr[0],line):
            s_line = line
            break

    print re.sub(expr[0],expr[1],s_line).strip()
    return username+" meant to say: "+re.sub(expr[0],expr[1],s_line).strip()

def _reverse_list(lst):
    r_lst=[]
    for line in lst:
        r_lst = [line] + r_lst
    return r_lst

def _get_username(line):
    #remeber the username
    m = re.match('.*<(.*)> ',line)
    if not m:
        return False
    username = m.groups()
    return username[0]
