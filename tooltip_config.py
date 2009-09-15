from backend.verse_template import VerseTemplate
from util.configmgr import config_manager
from backend.bibleinterface import biblemgr


tooltip_settings = config_manager.add_section("Tooltip")

tooltip_settings.add_item("plain_xrefs", False, item_type=bool)
tooltip_settings.add_item("border", 6, item_type=int)

def process_html_for_module(mod, text):
	# XUL TODO: make this work as expected
	return text


class TooltipConfig(object):
	def __init__(self, mod=None, book=None):
		self.tooltip = None
		self.mod = mod
		self.book = book
		self.scroll_to_current = False

	def get_module(self):
		if self.book:
			return self.book.mod

		return self.mod

	def another(self):
		"""Possibly duplicate this config if it stores any state, otherwise
		just return it as is"""
		return self

	def tooltip_changed(self):
		if self.tooltip:
			self.tooltip.update_text()

	def hide_tooltip(self):
		if self.tooltip:
			self.tooltip.HideTooltip()

	def bind_to_toolbar(self, toolbar):
		"""Rebind toolbar events for this new config"""
		pass
	
	def unbind_from_toolbar(self, toolbar):
		"""Unbind events, etc. from the toolbar. Called when the current
		config is removed."""
	
	def add_to_toolbar(self, toolbar, permanent):
		"""Called to add things to the tooltip's toolbar 
		(if anything needs to be added).
		
		This should return True if any items were added to the toolbar.
		"""
		return False
	
	def get_title(self):
		"""Gets the title to be used on a sticky tooltip."""
		return _("Sticky Tooltip")

	def get_text(self):
		"""Returns the actual text to be used for the tooltip."""
		return ""

class TextTooltipConfig(TooltipConfig):
	def __init__(self, text, mod):
		super(TextTooltipConfig, self).__init__(mod)
		self.text = text

	def get_text(self):
		"""Returns the actual text to be used for the tooltip."""
		return self.text

class StrongsTooltipConfig(TooltipConfig):
	def __init__(self, type, value):
		self.type = type
		self.value = value
		prefix = dict(Hebrew="H", Greek="G").get(type)
		
		module = "Strongs"+self.type #as module is StrongsHebrew
		mod = biblemgr.get_module(module)
		
		if prefix is not None:
			self.shortened = "%s%s" % (prefix, self.value)
		else:
			self.shortened = None	
	
		super(StrongsTooltipConfig, self).__init__(mod)
	
	def another(self):
		return StrongsTooltipConfig(self.type, self.value)

	def bind_to_toolbar(self, toolbar):
		toolbar.Bind(wx.EVT_TOOL,
			self.search,
			id=toolbar.gui_find.Id
		)

	def unbind_from_toolbar(self, toolbar):
		toolbar.Unbind(wx.EVT_TOOL)
		
	def add_to_toolbar(self, toolbar, permanent):
		#if not self.shortened: return False
		toolbar.gui_find = toolbar.AddLabelTool(wx.ID_ANY, 
			_("Find"),
			guiutil.bmp("find.png"),
			shortHelp=_("Search for this strong's number in the Bible"))

		self.bind_to_toolbar(toolbar)
		
		return True
	
	def search(self, event):
		if not self.shortened: return
		search_panel = guiconfig.mainfrm.bibletext.get_search_panel_for_frame()
		assert search_panel, "Search panel not found for %s" % guiconfig.mainfrm.bibletext
		self.hide_tooltip()
		search_panel.search_and_show("strongs:%s" % self.shortened)
	
	def get_text(self):
		if self.mod is None:
			tooltipdata = _("Module %s is not installed, "
			"so you cannot view "
			"details for this strong's number") %type
		
		else:
			#do lookup
			tooltipdata = biblemgr.dictionary.GetReferenceFromMod(
				self.mod, self.value)

		return tooltipdata

	
	
class BibleTooltipConfig(TooltipConfig):
	def __init__(self, references=None):
		super(BibleTooltipConfig, self).__init__(mod=None, book=biblemgr.bible)
		self.references = references
		self.toolbar = None
		self.is_bound = False
	
	def another(self):
		return BibleTooltipConfig(self.references)

	def bind_to_toolbar(self, toolbar):
		if not toolbar.permanent: return
		self.toolbar = toolbar
		import traceback
		assert not self.is_bound, self.is_bound
		self.set_refs(self.references, update=False)
		guiconfig.mainfrm.bible_observers += self.bible_ref_changed
		self.is_bound = ''.join(traceback.format_stack())
		
		toolbar.Bind(wx.EVT_TOOL, 
			lambda x:self.set_ref(toolbar.gui_reference.Value), 
			id=toolbar.gui_go.Id
		)
		
		toolbar.gui_reference.Bind(wx.EVT_TEXT_ENTER, 
			lambda x:self.set_ref(toolbar.gui_reference.Value))


		
		
	def unbind_from_toolbar(self, toolbar):
		if not toolbar.permanent: return

		assert self.is_bound
		guiconfig.mainfrm.bible_observers -= self.bible_ref_changed
		self.is_bound = False

		toolbar.Unbind(wx.EVT_TOOL, id=toolbar.gui_go.Id)
		toolbar.gui_reference.Unbind(wx.EVT_TEXT_ENTER)
		
	def add_to_toolbar(self, toolbar, permanent):
		toolbar.permanent = permanent
		if not permanent: return
		toolbar.gui_reference = wx.TextCtrl(toolbar,
				style=wx.TE_PROCESS_ENTER, size=(140, -1))

		toolbar.AddControl(toolbar.gui_reference)
		
		toolbar.gui_go = toolbar.AddLabelTool(wx.ID_ANY,  
			_("Go to verses"),
			guiutil.bmp("accept.png"),
			shortHelp=_("Open this reference")
		)

		return True

	def get_title(self):
		return "; ".join(GetBestRange(ref, userOutput=True) 
			for ref in self.references)

	def get_text(self):
		try:
			template = VerseTemplate(
				header="<a href='nbible:$internal_range'><b>$range</b></a><br>",
				body=u'<glink href="nbible:$internal_reference">'
					u'<small><sup>$versenumber</sup></small></glink> $text ')

			#no footnotes
			if tooltip_settings["plain_xrefs"]:
				biblemgr.temporary_state(biblemgr.plainstate)
			#apply template
			biblemgr.bible.templatelist.append(template)

			text = "<hr>".join(
				process_html_for_module(biblemgr.bible.mod, item)
				for item in biblemgr.bible.GetReferences(self.references)
			)

			return text

		finally:
			if tooltip_settings["plain_xrefs"]:
				biblemgr.restore_state()
			biblemgr.bible.templatelist.pop()
		
		
	def set_ref(self, reference):
		references = reference.split("|")
		return self.set_refs(references)
		
	def set_refs(self, refs, update=True):
		references = []
		try:
			context = "%s" % self.references[-1]
		except TypeError:
			context = ""
		for ref in refs:
			new_ref = self.get_verified_multi_verses(
				"%s" % ref, context
			)
			if new_ref is None:
				return

			context = new_ref
			references.append(new_ref)

		self.references = references

		reference_strings = '|'.join(
			GetBestRange(ref, userOutput=True) for ref in self.references
		)
		if self.toolbar.gui_reference:
			self.toolbar.gui_reference.ChangeValue(reference_strings)
		
		if update:
			self.tooltip_changed()

	def get_verified_multi_verses(self, ref, context):
		try:
			ref = GetBestRange(ref, context, raiseError=True, 
				userInput=True,	userOutput=False)
			return ref
		
		except VerseParsingError, e:
			wx.MessageBox(e.message, config.name())
	
	def bible_ref_changed(self, event):
		if event.settings_changed:
			self.tooltip_changed()

