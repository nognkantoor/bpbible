import xpcom
from xpcom import shutdown
from xpcom import components

import config
# we have to import some of these first so they are registered
from backend import bibleinterface
import display_options
from util.configmgr import config_manager
import util.i18n

from util.debug import is_debugging
try:
	assert False
except AssertionError:
	if not is_debugging():
		print "WARNING: Assertions are on in release mode!"
else:
	if is_debugging():
		print """WARNING: Assertions are off in release mode!"""

def save_settings():
	print "Saving settings"
	config_manager.save()
	print "Done"

class StartupObserver(object):
	_com_interfaces_ = xpcom.components.interfaces.nsIObserver
	_reg_clsid_ = "{ac9063d0-c24f-41ca-b82a-e2bddd886061}"
	_reg_contractid_ = "@bpbible.com/startup;1"
	_reg_categories_ = [
		("app-startup", "Application Startup")
	]

	def __init__(self):
		self.register()

	def observe(self, subject, topic, data):
		print "Loading settings"
		util.i18n.initialize()
		config_manager.load()

		shutdown.register(save_settings)

	def register(self):
		observerService = components.classes["@mozilla.org/observer-service;1"]\
						  .getService(components.interfaces.nsIObserverService);
		observerService.addObserver(self, "app-startup", False);

	def unregister(self):
		### I just copy and pasted this - I don't think unregistering 
		### is necessary here
		observerService = components.classes["@mozilla.org/observer-service;1"]\
						.getService(components.interfaces.nsIObserverService);
		observerService.removeObserver(self, "app-startup");
