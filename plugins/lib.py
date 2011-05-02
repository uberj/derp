import re
# common functions
def reverse_list(lst):
    r_lst=[]
    for line in lst:
        r_lst = [line] + r_lst
    return r_lst

"""
Pass in a line for the log file and this function will parse the line and return a user name.
"""
def get_user(line):
    #remeber the user
    m = re.match('.*<(.*)> ',line)
    if not m:
        return False
    user = m.groups()
    return user[0].strip()
