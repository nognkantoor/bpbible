import cgi
import mozutils
from genbook_tree_view import GenbookTreeView
from backend.bibleinterface import biblemgr
from swlib import pysw
from util.debug import dump, dprint, ERROR
from util.unicode import to_unicode

tree_view = None

def on_load():
	global tree_view
	initialise_module_name()
	dprint(ERROR, str(biblemgr.genbook.is_gospel_harmony), str(biblemgr.genbook.mod.Name()))
	document.getElementById("reference_lookup_hbox").hidden = not biblemgr.genbook.is_gospel_harmony
	
	tree_view = GenbookTreeView(window.mod_name)
	genbook_tree = document.getElementById("genbook_tree")
	genbook_tree.view = tree_view
	genbook_tree.addEventListener("select", genbook_list_select, True)
	load_genbook_entry_by_index(0)

def genbook_list_select(event):
	index = document.getElementById("genbook_tree").currentIndex
	load_genbook_entry_by_index(index)

def load_genbook_entry_by_index(index):
	browser = document.getElementById("browser")
	data = tree_view.visibleData[index].data
	t = to_unicode(data.getText(), data.module)
	# Clear the window.
	browser.setAttribute("src", "bpbible://")
	browser.setAttribute("src", "bpbible://content/page/%s%s" % (window.mod_name, t))
	document.title = get_window_title(data)

def handle_reference_keypress(event):
	if event.keyCode == event.DOM_VK_RETURN:
		lookup_reference()

def go(event):
	lookup_reference()

def lookup_reference():
	item = document.getElementById("textbox_reference")
	assert item
	dump("Looking up reference in Genbook: %s" % item.value)
	try:
		reference = pysw.GetVerseStr(item.value, userInput=True, raiseError=True)
	except pysw.VerseParsingError, v:
		mozutils.doAlert(str(v))
		return

	genbook_key = biblemgr.genbook.find_reference(reference)
	dump("Reference maps to Genbook key: %s" % genbook_key)
	if genbook_key is None:
		mozutils.doAlert("%s is not in this harmony." % reference)
		return
	tree_view.go_to_key(genbook_key)

def get_window_title(data):
	return u"%s (%s) - BPBible" % (data.breadcrumb(), window.mod_name)

def initialise_module_name():
	module_name = "Josephus"
	if window.location.search:
		parameters = cgi.parse_qs(window.location.search[1:])
		if parameters.has_key("module_name"):
			module_name = parameters["module_name"][0]
	dprint(ERROR, "Initialising module name to %s" % module_name)
	window.mod_name = module_name
	biblemgr.genbook.SetModule(module_name, notify=False)
