from zope.interface import implements
from twisted.plugin import IPlugin
from icommand import ICommand

import re
from lxml import objectify, html
import httplib2
from lib import reverse_list

class Utils(object):
    implements(IPlugin,ICommand)
    commands = {
                'autoc':'auto',
                'spell':'spell',
                's':'s'
                }
    name = "Utils"

    def __init__( self ):
        print "Utils object imported"

    def auto( self, bundle ):
        cursor = bundle['cursor']
        user = bundle['user']
        expr = bundle['idea'].split('/')[1:] # Just get the /<search>/<replace. Put in list
        channel = bundle['channel']
        sql = "select * from '%s' order by date desc limit 5" % re.escape(channel) # Unless there is crazy lag, if won't be that long ago
        cursor.execute(sql)
        lines = cursor.fetchall()
        auto_line=""
        for line in lines[1:]: # [1:] get's rid of the thing the user just said
            # first check if this line was said by the user
            line_un = line[2]
            if user == line_un:
                auto_line = line[3]
                break
        print auto_line
        if not auto_line:
            return "BUG_ON!"
        bundle['sensory_input'] = auto_line# The the R's !!
        return self.spell(bundle)

    def spell( self, bundle ):
        word = bundle['sensory_input']
        user = bundle['user']
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
        search = "http://www.google.com/base/feeds/snippets?q=%s" % query[1:] # There's an extra +
        print search
        resp, content = h.request( search ,"GET")
        lxml_html = html.fromstring(content)
        spell_link_objects = dict(lxml_html.xpath('//link')[1].items())
        m = re.search(r"spell=1",spell_link_objects['href'])
        if m:
            return spell_link_objects['title']
        else:
            return user+", sounds right to me"
        # kind of hackish. We need to wait for the popen to finish

    def s( self, bundle ):
        print "The bundle "+str(bundle)
        cursor = bundle['cursor']
        channel = bundle['channel']
        user = bundle['user']
        expr = bundle['msg'].split('/')[1:] # Just get the /<search>/<replace. Put in list
        sql = "select * from '%s' order by date desc" % re.escape(channel)
        print expr
        offset = 0
        try:
            offset = int(expr[2])
        except ValueError,e:
            print e
        if offset:
            sql = sql+" limit "+str(offset+1)
            print sql
        else:
            sql = sql+" limit 2"
            print sql
        cursor.execute(sql)
        lines = cursor.fetchall()
        lines = reverse_list(lines)
        string = str(lines[0][3])
        print string
        print expr
        print re.sub(expr[0],expr[1],string)
        return user+" meant to say: "+re.sub(expr[0],expr[1],string).strip()

utils = Utils()
