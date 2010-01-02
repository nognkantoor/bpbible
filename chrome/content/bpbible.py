import cgi
import reload_util
from swlib import pysw
from backend.bibleinterface import biblemgr
import mozutils
import config
from util.debug import dump, dprint, ERROR
from display_options import all_options, get_js_option_value, options

import util.dom_util
from xpcom import components

from util.debug import is_debugging
import frame_util

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
	print item
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
	browser.setAttribute("src", "bpbible://content/page/%s/%s" % (window.mod_name, i))
	document.title = get_window_title(i)

def process_tooltip():
	pt = document.getElementById("process_tooltip")
	d = pt.getAttribute("href")
	firer = pt.getAttribute("firer")
	leaving = pt.getAttribute("leaving") == "true"
	if leaving:
		frame_util.clear_tooltip(window)
		return

	f = window.content.document.getElementById(firer)
	if not f:
		print "No firer found????", firer
	
	frame_util.firer = f

	if not d: 
		# We reset it to make sure it changes; this is the reset, so ignore
		return
	
	print "Got it! was", d
	from protocols import protocol_handler
	protocol_handler.on_hover(window, d, 0, 0)
	
def do_load():
	util.dom_util.document = document
	lookup_reference()

	#window.open('chrome://bpbible/content/module_selector.xul', '', 
	#			'chrome,scrollbars,resizable');
	
def get_window_title(reference):
	return u"%s (%s) - BPBible" % (pysw.GetBestRange(reference, userOutput=True), window.mod_name)

def initialise_module_name(reference_item):
	print reference_item
	module_name = "ESV"
	if window.location.search:
		parameters = cgi.parse_qs(window.location.search[1:])
		if parameters.has_key("module_name"):
			module_name = parameters["module_name"][0]
		if parameters.has_key("reference"):
			print reference_item, "AND it's setAttribute", reference_item.setAttribute
			reference_item.setAttribute("value", parameters["reference"][0])
			#reference_item.value = parameters["reference"][0]
	dprint(ERROR, "Initialising module name to %s" % module_name)
	window.mod_name = module_name

def add_tooltip_handlers():
	b = document.createElement("broadcaster")
	b.id = "process_tooltip"
	o = document.createElement("observes")
	o.setAttribute("element", "process_tooltip")
	o.setAttribute("attribute", "href")
	o.addEventListener("broadcast", process_tooltip, False)
	document.documentElement.appendChild(b)
	document.documentElement.appendChild(o)
	tt = document.createElement("panel")
	tt.id = "tooltippanel"
	tt.setAttribute("noautofocus", "true")
	document.documentElement.appendChild(tt)

window.addEventListener("load", add_tooltip_handlers, False)
