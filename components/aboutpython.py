from xpcom import components, verbose

class AboutPython:
	_com_interfaces_ = components.interfaces.nsIAboutModule

	def newChannel(self, aURI):
		ioService = components.classes["@mozilla.org/network/io-service;1"] \
			   .getService(components.interfaces.nsIIOService);
		uri = ioService.newURI(self.file, "utf-8", aURI)
		return ioService.newChannelFromURI(uri)

	def getURIFlags(self, aURI):
		AM = components.interfaces.nsIAboutModule
		return AM.URI_SAFE_FOR_UNTRUSTED_CONTENT | AM.ALLOW_SCRIPT

class AboutPythonCSS(AboutPython):
	### TODO: OK, OK, this is a nasty hack - but it gets the CSS working
	### nicely :)
	_reg_contractid_ = '@mozilla.org/network/protocol/about;1?what=bpcss'
	_reg_clsid_ = '{6d5d462e-6de7-4bca-bbc6-c488d481351b}'
	_reg_desc_ = "BPBible CSS server"
	file = "chrome://bpbible/skin/bpbible_html.css"

class AboutPythonJS(AboutPython):
	### TODO: OK, OK, this is a nasty hack - but it gets the CSS working
	### nicely :)
	_reg_contractid_ = '@mozilla.org/network/protocol/about;1?what=bpjs'
	_reg_clsid_ = '{60fd5915-65ca-435b-a8c5-17c727308c33}'
	_reg_desc_ = "BPBible JS server"
	file = "chrome://bpbible/content/bpbible_html.js"

class AboutPythonJQuery(AboutPython):
	### TODO: OK, OK, this is a nasty hack - but it gets the CSS working
	### nicely :)
	_reg_contractid_ = '@mozilla.org/network/protocol/about;1?what=bpjq'
	_reg_clsid_ = '{01b8a6fc-b2f4-405b-81be-1db94e8aaf12}'
	_reg_desc_ = "BPBible JQuery server"
	file = "chrome://bpbible/content/jquery-1.3.2.js"
