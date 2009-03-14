from backend.bibleinterface import biblemgr
from swlib.pysw import SW
from gui.tree_view import TreeItem, BasicTreeView
from util import _, languages
from util.observerlist import ObserverList
from util.unicode import to_unicode
from util.debug import dprint, ERROR

class ModuleTreeView(BasicTreeView):
	def __init__(self):
		super(ModuleTreeView, self).__init__()
		
		self.on_module_choice = ObserverList()
		self.on_category_choice = ObserverList()
		self.top_level_items = []

		self.module_types = (
			(_("Bibles"), biblemgr.bible),
			(_("Commentaries"), biblemgr.commentary),
			(_("Dictionaries"), biblemgr.dictionary),
			(_("Other books"), biblemgr.genbook),
		)

		self.on_selection += self.on_version_tree
		self.recreate()
	
	@property
	def blank_text(self):
		return _("Find Book...")

	def bind_events(self):
		super(ModuleTreeView, self).bind_events()
		
		#self.tree.Bind(wx.EVT_TREE_ITEM_MENU, self.version_tree_menu)
	
	def unbind_events(self):
		if not super(ModuleTreeView, self).unbind_events():
			return

		self.tree.Unbind(wx.EVT_TREE_ITEM_MENU)
		self.tree.Unbind(wx.EVT_TREE_DELETE_ITEM)
		
	def on_version_tree(self, item):
		if isinstance(item.data, SW.Module):
			self.on_module_choice(item.data, item.parent.data)
		else:
			self.on_category_choice(item.data, item.parent.data)
		
	def recreate(self):
		self.add_first_level_groups()

		for tree_item in self.top_level_items:
			self.add_children(tree_item)

		self.setup(self.top_level_items)
		self.expand_all()
		
	def version_tree_tooltip(self, event):
		item = event.GetItem()
		data = self.tree.GetPyData(item)
		if isinstance(data.data, SW.Module):
			event.SetToolTip(to_unicode(data.data.Description(), data.data))
		
	def version_tree_menu(self, event):
		item = event.GetItem()
		if not item:
			return

		data = self.tree.GetPyData(item).data

		if not isinstance(data, SW.Module): 
			return

		menu = wx.Menu()
		self.add_menu_items(data, menu)
		self.tree.PopupMenu(menu, event.GetPoint())
	
	def add_menu_items(self, data, menu):
		def make_event(module):	
			def show_information(event):
				#ModuleInfo(self, module).ShowModal()
				pass

			return show_information
	
		
		item = menu.Append(		
			wx.ID_ANY, 
			_("Show information for %s") % data.Name()
		)

		menu.Bind(wx.EVT_MENU, make_event(data), item)
	
	
	def add_first_level_groups(self):
		for text, book in self.module_types:
			self.top_level_items.append(TreeItem(text, data=book, filterable=False))

	def add_children(self, tree_item):
		modules = tree_item.data.GetModules()
		for module in modules: 
			self.add_module(tree_item, module)
	
	def add_module(self, tree_item, module, inactive_description=""):
		text = "%s - %s" % (
			module.Name(), to_unicode(module.Description(), module))
		
		if biblemgr.modules[module.Name()] != module:
			text += inactive_description

		tree_item.add_child(text, data=module)
	
class PathModuleTreeView(ModuleTreeView):
	def AppendItemToTree(self, parent, text):
		return self.tree.AppendItem(parent, text, ct_type=1)
		
	def add_first_level_groups(self):
		for path, mgr, modules in reversed(biblemgr.mgrs):
			self.top_level_items.append(TreeItem(path, data=mgr))
	
	def add_children(self, tree_item):
		for path, mgr, modules in reversed(biblemgr.mgrs):
			if mgr == tree_item.data:
				for modname, mod in sorted(modules, key=lambda x:x[0]):
					self.add_module(tree_item, mod, 
						"\nThis book is not active as it "
						"is shadowed by a book in a different path")
				break
		else:
			dprint(ERROR, "Did not find mgr in list", mgr)
	
class LanguageModuleTreeView(ModuleTreeView):
	def add_first_level_groups(self):
		language_mappings = {}
		self.data = {}
		for module in biblemgr.modules.values():
			lang = module.Lang()
			if lang not in language_mappings:
				language_mappings[lang] = \
					languages.get_language_description(lang)

			self.data.setdefault(lang, []).append(module)
		
		for lang, mapping in sorted(language_mappings.items(), 
			key=lambda (lang, mapping): mapping):
			self.top_level_items.append(TreeItem(mapping, data=lang))
	
	def add_children(self, tree_item):
		for mod in sorted(self.data[tree_item.data], 
							key=lambda mod:mod.Name()):
			self.add_module(tree_item, mod)
