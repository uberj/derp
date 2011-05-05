from twisted.plugin import getPlugins,IPlugin
from ibot import plugins

def main():
    for command in getPlugins(IPlugin,plugins):
        print "In the loop"
        bundle = "blah"
        print command
        print command.cmd(bundle)
        print(getPlugins(IPlugin))

if __name__=='__main__':
    main()
