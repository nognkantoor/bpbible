from xpcom import components
def reboot_filtering():
	import backend.osisparser as o
	import backend.thmlparser as t
	import protocol_handlers as p
	import quotes as q
	for item in q, o, t, p:
		reload(item)
	
	print "Reloaded"

def reboot_bits():
	import tooltip_config as t	
	import protocols as p
	import frame_util as f
	reboot_filtering()
	for item in f, t, p:
		reload(item)
	
	print "Reloaded"

def reload_chrome():
	reboot_filtering()
	reboot_bits()
	components.classes["@mozilla.org/chrome/chrome-registry;1"] \
			  .getService(components.interfaces.nsIXULChromeRegistry) \
			  .reloadChrome()
