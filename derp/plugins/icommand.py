from zope.interface import Interface, Attribute

# Idea. Make all public functions corrospond to commands. Use private functions for everything else.
class ICommand(Interface):
    def cmd(bundle):
        """
        blah blag
        @ type bundle blah
        @ param bundle blah
        """

    commands = Attribute("""List of the commands that the bot will pasre and look for.""")
