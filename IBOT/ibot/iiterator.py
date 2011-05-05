from twisted.plugin import getPlugins,IPlugin
import plugins

def main():
    for command in getPlugins(IPlugin,plugins):
        print "In the loop"
        bundle = "blah"
        print command.cmd(bundle)

if __name__=='__main__':
    main()

