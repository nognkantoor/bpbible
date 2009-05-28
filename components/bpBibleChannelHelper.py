import xpcom
from backend.bibleinterface import biblemgr
from swlib.pysw import SW
import os
import config

class bpBibleChannelHelper:
	_com_interfaces_ = xpcom.components.interfaces.bpBibleChannelHelper
	_reg_clsid_ = "b79e8f5b-5aee-47e2-b831-d3a2f7609549"
	_reg_contractid_ = "@bpbible.com/bpBibleChannelHelper;1"

	def getDocument( self, param0 ):
		import time
		t = time.time()

		# Result: wstring
		# In: param0: wstring
		print "PARAM0", param0, 
		
		ref = SW.URL.decode(param0).c_str()[1:]
		assert "!" not in ref

		print `ref`
		if not ref: return "<html><body>Content not loaded</body></html>"
		print "Ref contains '!'?", "!" in ref
		print ref

		stylesheets = ["bpbible_html.css"]
		scripts = ["jquery-1.3.2.js", "highlight.js", "bpbible_html.js"]
		

		c = biblemgr.bible.GetChapter(ref, ref, config.current_verse_template)
		c = c.replace("<!P>", "</p><p>")

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

		text = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	%s
	%s
	<script type="application/x-python">
from mozutils import doAlert, doQuit
doAlert("Security Violated!!! Aborting.")
doQuit(True)
</script>
            	
</head>
<body dir="%s">
	<div id="content">
	<!-- <p> -->
	%s
	<!-- </p> -->
	%s
	</div>
</body></html>''' % ('\n'.join(resources), f, dir, c, 
	"<div class='timer'>Time taken: %.3f</div>" % (time.time() - t))
		
		try:
			open("tmp.html", "w").write(text)
		except Exception, e:
			print "Error writing", e
		return text
		return u"test. And param0 was %s" % param0
