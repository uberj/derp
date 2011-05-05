from zope.interface import Interface, Attribute

class ICommand(Interface):
    def cmd(bundle):
        """
        blah blag
        @ type bundle blah
        @ param bundle blah
        """

    command = Attribute("""The name of the command that the bot will pasre and look for.""")
