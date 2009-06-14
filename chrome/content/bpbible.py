import cgi
from swlib import pysw
import mozutils
import config
from util.debug import dump, dprint, ERROR
import util.dom_util
import util.i18n
if not hasattr(util.i18n, "langid"):
	util.i18n.initialize()

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

def do_load():
	util.dom_util.document = document
	lookup_reference()
	window.open('chrome://bpbible/content/module_selector.xul', '', 'chrome');

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
