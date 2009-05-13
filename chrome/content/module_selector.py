from backend.bibleinterface import biblemgr
from module_tree_view import ModuleTreeView

treeView = None

def load_module_tree_view():
	global treeView
	treeView = ModuleTreeView()
	tree = document.getElementById("module_tree")
	tree.view = treeView
	treeView.setup_tree_events(tree)
	treeView.on_module_choice += lambda module, book: book.SetModule(module)
	biblemgr.bible.observers += lambda _: lookup_reference()

def lookup_reference():
	item = document.getElementById("toolbar_location")
	assert item
	dump("Looking up reference: %s" % item.value)
	browser = document.getElementById("browser")
	browser.setAttribute("src", "bpbible://%s/%s" % (biblemgr.bible.mod.Name(), item.value))

def set_browser_text(text):
	document.getElementById("bodycontent").innerHTML = text.replace("<!P>", "&lt;!P&gt;")
