import cgi
from swlib import pysw
from backend.bibleinterface import biblemgr
import mozutils
import config
from util.debug import dump, dprint, ERROR
from display_options import all_options, get_js_option_value, options

import util.dom_util
from xpcom import components

from util.debug import is_debugging

def bpbible_doCommand(event):
	item_name = event.target.id
	print "Performing command", item_name
	if item_name == "menu_FileQuitItem":
		mozutils.doQuit(forceQuit=False)
	elif item_name == "menu_About":
		arguments = None
		window.openDialog("chrome://bpbible/content/about.xul", "about", "centerscreen,modal", arguments)
	elif item_name == "menu_Extensions":
		arguments = None
		window.openDialog("chrome://mozapps/content/extensions/extensions.xul?type=extensions", "about", "centerscreen,modal", arguments)		

def handle_location_keypress(event):
	if event.keyCode == event.DOM_VK_RETURN:
		lookup_reference()

def go(event):
	lookup_reference()

def lookup_reference():
	item = document.getElementById("toolbar_location")
	if not hasattr(window, "mod_name"):
		initialise_module_name(item)
	assert item
	dump("Looking up reference: %s" % item.value)
	i = item.value
	try:
		i = pysw.GetVerseStr(item.value, userInput=True, raiseError=True)
	except pysw.VerseParsingError, v:
		mozutils.doAlert(str(v))
		return

	dprint(ERROR, "window.mod_name", window.mod_name, "hasattr", hasattr(window, "mod_name"))
	browser = document.getElementById("browser")

	# clear it
	browser.setAttribute("src", "bpbible://")

	# now set it
	browser.setAttribute("src", "bpbible://%s/%s" % (window.mod_name, i))
	document.title = get_window_title(i)

def process_tooltip():
	d = document.getElementById("process_tooltip").getAttribute("attribute1")
	if not d: 
		# We reset it to make sure it changes; this is the reset, so ignore
		return
	
	print "Got it! was", d
	
def do_load():
	set_menu_items()
	util.dom_util.document = document
	lookup_reference()
	window.open('chrome://bpbible/content/module_selector.xul', '', 
				'chrome,scrollbars');
	
def get_window_title(reference):
	return u"%s (%s) - BPBible" % (pysw.GetBestRange(reference, userOutput=True), window.mod_name)

def initialise_module_name(reference_item):
	module_name = "ESV"
	if window.location.search:
		parameters = cgi.parse_qs(window.location.search[1:])
		if parameters.has_key("module_name"):
			module_name = parameters["module_name"][0]
		if parameters.has_key("reference"):
			reference_item.value = parameters["reference"][0]
	dprint(ERROR, "Initialising module name to %s" % module_name)
	window.mod_name = module_name

def set_menu_items():
	for option in all_options():
		menu_item = document.getElementById("menu_%s" % option)
		if not menu_item:
			dprint(ERROR, "Couldn't find menu item for option ", option)
			continue

		if options[option]:
			menu_item.setAttribute("checked", "true")

def toggle_option(event):
	checked = event.target.hasAttribute("checked")

	# strip off menu_
	option = event.target.id[5:]
	options[option] = checked
	propagate_setting_change(option, "true" if checked else "false")

def propagate_setting_change(type, value):
	assert isinstance(value, str), "Wasn't a string"
	wm = components.classes["@mozilla.org/appshell/window-mediator;1"]\
				   .getService(components.interfaces.nsIWindowMediator);  
	enumerator = wm.getEnumerator("")
	while enumerator.hasMoreElements():
		win = enumerator.getNext()
		print win.location.href
		if win.content and win.content.location.protocol == "bpbible:":
			body = win.content.document.body
			body.setAttribute(type, value)
