import xpcom
from backend.bibleinterface import biblemgr
from swlib.pysw import SW
import os
import config
from util.debug import dprint, ERROR
from display_options import all_options, get_js_option_value

class bpBibleChannelHelper:
	_com_interfaces_ = xpcom.components.interfaces.bpBibleChannelHelper
	_reg_clsid_ = "b79e8f5b-5aee-47e2-b831-d3a2f7609549"
	_reg_contractid_ = "@bpbible.com/bpBibleChannelHelper;1"

	def getDocument( self, module_name, param0 ):
		import time
		t = time.time()

		# Result: wstring
		# In: param0: wstring
		print "PARAM0", param0, 
		dprint(ERROR, "PARAM0", param0, "MODULE_NAME", module_name)
		
		ref = SW.URL.decode(param0).c_str()[1:]
		assert "!" not in ref

		print `ref`
		if not ref: return "<html><body>Content not loaded</body></html>"
		print "Ref contains '!'?", "!" in ref
		print ref

		stylesheets = ["bpbible_html.css"]
		scripts = ["jquery-1.3.2.js", "highlight.js", "bpbible_html.js",
				  "hyphenate.js", "columns.js"]
		

		book = biblemgr.get_module_book_wrapper(module_name)
		if book:
			c = book.GetChapter(ref, ref, config.current_verse_template)
			c = c.replace("<!P>", "</p><p>")
		else:
			dprint(ERROR, "Book `%s' not found." % module_name)
			c = ''

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

		f = ""
		firebug = False
		if firebug:
			f = """
			<script type='text/javascript' 
				src='chrome://firebuglite/content/firebug-lite.js'></script>
			<script type="text/javascript">
			firebug.env.css = "chrome://firebuglite/content/firebug-lite.css";
			</script>"""
	

		dir = {
			SW.DIRECTION_BIDI: "bidi",
			SW.DIRECTION_LTR:  "ltr",
			SW.DIRECTION_RTL:  "rtl",
		}.get(ord(biblemgr.bible.mod.Direction()))
		if not dir: 
			print "Unknown text direction"
			dir = "ltr"
		
		lang = biblemgr.bible.mod.Lang()
		
		options = []
		for option in all_options():
			options.append('%s="%s"' % (option, get_js_option_value(option)))

		text = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="%s">
<head>
	%s
	%s
	<script type="application/x-python">
from mozutils import doAlert, doQuit
doAlert("Security Violated!!! Aborting.")
doQuit(True)
</script>
            	
</head>
<body dir="%s" %s>
	<div id="content">
	<!-- <p> -->
	%s
	<!-- </p> -->
	</div>
	%s
</body></html>''' % (lang, '\n'.join(resources), f, dir, ' '.join(options), c, 
	"<div class='timer'>Time taken: %.3f</div>" % (time.time() - t))
		
		try:
			open("tmp.html", "w").write(text)
		except Exception, e:
			print "Error writing", e
		return text
		return u"test. And param0 was %s" % param0
