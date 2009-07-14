from backend.bibleinterface import biblemgr
from swlib.pysw import SW
import os
import config
from util.debug import dprint, ERROR
from display_options import all_options, get_js_option_value
from util.string_util import convert_rtf_to_html
from util.unicode import try_unicode
from util import languages

BASE_HTML = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="%(lang)s">
<head>
	%(head)s
	<script type="application/x-python">
from mozutils import doAlert, doQuit
doAlert("Security Violated!!! Aborting.")
doQuit(True)
</script>
            	
</head>
<body dir="%(dir)s" %(bodyattrs)s>
	<div id="content">
	<!-- <p> -->
	%(content)s
	<!-- </p> -->
	</div>
	%(timer)s
</body></html>'''

class ProtocolHandler(object):
	def get_content_type(self, aURI):
		return 'text/html'
	
	def get_document(self, aURI):
		return "No content specified"
	
	def _get_html(self, module, content, bodyattrs="", timer="", 
		stylesheets=[], scripts=[]):
		dir = {
			SW.DIRECTION_BIDI: "bidi",
			SW.DIRECTION_LTR:  "ltr",
			SW.DIRECTION_RTL:  "rtl",
		}.get(ord(module.Direction()))
		if not dir: 
			print "Unknown text direction"
			dir = "ltr"

		resources = []
		skin_prefixs = ["skin/standard", "skin"]
		script_prefixs = ["content", "content"]

		### for testing, the file link is easier - but the chrome link is the
		### one we should be using once it is working properly
		prefixs = ["file:///" + os.getcwd() + "/chrome"]#, "chrome://bpbible"]
		for skin_prefix, script_prefix, prefix \
				in zip(skin_prefixs, script_prefixs, prefixs):
			for item in stylesheets:
				resources.append('<link rel="stylesheet" type="text/css" href="%s/%s/%s"/ >' % (prefix, skin_prefix, item))
			for item in scripts:
				resources.append('<script type="text/javascript" src="%s/%s/%s"></script>' % (prefix, script_prefix, item))

		text = BASE_HTML % dict(
			lang=module.Lang(),
			dir=dir, 
			head='\n'.join(resources),
			bodyattrs=bodyattrs, 
			content=content, 
			timer=timer)
		
		try:
			open("tmp.html", "w").write(text.encode("utf8"))
		except Exception, e:
			print "Error writing tmp.html", e
		return text


class NullProtocolHandler(ProtocolHandler):
	def get_document(self, aURI):
		return "<html><body>Content not loaded</body></html>"

class PageProtocolHandler(ProtocolHandler):
	def get_document(self, aURI):
		import time
		t = time.time()

		page = str(aURI.path)

		ref = SW.URL.decode(page).c_str()[1:]
		assert ref, "No reference"

		module_name, ref = ref.split("/")

		stylesheets = ["bpbible_html.css"]
		scripts = ["jquery-1.3.2.js", "highlight.js", "bpbible_html.js",
				  "hyphenate.js", "columns.js"]

		book = biblemgr.get_module_book_wrapper(module_name)
		if book.is_verse_keyed:
			c = book.GetChapter(ref, ref, config.current_verse_template)
			stylesheets.append("bpbible_verse_keyed.css")
		elif book.is_dictionary:
			try:
				index = int(ref)
				ref = book.GetTopics()[index]
			except ValueError:
				pass

			c = book.GetReference(ref)
		else:
			dprint(ERROR, "Book `%s' not found." % module_name)
			c = ''
		c = c.replace("<!P>", "</p><p>")

		options = []
		for option in all_options():
			options.append('%s="%s"' % (option, get_js_option_value(option)))

		return self._get_html(
			biblemgr.bible.mod, c,
			bodyattrs=' '.join(options), 
			stylesheets=stylesheets,
			scripts=scripts,
			timer="<div class='timer'>Time taken: %.3f</div>" % (time.time() - t))
		
class ModuleInformationHandler(ProtocolHandler):
	def get_document(self, aURI):
		page = str(aURI.path)

		module_name = SW.URL.decode(page).c_str()[1:]

		book = biblemgr.get_module_book_wrapper(module_name)
		if not book:
			dprint(ERROR, "Book `%s' not found." % module_name)
			return "Error: Book `%s' not found." % module_name

		module = book.mod
		
		rows = []
		t = u"<table class='module_information'>%s</table>"
		for key, value in (
			("Name", module.Name()), 
			("Description", module.Description()),
			("Language", languages.get_language_description(module.Lang())),
			("License", module.getConfigEntry("DistributionLicense")),
			("About", module.getConfigEntry("About")), 
		):
			rows.append('''
			<tr>
				<th class="module_information_key">%s</th>
				<td class="module_information_value">%s</td>
			</tr>''' % (
				key, convert_rtf_to_html(try_unicode(value, module))
			))

		t %= ''.join(rows)

		return self._get_html(module, t, stylesheets=["book_information_window.css"])

handlers = {
	"page": PageProtocolHandler(), 
	'': NullProtocolHandler(),
	'moduleinformation': ModuleInformationHandler(),
}

