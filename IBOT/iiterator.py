
def main():
    from twisted.plugin import getPlugins,IPlugin,getCache
    from ibot import plugins
    for command in getPlugins(IPlugin,plugins):
        print "In the loop"
        bundle = "blah"
        print getCache(plugins)
        command.cmd(bundle)

if __name__=='__main__':
    main()
