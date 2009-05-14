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

		c = biblemgr.bible.GetChapter(ref, ref, config.current_verse_template)
		c = c.replace("<!P>", "</p><p>")
		stylesheet = '<link rel="stylesheet" type="text/css" href="chrome://bpbible/skin/bpbible_html.css"/ >'
		if "bpbibleng" in os.getcwd():
			p = os.path.expanduser("~/bpbibleng/chrome/skin/standard/bpbible_html.css")
			#s = open().read()
			#stylesheet = "<style type='text/css'>%s</style>" % s
			stylesheet += '<link rel="stylesheet" type="text/css" href="file:///%s" />' % p
			

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
	<script type="text/javascript" 
		src="chrome://bpbible/content/jquery-1.3.2.js"></script>
	<script type="text/javascript" 
		src="chrome://bpbible/content/bpbible_html.js"></script>
		
	<script type="application/x-python">
print "Security Violated!!!"
</script>
            	
</head>
<body dir="%s">
	<!-- <p> -->
	%s
	<!-- </p> -->
	%s
</body></html>''' % (stylesheet, dir, c, 
	"<div class='timer'>Time taken: %.3f</div>" % (time.time() - t))
		
		try:
			open("tmp.html", "w").write(text)
		except Exception, e:
			print "Error writing", e
		return text
		return u"test. And param0 was %s" % param0
