import sys
import mozutils

def bpbible_doCommand(event):
	item_name = event.target.id
	print "Performing command", item_name
	if item_name == "menu_FileQuitItem":
		mozutils.doQuit(forceQuit=False)
	elif item_name == "aboutName":
		arguments = None
		window.openDialog("chrome://bpbible/content/about.xul", "about", "centerscreen,modal", arguments)
	elif item_name == "menu_Extensions":
		arguments = None
		window.openDialog("chrome://mozapps/content/extensions/extensions.xul?type=extensions", "about", "centerscreen,modal", arguments)		

def set_menu_items(document):
	for option in all_options():
		menu_item = document.getElementById("menu_%s" % option)
		if not menu_item:
			dprint(ERROR, "Couldn't find menu item for option ", option)
			continue

		if options.item_types[option] == str:
			print menu_item.tagName
			assert menu_item.tagName == "menu"
			cn = menu_item.firstChild.firstChild
			while cn:
				if "menu_" + options[option] == cn.id:
					cn.setAttribute("checked", "true")
					break
				#else:
				#	cn.removeAttribute("checked")

				cn = cn.nextSibling

			else:
				dprint(ERROR, "Couldn't find submenu item for option", 
					option, options[option])

		else:
			assert menu_item.tagName == "menuitem"

			if options[option]:
				menu_item.setAttribute("checked", "true")
			else:
				menu_item.removeAttribute("checked")

def set_menu_popup_state(event):
	set_menu_items(event.target.ownerDocument)

def set_init_menu_items():
	if not (sys.platform == 'darwin' or document.documentElement.hasAttribute("has-menu")):
		mb = document.getElementById("menubar_explorer")
		mb.setAttribute("hidden", "true")
		p = mb.parentNode
		p.removeChild(mb)
		if p.childNodes.length == 0:
			p.setAttribute("hidden", "true")
	else:
		popup = document.getElementById("popup_DisplayOptions")
		assert popup
		popup.addEventListener("popupshowing", set_menu_popup_state, False)

window.addEventListener("load", set_init_menu_items, False)

def toggle_option(event):
	value = event.target.hasAttribute("checked") and event.target.getAttribute("checked") != "false"

	# strip off menu_
	t = event.target
	option = t.id[5:]
	if option not in options.items:
		pp = t.parentNode.parentNode.id
		value = option
		
		# strip off menu_
		option = pp[5:]

	options[option] = value
	propagate_setting_change(option, get_js_option_value(option))

def propagate_setting_change(type, value):
	if not isinstance(value, str):
		raise TypeError("Wasn't a string (%r)" % value)

	wm = components.classes["@mozilla.org/appshell/window-mediator;1"]\
				   .getService(components.interfaces.nsIWindowMediator);  
	enumerator = wm.getEnumerator("")
	while enumerator.hasMoreElements():
		win = enumerator.getNext()
		print win.location.href
		if win.content and win.content.location.protocol == "bpbible:":
			body = win.content.document.body
			body.setAttribute(type, value)


def do_reloading(func):
	reload(reload_util)
	d = reload_util.__dict__[func] 
	if callable(d):
		d()
	else:
		reload_util.reboot_section(func)

import xpcom
class Observer(object):
	_com_interfaces_ = xpcom.components.interfaces.nsIObserver
	def observe(self, subject, topic, data):
		print "Observing", topic
		if topic == "xul-overlay-merged":
			print "merge"
			set_init_menu_items()
		else:
			print "Unknown topic", topic
			
