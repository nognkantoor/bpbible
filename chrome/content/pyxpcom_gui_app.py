import mozutils
from backend.bibleinterface import biblemgr
import sys
from util.debug import dump

def pyxpcom_gui_app_doCommand(event):
	item_name = event.target.id
	print "Performing command", item_name
	if item_name == "menu_FileQuitItem":
		mozutils.doQuit(forceQuit=False)
	elif item_name == "menu_About":
		arguments = None
		window.openDialog("chrome://pyxpcom_gui_app/content/about.xul", "about", "centerscreen,modal", arguments)
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
	document.getElementById("bodycontent").innerHTML = text

def do_load():
	lookup_reference()

def run_dom_inspector():
	window.open("chrome://inspector/content/inspector.xul", "", "chrome");
