
# Credit Goes to dwestbrook on stack overflow
# http://stackoverflow.com/questions/211100/pythons-import-doesnt-work-as-expected
# HAKAKAKCKCKCKCK
# Need to put this in a more appropriate file
import sys
sys.path.append("/home/uberj/Herp/derp/")
import derp
from twisted.python.rebuild import rebuild

# Credit Goes to dwestbrook on stack overflow
# http://stackoverflow.com/questions/211100/pythons-import-doesnt-work-as-expected
def my_import( name ):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def load_plugins( interface , dictionary ):
    from twisted.plugin import getPlugins
    from derp import plugins
    #if not self.irc_auth.q_auth():
    if False:
        print "Plugins failed to load"
        return
    else:
        for plugin in getPlugins(interface,plugins):
            try:
                for cmd,fun in plugin.commands.items():
                    object_path = plugin.__module__+"."+plugin.name
                    rebuild(my_import(plugin.__module__))
                    print object_path
                    p_object = eval(object_path[5:])()
                    dictionary[cmd] = p_object.__getattribute__(fun)
                # Check to see whether this is a sub_routine. If it is add it to the sub dict.
            except AttributeError:
                print "Error on importing plugins: "+str(plugin)
        for key,value in dictionary.items():
            print str(key)+" : "+str(value)
