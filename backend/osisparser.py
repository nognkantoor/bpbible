from backend import filterutils
from swlib.pysw import SW, GetBestRange
from util.debug import dprint, WARNING
import os.path

class OSISParser(filterutils.ParserBase):
	def __init__(self, *args, **kwargs):
		super(OSISParser, self).__init__(*args, **kwargs)
		self.did_xref = False
		
		self.strongs_bufs = []
		self.morph_bufs = []
		self.was_sword_ref = False
		self.in_indent = False
		self.in_morph_seg = False
		self._end_hi = ""
	
	def start_hi(self, xmltag):
		assert not xmltag.isEmpty(), "Hi cannot be empty"
		type = xmltag.getAttribute("type")
		types = {
			"bold": ("<b>", "</b>"),
			"italic": ("<i>", "</i>"),
			"sub": ("<sub>", "</sub>"),
			"sup": ("<sup>", "</sup>"),
			"underline": ("<u>", "</u>"),
			"small-caps": ('<span class="small-caps">', "</span>"),
		}
		if type not in types:
			dprint(WARNING, "Unhandled hi type", type)
			type = "italic"
		
		start, end = types[type]
		self.buf += start
		self._end_hi = end
	
	def end_hi(self, xmltag):
		self.buf += self._end_hi
		
	def start_reference(self, xmltag):
		self.ref = xmltag.getAttribute("osisRef")
		if not self.ref:
			self.ref = None
			self.success = SW.INHERITED
			dprint(WARNING, "No osisRef in reference", xmltag.toString())
			
			return
			

		#TODO check this
		#TODO check for Bible:Gen.3.5
		idx = self.ref.find(":")
		self.was_sword_ref = False
		
		if idx != -1:
			if not self.ref[:idx].startswith("Bible"):
				self.ref = "sword://%s/%s" % (
					self.ref[:idx], SW.URL.encode(self.ref[idx+1:]).c_str()
				)
				self.was_sword_ref = True
			else:
				self.ref = self.ref[idx+1:]

		self.u.suspendLevel += 1
		self.u.suspendTextPassThru = self.u.suspendLevel
	
	def end_reference(self, xmltag):
		if self.ref is None:
			self.success = SW.INHERITED
			return

		self.u.suspendLevel -= 1
		self.u.suspendTextPassThru = self.u.suspendLevel

		if self.was_sword_ref:
			self.buf += '<a href="%s">%s</a>' % (
				self.ref, self.u.lastTextNode.c_str()
			)
		else:			
			ref = GetBestRange(self.ref, abbrev=True, use_bpbible_locale=True)
			self.buf += '<a href="bible:%s">%s</a>' % (
				ref, self.u.lastTextNode.c_str()
			)
			
	def start_lb(self, xmltag):
		type = xmltag.getAttribute("type")
		if not xmltag.isEmpty():
			print "Can lb's really be non-empty?"
		if type == "x-end-paragraph":
			self.buf += "</p>"
		elif type == "x-begin-paragraph":
			self.buf += "<p>"

	def start_w(self, xmltag):
		self.strongs_bufs = []
		self.was_G3588 = None
		# w lemma="strong:H03050" wn="008"
	
		lemmas = xmltag.getAttribute("lemma")
		if (not lemmas or self.u.suspendTextPassThru):
			#not	filterutils.filter_settings["strongs_headwords"]):
			self.success = SW.INHERITED		
			return

		# TODO: gloss, xlit?, POS?

		for lemma in lemmas.split(" "):
		
			if (not lemma.startswith("strong:") and 
				not lemma.startswith("x-Strongs:") and
				not lemma.startswith("Strong:")):
				dprint(WARNING, "Could not match lemma", lemma)
				#self.success = SW.INHERITED
				continue
				
				#return
			
			strongs = lemma[lemma.index(":")+1:]
			if self.was_G3588 is None and strongs == "G3588":
				self.was_G3588 = True
			else:
				self.was_G3588 = False
		
			headword = self.get_strongs_headword(strongs)
			if not headword:
				self.success = SW.INHERITED
				return
			
			self.strongs_bufs.append(headword)
			
		self.morph_bufs = []
		morph = xmltag.getAttribute("morph")
		if morph:
			for attrib in morph.split():
				val = attrib.find(":")
				if val == -1:
					val = attrib
				else:
					val = attrib[val+1:]
				val2 = val
				if val[0] == 'T' and val[1] in "GH" and val[2] in "0123456789":
					val2 = val2[2:]
				if not self.u.suspendTextPassThru:
					self.morph_bufs.append("<a class=\"morph\" href=\"morph://%s/%s\">(%s)</a>"%(
							SW.URL.encode(morph).c_str(),
							SW.URL.encode(val).c_str(),
							val2))
		
		if self.strongs_bufs:
			self.u.suspendLevel += 1
			self.u.suspendTextPassThru = self.u.suspendLevel
			
	
	def end_w(self, xmltag):
		if self.strongs_bufs:
			self.u.suspendLevel -= 1
			self.u.suspendTextPassThru = self.u.suspendLevel
	
		if self.was_G3588 and not self.u.lastSuspendSegment.size():
			# and not self.morph_bufs:
			# don't show empty 3588 tags
			return
			
		if self.strongs_bufs:
			self.buf += '<span class="strongs-block"><span class="strongs_word">'
			self.buf += self.u.lastSuspendSegment.c_str() or "&nbsp;"
			self.buf += '</span><span class="strongs"><span class="strongs_headwords">'
			self.buf += "".join(self.strongs_bufs)
			if self.morph_bufs:
				self.buf += '</span><span class="strongs_morph">'
				self.buf += "".join(self.morph_bufs)

			self.buf += "</span></span></span>"
			return

		self.success = SW.INHERITED
		
	def start_note(self, xmltag):
		self.did_xref = False
		
	
		type = xmltag.getAttribute("type")
		footnoteNumber = xmltag.getAttribute("swordFootnote")
		if not type:
			print "Not type - module bug", xmltag.toString()
			type = "missing"
		if not type or not footnoteNumber:
			if type != "x-strongsMarkup":
				print "FAILED", xmltag.toString()
			self.success = SW.INHERITED
			return
		
		was_xref = type in ("crossReference", "x-cross-ref")
		
		footnote_type = "n"		
		if was_xref:
			footnote_type = "x"

		do_xref = filterutils.filter_settings["footnote_ellipsis_level"]
		footnotes = SW.Buf("Footnote")
		refList = SW.Buf("refList")
		n = SW.Buf("n")
		number = SW.Buf(footnoteNumber)
		#if not do_xref:
		#	self.success = SW.INHERITED

		map = self.u.module.getEntryAttributesMap()
		footnote = map[footnotes][number]
		if n in footnote:
			footnote_char = footnote[n].c_str()
		else:
			if was_xref: footnote_char = "x"
			else: footnote_char = "n"

		if do_xref:
			try:			
				refs = footnote[refList].c_str()
			
			except IndexError:
				dprint(WARNING, "Error getting Footnote '%s' refList" % 
					footnoteNumber)
				self.success = SW.INHERITED
				return

			if not refs:
				# if there weren't any references, just do the usual
				self.success = SW.INHERITED
				return
			

			self.u.inXRefNote = True
			
			self.buf += filterutils.ellipsize(
				refs.split(";"), 
				self.u.key.getText(),
				int(filterutils.filter_settings["footnote_ellipsis_level"])
			)
		else:
			c = "footnote footnote_%s" % type
			self.buf += "<a class=\"%s\" href=\"passagestudy.jsp?action=showNote&type=%c&value=%s&module=%s&passage=%s\">%s</a>" % (
								c,
								footnote_type,
								SW.URL.encode(footnoteNumber).c_str(), 
								SW.URL.encode(self.u.version.c_str()).c_str(), 
								SW.URL.encode(self.u.key.getText()).c_str(), 
								footnote_char
			)
		self.did_xref = True
		self.u.suspendLevel += 1
		self.u.suspendTextPassThru = self.u.suspendLevel
		
			
		

	def end_note(self, xmltag):
		if self.did_xref:
			self.u.inXRefNote = False
			self.u.suspendLevel -= 1
			self.u.suspendTextPassThru = self.u.suspendLevel
			self.did_xref = False
			
			return
		
			

		self.success = SW.INHERITED	
	
	def start_milestone(self, xmltag):
		if not xmltag.isEmpty():
			print "Can milestone's really be non-empty?"
	
		if xmltag.getAttribute("type") == "x-p":
			# m = attributes["marker"] (Pilcrow character in KJV)
			self.buf += "<!P>"
		else:
			self.success = SW.INHERITED	

		
	# TODO:
	# lg starting in previous chapter
	# verse numbers on x-indent lines
	# verse numbers (and footnotes) float lefter? (hard)
	# version comparison problems - kill these!

	def start_title(self, xmltag):
		canonical = xmltag.getAttribute("canonical")
		canonical = canonical or "false"
		self.buf += '<h6 class="heading" canonical="%s">' % canonical
	
	def end_title(self, xmltag):
		self.buf += '</h6>'

	def start_lg(self, xmltag):
		if xmltag.getAttribute("eID"):
			return self.end_lg(xmltag)

		self.buf += '<blockquote class="lg" width="0">'
	
	def end_lg(self, xmltag):
		self.buf += '</blockquote>'
	
	def write(self, text):
		if self.u.suspendTextPassThru:
			self.u.lastSuspendSegment.append(text)
		else:
			self.buf += text

	def start_divineName(self, xmltag):
		self.write("<span class='divineName'>")

	def end_divineName(self, xmltag):
		self.write("</span>")
	
		
	def start_l(self, xmltag):
		if xmltag.getAttribute("eID"):
			return self.end_l(xmltag)

		if xmltag.isEmpty() and not xmltag.getAttribute("sID"):
			print "<l />?!?", xmltag.toString()
			self.success = SW.INHERITED
			return
		
		mapping = {
			# usual poetry indent in ESV
			"x-indent": 2,

			# extra indent - 1 Tim 3:16 (ESV) for example
			"x-indent-2": 4,

			# declares lines - Declares the Lord, Says the Lord, etc.
			"x-declares": 6,
			
			# doxology - Amen and Amen - Psalms 41:13, 72:19, 89:52 in ESV 
			"x-psalm-doxology": 6,

			# usual poetry indent in WEB
			"x-secondary": 2,
		}

		level = xmltag.getAttribute("level")
		if level:
			# the level defaults to 1 - i.e. no indent
			indent = 2 * (int(level) - 1)
		else:
			indent = mapping.get(xmltag.getAttribute("type"), 0)

		#if indent:
		if self.in_indent:
			dprint(WARNING, "Nested indented l's", self.u.key.getText())

		self.in_indent = True
		self.buf += '<div class="indentedline" width="%d" source="l">' % indent
		#else:
		#	self.success = SW.INHERITED

	def end_l(self, xmltag):
		if self.in_indent:
			self.buf += "</div>"
			self.in_indent = False
			
		else:
			self.success = SW.INHERITED
	
	def start_figure(self, xmltag):
		src = xmltag.getAttribute("src")
		if not src:
			self.success = SW.FAILED
			return

		data_path = self.u.module.getConfigEntry("AbsoluteDataPath")
		img_path = os.path.realpath("%s/%s" % (data_path, src))
		self.buf += '<img border=0 src="%s" />' % img_path
			
	def start_seg(self, xmltag):
		type = xmltag.getAttribute("type")
		if type in ("morph", "x-morph"):
			self.buf += '<span class="morphSegmentation">'
			if self.in_morph_seg:
				dprint(WARNING, "Nested morph segs", self.u.key.getText())

			self.in_morph_seg = True
		else:
			self.success = SW.INHERITED

	
	def end_seg(self, xmltag):
		if self.in_morph_seg:
			self.buf += "</span>"
			self.in_morph_seg = False
			
		else:
			self.success = SW.INHERITED

	def start_harmonytable(self, xmltag):
		from backend.bibleinterface import biblemgr
		references = xmltag.getAttribute('refs').split("|")
		if not references:
			return

		header_row = u"<tr>%s</tr>" % (
			u"".join(
				u"<th>%s</th>" % GetBestRange(reference, userOutput=True)
				for reference in references
			))
		body_row = u"<tr>%s</tr>" % (
			u"".join(
				u"<td>%s</td>" % biblemgr.bible.GetReference(reference)
				for reference in references
			))
		table = u'<table class="harmonytable">%s%s</table>' % (header_row, body_row)
		self.buf += table.encode("utf8")

	def end_harmonytable(self, xmltag):
		# Prevent SWORD choking on this.
		pass
		
class OSISRenderer(SW.RenderCallback):
	def __init__(self):
		super(OSISRenderer, self).__init__()
		self.thisown = False

	@filterutils.return_success
	@filterutils.report_errors
	@filterutils.OSISUserData
	def run(self, buf, token, u):
		if not filterutils.filter_settings["use_osis_parser"]: 
			return "", SW.INHERITED
	
		# w lemma="strong:H03050" wn="008"		
		p.process(token, u)
		return p.buf, p.success

	def set_biblemgr(self, biblemgr):
		p.set_biblemgr(biblemgr)

p = OSISParser()

