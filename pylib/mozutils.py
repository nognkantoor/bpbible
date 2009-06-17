from xpcom import components as Components

import xpcom

try:
	# force map to be created
	str(xpcom.Exception(3))

	# now overwrite with a function which always puts the name in
	xpcom.Exception.__str__ = lambda x: "%d (%s)" % (x.errno, xpcom.hr_map[x.errno])
except Exception, e:
	print "EXCPTION", e

class KeysGetter(object): 
	def __get__(self, obj, objtype): 
		if obj is None: 
			print "OBJ IS NONE????"
			return [] 
		
		# This may be first time trying this interface - get the nsIClassInfo
		if not obj._tried_classinfo_:
			obj._build_all_supported_interfaces_()
	
		return obj._name_to_interface_iid_.keys()

xpcom.client.Component.__members__ = KeysGetter()

def doAlert(message, title=""):
	promptService =  Components.classes["@mozilla.org/embedcomp/prompt-service;1"].getService(Components.interfaces.nsIPromptService)
	promptService.alert(None, title, message)

def doQuit(forceQuit=False):
	appStartup = Components.classes['@mozilla.org/toolkit/app-startup;1'].getService(Components.interfaces.nsIAppStartup)
	  
	# eAttemptQuit will try to close each XUL window, but the XUL window can cancel the quit
	# process if there is unsaved data. eForceQuit will quit no matter what.
	if forceQuit:
		quitSeverity = Components.interfaces.nsIAppStartup.eForceQuit
	else:
		quitSeverity = Components.interfaces.nsIAppStartup.eAttemptQuit
	appStartup.quit(quitSeverity)
