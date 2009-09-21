from swlib.pysw import SW
from backend.bibleinterface import biblemgr
from tooltip_config import TextTooltipConfig, tooltip_settings, process_html_for_module, StrongsTooltipConfig, BibleTooltipConfig
from frame_util import get_module_for_frame, show_tooltip
from backend.verse_template import VerseTemplate


from util.debug import *
from util import noop
from util.unicode import to_unicode, to_str
#import guiconfig


class ProtocolHandler(object):
	def __init__(self):
		self.hover = {}
		self.protocols = {}
		#self.hover.name = "hovering"
		#self.hover.protocols = "opening link"
		
	def register_hover(self, protocol, handler):
		self.hover[protocol] = handler
	
	def register_handler(self, protocol, handler):
		self.protocols[protocol] = handler
		
	def on_hover(self, frame, href, x, y):
		self._handle(self.hover, frame, href, x, y)
	
	def on_link_opened(self, frame, href):
		self._handle(self.protocols, frame, href)
	
	def _handle(self, d, frame, href, *args):
		url = SW.URL(str(href))
		protocol = url.getProtocol()
		# don't decode if no protocol, or : in decoded may become the protocol
		if protocol:
			href = SW.URL.decode(str(href)).c_str()
			url = SW.URL(href)
			protocol = url.getProtocol()
		
		if protocol in d:
			d[protocol](frame, href, url, *args)
		else:
			dprint(WARNING, 
				"Protocol %s has no handler" % protocol,
				href)

protocol_handler = ProtocolHandler()

def on_web_opened(frame, href, url):
	guiutil.open_web_browser(href)

for item in ("http", "https", "ftp"):
	protocol_handler.register_handler(item, on_web_opened)
	protocol_handler.register_hover(item, noop)

def find_frame(module):
	for frame in guiconfig.mainfrm.frames:
		if hasattr(frame, "book") and frame.book.ModuleExists(module):
			return frame

def on_sword_opened(frame, href, url):
	module = url.getHostName()
	key = SW.URL.decode(url.getPath()).c_str()
	frame = find_frame(module)
	if not frame:
		return
	
	guiconfig.mainfrm.set_module(module, frame.book)
	
	frame.SetReference_from_string(
		to_unicode(
			key,
			frame.book.mod,
		)
	)
	

def on_sword_hover(frame, href, url, x, y):
	tooltip_config = TextTooltipConfig("", mod=None)

	module = url.getHostName()
	key = SW.URL.decode(url.getPath()).c_str()
	
	f = find_frame(module)
	if f:
		mod = biblemgr.get_module(module)
		mod.KeyText(key)
		
		ref = to_unicode(mod.getKeyText(), mod)
		ref = f.format_ref(mod, ref)
		text = mod.RenderText()

		tooltip_config.module = mod
		tooltip_config.text = ("%s (%s)<br>%s" % (
			ref, mod.Name(), text
		))
	else:
		tooltip_config.text = (
			_("The book '%s' is not installed, "
				"so you cannot view "
				"details for this entry (%s)") % (module, key))

	frame.show_tooltip(tooltip_config)

protocol_handler.register_handler("sword", on_sword_opened)
protocol_handler.register_hover("sword", on_sword_hover)

def on_hover_bible(frame, href, url, x, y):
	# don't show a tooltip if there is no bible
	if biblemgr.bible.mod is None:
		return

	ref = url.getHostName()
	if ref:
		references = [ref]
	else:
		values = url.getParameterValue("values")
		if not values:
			return

		references = [
			url.getParameterValue("val%s" % value)
			for value in range(int(values))
		]

	show_tooltip(frame, BibleTooltipConfig(references))

def on_hover_get_config(frame, href, url):
	print "ON HOVER", href
	def text_config(text, module=None):
		return TextTooltipConfig(text, mod=module or get_module_for_frame(frame))

	if url.getHostName() != "passagestudy.jsp":
		return

	action = url.getParameterValue("action")
	bible = biblemgr.bible
	dictionary = biblemgr.dictionary

	# set the tooltip's reference to this reference in case there is a
	# scripture note inside the note
	# e.g. first note in Matthew 2:1 in calvin's commentaries
	# XUL TODO: make this code work
	#if not hasattr(frame, "reference"):
	#	dprint(WARNING, "Frame didn't have reference")#, frame)
	#	frame.reference = ""

	#frame.tooltip.html.reference = frame.reference

	if action == "showStrongs":
		dictionary = biblemgr.dictionary		
		type = url.getParameterValue("type") #Hebrew or greek
		value = url.getParameterValue("value") #strongs number
		if not type or not value: 
			print "Not type or value", href
			return

		return StrongsTooltipConfig(type, value)

	elif action=="showMorph":
		type = url.getParameterValue("type") #Hebrew or greek
		types = type.split(":", 1)
		if types[0] not in ("robinson", "Greek"):
			tooltipdata = _("Don't know how to open this morphology type:")
			tooltipdata += "<br>%s" % type
		else:
			value = url.getParameterValue("value") #strongs number
			module = biblemgr.get_module("Robinson")
			if not value:
				return
			
			if not module:
				tooltipdata = _("Module %s is not installed, so you "
				"cannot view details for this morphological code") % type
			else:
				tooltipdata = dictionary.GetReferenceFromMod(module, value)

		return text_config(tooltipdata, module)


	elif(action=="showNote"):
		type = url.getParameterValue("type") #x or n
		value = url.getParameterValue("value") #number footnote in verse
		if((not type) or (not value)): 
			dprint(WARNING, "Not type or value in showNote", href)
			return
		module = biblemgr.get_module(url.getParameterValue("module"))
		passage = url.getParameterValue("passage")
		if not passage or not module:
			return

		if type == "n":
			data = bible.GetFootnoteData(module, passage, value, "body")
			data = data or ""
			return text_config(data, module)


		elif type == "x":
			#make this plain
			template = VerseTemplate(
			header="<a href='nbible:$internal_range'><b>$range</b></a><br>",
			body=u'<glink href="nbible:$internal_reference">'
				u'<small><sup>$versenumber</sup></small></glink> $text ')
			try:
				#no footnotes
				if tooltip_settings["plain_xrefs"]:
					biblemgr.temporary_state(biblemgr.plainstate)
				
				#apply template
				biblemgr.bible.templatelist.append(template)

				#find reference list
				reflist = bible.GetFootnoteData(module, passage, value, "refList")
				#it seems note may be as following - 
				#ESV: John.3.1.xref_i "See Luke 24:20"
				#treat as footnote then. not sure if this is intended behaviour
				#could lead to weird things
				data = ""
				if(not reflist):
					data = bible.GetFootnoteData(module, passage, value, "body")
				else:
					reflist = reflist.split("; ")
					#get refs
					verselist = bible.GetReferencesFromMod(module, reflist)
					data += '<hr>'.join(
						process_html_for_module(module, ref)
						for ref in verselist
					)

				return text_config(data, module)

			finally:
				#put it back how it was
				if tooltip_settings["plain_xrefs"]:
					biblemgr.restore_state()
				biblemgr.bible.templatelist.pop()


	elif action=="showRef":
		type = url.getParameterValue("type") 
		if type != "scripRef":
			dprint(WARNING, "unknown type for showRef", type, href)
			return
		value = url.getParameterValue("value") #passage
		module = biblemgr.get_module(url.getParameterValue("module"))
		if not module:
			module = biblemgr.bible.mod

		if not value:
			return

		tooltip_config.mod = module
		
		#make this plain
		#template = VerseTemplate(header = "$range<br>", 
		#body = '<font color = "blue"><small><sup>$versenumber</sup></small></font> $text')
		template = VerseTemplate(
			header="<a href='bible:$internal_range'><b>$range</b></a><br>", 
			body=u'<glink href="nbible:$internal_reference">'
				u'<small><sup>$versenumber</sup></small></glink> $text ')

		try:
			if tooltip_settings["plain_xrefs"]: 
				#no footnotes
				biblemgr.temporary_state(biblemgr.plainstate)
				#apply template
			biblemgr.bible.templatelist.append(template)

			value = value.split("; ")
			
			context = frame.reference
			
			# Gen books have references that are really tree keys...
			if not isinstance(context, basestring):
				context = "%s" % context

			
			#get refs
			refs = bible.GetReferencesFromMod(module, value, 
				context=context)

			data = '<hr>'.join(
				process_html_for_module(module, ref)
				for ref in refs
			)

			#set tooltip text
			return text_config(data)

		finally:
			#put it back how it was
			if tooltip_settings["plain_xrefs"]:
				biblemgr.restore_state()
			biblemgr.bible.templatelist.pop()

	dprint(WARNING, "Unknown action", action, href)

def on_hover(frame, href, url, x, y):
	tooltip_config = on_hover_get_config(frame, href, url)
	if not tooltip_config: return
	show_tooltip(frame, tooltip_config)

hover = protocol_handler.register_hover
hover("bible", on_hover_bible)
hover("nbible", lambda *args, **kwargs:None)
hover("", on_hover)
click = protocol_handler.register_handler

def on_link_clicked_bible(frame, href, url):
	host = url.getHostName()
	
	# if we are a list of links, we don't care about being clicked on
	if not host: 
		return

	guiconfig.mainfrm.set_bible_ref(host, LINK_CLICKED)

def on_link_clicked(frame, href, url):
	host = url.getHostName()
	if host != "passagestudy.jsp":
		return
	action = url.getParameterValue("action")
	if action == "showStrongs":
		type = url.getParameterValue("type") #Hebrew or greek
		value = url.getParameterValue("value") #strongs number
		if not type or not value: 
			return
		#do lookup
		type = "Strongs"+type #as module is StrongsHebrew or StrongsGreek
		if biblemgr.dictionary.ModuleExists(type):
			guiconfig.mainfrm.set_module(type, biblemgr.dictionary)
			wx.CallAfter(guiconfig.mainfrm.UpdateDictionaryUI, value)
		return
	if action=="showMorph":
		type = url.getParameterValue("type") #Hebrew or greek
		value = url.getParameterValue("value") #strongs number
		if not type or not value: 
			return
		
		if type.split(":")[0] not in ("robinson", "Greek"):
			return

		#do lookup
		type = "Robinson"
		if biblemgr.dictionary.ModuleExists(type):
			guiconfig.mainfrm.set_module(type, biblemgr.dictionary)
			wx.CallAfter(guiconfig.mainfrm.UpdateDictionaryUI, value)


click("bible", on_link_clicked_bible)
click("nbible", on_link_clicked_bible)

click("", on_link_clicked)

def on_strongs_hover(frame, href, url, x, y):
	dictionary = biblemgr.dictionary		
	type = url.getHostName() #Hebrew or greek
	value = url.getPath() #strongs number
	if not type or not value: 
		print "Not type or value", href
		return

	show_tooltip(frame, StrongsTooltipConfig(type, value))

hover("strongs", on_strongs_hover)
