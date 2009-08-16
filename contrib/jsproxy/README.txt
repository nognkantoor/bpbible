
WARNING: The XPCOM Python/Javascript proxy is alpha quality software.
         It is still in development and will have bugs.
         ** The API is completely unstable and is likely to change. **

         
USAGE example for your python code (modified from real code - so currently untested but should work).

class MyProgressListerner(object):
    _com_interfaces_ = [ Components.interfaces.nsIWebProgressListener ]
    def onLocationChange(self, aWebProgress, aRequest, aLocation):
        if aRequest:
            print
            print 'Location change called', aRequest.name
            urlbar = document.getElementById('urlbar')
            urlbar.value = aRequest.name
    def onProgressChange(self, aWebProgress, aRequest, aCurSelfProgress, aMaxSelfProgress, aCurTotalProgress, aMaxTotalProgress):
        sys.stdout.write('.')
        sys.stdout.flush()
    def onSecurityChange(self, aWebProgress, aRequest, aState):
        sys.stdout.write('*')
        sys.stdout.flush()
    def onStateChange(self, aWebProgress, aRequest, aStateFlags, aStatus):
        if aRequest.name[0:4] != 'http':
            return
        if aWebProgress.isLoadingDocument:
            return
        if (aStateFlags & STATE_FLAGS.STOP) and (aStateFlags & STATE_FLAGS.WINDOW):
            print
            print 'Finished loading ', aRequest.name
    def onStatusChange(self, aWebProgress, aRequest, aStatus, aMessage):
        return

bproxy = None

def change_url(url):
    global bproxy  # should be using a controller class instead of globals
    
    browser = document.getElementById('browser')
    bproxy = jsproxy.JSProxy(browser)
    mylistener = MyProgressListerner()    
    bproxy.register(mylistener)
    bproxy.addProgressListener(mylistener, Components.interfaces.nsIWebProgress.NOTIFY_ALL)
    bproxy.loadURI(url, None, None)
