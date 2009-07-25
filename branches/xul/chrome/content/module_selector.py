import urllib
from backend.bibleinterface import biblemgr
from module_tree_view import ModuleTreeView
from util import debug
from swlib.pysw import SW

treeView = None

def load_module_tree_view():
	window.mod = biblemgr.bible.mod
	global treeView
	treeView = ModuleTreeView()
	tree = document.getElementById("module_tree")
	tree.view = treeView
	treeView.setup_tree_events(tree)
	treeView.on_module_choice += on_module_choice
	tree.addEventListener("contextmenu", check_context_menu, True)

def set_browser_text(text):
	document.getElementById("bodycontent").innerHTML = text.replace("<!P>", "&lt;!P&gt;")

def on_module_choice(event_type, module, book):
	module_name = module.Name()
	debug.dprint(debug.ERROR, "event type", event_type, "module", str(module), module_name, "book", str(book))
	if event_type == "select":
		if book.is_verse_keyed:
			debug.dprint(debug.ERROR, 'Changing current module to', module_name)
			window.mod_name = module_name
			lookup_reference()
	elif event_type == "dblclick":
		if book.is_verse_keyed:
			reference = document.getElementById("toolbar_location").value
			debug.dprint(debug.ERROR, 'Loading Bible window', module_name, reference)
			url = ('chrome://bpbible/content/bible_window.xul?module_name=%s&reference=%s' %
				(urllib.quote(module_name), urllib.quote(reference)))
			bible_window = window.open(url, '', 'chrome,scrollbars,resizable')
		
		elif book.is_dictionary:
			debug.dprint(debug.ERROR, 'Loading Dictionary window', module_name)
			url = 'chrome://bpbible/content/dictionary_window.xul?module_name=%s' % urllib.quote(module_name)
			window.open(url, '', 'chrome,scrollbars,resizable')

		elif book.is_genbook:
			debug.dprint(debug.ERROR, 'Loading Genbook window', module_name)
			url = 'chrome://bpbible/content/genbook_window.xul?module_name=%s' % urllib.quote(module_name)
			window.open(url, '', 'chrome,scrollbars,resizable')
		


def check_context_menu(event):
	selection = treeView.visibleData[treeView.tree.currentIndex].data
	if not isinstance(selection, SW.Module):
		event.preventDefault()

def show_module_information():
	selection = treeView.visibleData[treeView.tree.currentIndex].data
	assert isinstance(selection, SW.Module)
	window.open(
		'chrome://bpbible/content/book_information_window.xul?module_name=%s' 
		% selection.Name(), '', 'chrome,scrollbars,resizable');
