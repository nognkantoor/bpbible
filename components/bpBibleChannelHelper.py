import xpcom
from backend.bibleinterface import biblemgr
from swlib.pysw import SW
import config

class bpBibleChannelHelper:
	_com_interfaces_ = xpcom.components.interfaces.bpBibleChannelHelper
	_reg_clsid_ = "b79e8f5b-5aee-47e2-b831-d3a2f7609549"
	_reg_contractid_ = "@bpbible.com/bpBibleChannelHelper;1"

	def getDocument( self, param0 ):
		# Result: wstring
		# In: param0: wstring
		print param0, 
		ref = SW.URL.decode(param0).c_str()[2:]
		if ref.startswith("!"):
			return '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<link rel="stylesheet" type="text/css" href="about:bpcss"/ >
	<style>
@import URL("chrome://bpbible/skin/bpbible.css");	
	</style>
</head>
<body>
	<iframe type="content-primary" src="bpbible://ESV/%s"></iframe>
	
</body></html>''' % (ref[1:])
		

		print ref
		c = biblemgr.bible.GetChapter(ref, ref, config.current_verse_template)
		c = c.replace("<!P>", "&lt;!P&gt;")

		text = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<link rel="stylesheet" type="text/css" href="about:bpcss"/ >
	<style>
@import URL("chrome://bpbible/skin/bpbible.css");	
	</style>
</head>
<body>
	%s
</body></html>''' % (c)
		
		return text
		return u"test. And param0 was %s" % param0
