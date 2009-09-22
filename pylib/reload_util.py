from xpcom import components
filtering = "quotes backend.filterutils backend.osisparser backend.thmlparser protocol_handlers"
tooltip_bits = filtering + " config frame_util tooltip_config protocols"
trees = "gui.tree_view module_tree_view genbook_tree_view"
ALL = "filtering tooltip_bits trees".split()

def reboot_section(name):
	for item in globals()[name].split():
		print "Reloading", item
		# fromlist non-empty means for A.B B is returned, not A
		# HACK: fromlist=True
		m = __import__(item, fromlist=True)
		reload(m)
	
	print "Reloaded", name

def reload_all():
	for item in ALL:
		reboot_section(item)

def reload_chrome():
	reload_all()
	components.classes["@mozilla.org/chrome/chrome-registry;1"] \
			  .getService(components.interfaces.nsIXULChromeRegistry) \
			  .reloadChrome()
