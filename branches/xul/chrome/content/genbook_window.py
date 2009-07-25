import cgi
from gui.tree_view import BasicTreeView, LazyTreeItem
from swlib.pysw import ImmutableTK
from backend.bibleinterface import biblemgr
from util.debug import dump, dprint, ERROR
from util.unicode import to_unicode

tree_view = None

def on_load():
	global tree_view
	initialise_module_name()
	tk = biblemgr.genbook.GetKey()
	itk = ImmutableTK(tk)
	ImmutableTK.has_children = ImmutableTK.hasChildren
	
	tree_view = BasicTreeView()
	tree_view.setup(LazyTreeItem(itk), is_root=True)
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
