import mozutils
from backend.bibleinterface import biblemgr
import sys
from util.debug import dump
import util.dom_util

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

	text = biblemgr.bible.GetChapter(
		item.value
	)
	set_browser_text(text)

def set_browser_text(text):
	document.getElementById("bodycontent").innerHTML = text.replace("<!P>", "&lt;!P&gt;")

def do_load():
	util.dom_util.document = document
	lookup_reference()
	window.open('chrome://bpbible/content/module_selector.xul', '', 'chrome');

def run_dom_inspector():
	window.open("chrome://inspector/content/inspector.xul", "", "chrome");
