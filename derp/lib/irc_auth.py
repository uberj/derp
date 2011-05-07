import re
"""
 A class to hold a state machine to determine if someone is who they say they are.
 Parse the /msg info <nick> output.
"""
class admin_auth( object ):
    """
    NickServ derpxes Information on uberj (account uberj):
    NickServ derpxes Registered : Jun 21 23:52:09 2010 (45 weeks, 4 days, 19:51:10 ago)
    NickServ derpxes Last addr  : ~uberj@shell.onid.oregonstate.edu
    NickServ derpxes Last seen  : now
    NickServ derpxes Flags      : HideMail
    NickServ derpxes *** End of Info ***

    The plan:
        If the user has last seen "now" then they are online and registered (no one else can have their nick).
        If the user trying to authenticate has that same nick, then we know it's them and we confirm.
    """
    def __init__( self ):
        self.phase = 1
        self.authed = False
        self.user = ""

    def new_line( self, admin, line ):
        if self.phase is 1:
            m = re.search("account \x02(.*)\x02",line)
            if m:
                print m.groups(0)[0]
                # Are we dealing with an authorized user
                if m.groups(0)[0] == admin:
                    self.phase = 2
                    print "Phase 1 passed"
        elif self.phase is 2:
            m = re.match("Registered",line])
            if m:
                print "Phase 2 passed"
                self.phase = 3
        elif self.phase is 3:
            m = re.match("Last addr",line)
            if m:
                print "Phase 3 passed"
                self.phase = 4
        elif self.phase is 4:
            m = re.match("Last seen",line)
            status = line.split(":")
            self.phase = 5
            print "status is"
            print status
        elif self.phase is 5:
            self.phase is 6
        elif self.phase is 6:
            self.authed = True



    def de_auth( self ):
        self.authed = False

    def q_auth( self ):
        return self.authed
