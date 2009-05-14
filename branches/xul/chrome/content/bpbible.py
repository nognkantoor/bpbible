from swlib import pysw
import mozutils
import config
from util.debug import dump
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
	assert item
	dump("Looking up reference: %s" % item.value)
	i = item.value
	try:
		i = pysw.GetVerseStr(item.value, userInput=True, raiseError=True)
	except pysw.VerseParsingError, v:
		mozutils.doAlert(str(v))
		return

	browser = document.getElementById("browser")

	# clear it
	browser.setAttribute("src", "bpbible://")

	# now set it
	browser.setAttribute("src", "bpbible://ESV/%s" % i)

def do_load():
	util.dom_util.document = document
	lookup_reference()
	window.open('chrome://bpbible/content/module_selector.xul', '', 'chrome');
