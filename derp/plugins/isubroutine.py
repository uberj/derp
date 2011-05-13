from zope.interface import Interface, Attribute

# These classes will be ran at periodic intervals. They should always
# return defered objects.

class ISubroutine(Interface):
    def sub():
        """
        This function is the one that should spawn all the work in the
        subroutine. It will be the one called X seconds in the main reactor loop.
        @ type bundle blah
        @ param bundle blah
        """

    """
    The only difference between these Subroutines and Commands is that
    subroutines will be packed into a defered and called into a looping call.
    Commands are immediatly called and block until they are finished.
    """
