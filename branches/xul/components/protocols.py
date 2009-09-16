import xpcom
from xpcom import components
import protocol_handlers
import mozutils

class BPBibleProtocol:
	nsIProtocolHandler = components.interfaces.nsIProtocolHandler

	_reg_desc_ = "BPBibleProtocol XPCOM Component"
	_com_interfaces_ = nsIProtocolHandler
	_reg_clsid_ = "{13359272-17f8-40b2-836e-de1aa1e450b6}"
	_reg_contractid_ =   "@mozilla.org/network/protocol;1?name=bpbible"

	scheme = "bpbible"
	defaultPort = 0
	protocolFlags  = (nsIProtocolHandler.URI_NOAUTH | 
					nsIProtocolHandler.URI_NORELATIVE | 
				#// we could use URI_LOADABLE_BY_ANYONE and set
				#// contentaccessible=yes in chrome.manifest - but this lets us
				#// access file:// as well...
				nsIProtocolHandler.URI_IS_UI_RESOURCE)

	def newURI(self, aSpec, aOriginCharset, aBaseURI):
		Cc = components.classes
		Ci = components.interfaces
		url = Cc["@mozilla.org/network/standard-url;1"].\
				 createInstance(Ci.nsIStandardURL);
		url.init(Ci.nsIStandardURL.URLTYPE_STANDARD,
				 80, aSpec, aOriginCharset, aBaseURI);
		return url.QueryInterface(Ci.nsIURI);
	
	def newChannel(self, aURI):
		Cc = components.classes
		Ci = components.interfaces
		channel = Cc["@mozilla.org/network/input-stream-channel;1"].\
					createInstance(Ci.nsIInputStreamChannel)

		content_type = self.get_content_type(aURI)
		ch = channel.QueryInterface(Ci.nsIChannel)
		ch.contentType = content_type
		ch.contentCharset = "utf-8"
		channel.setURI(aURI)

		html = self.get_document(aURI)
		
		converter = Cc["@mozilla.org/intl/scriptableunicodeconverter"]\
			.createInstance(Ci.nsIScriptableUnicodeConverter)
			
		converter.charset = "UTF-8"
		bst = converter.convertToInputStream(html);
		channel.contentStream = bst
		return channel

	def allowPort(self, port, scheme):
		return False;
	
	def _breakup_url(self, aURI):
		assert aURI.host == "content" or not aURI.host, \
			"only content is supported at the moment..."

		page = str(aURI.path)[1:]
		d = page.split("/", 1)
		if len(d) == 1:
			d.append('')

		protocol, path = d
		
		assert protocol in protocol_handlers.handlers, \
			"No handler for host type %s" % protocol

		return protocol, path

	def get_content_type(self, aURI):
		protocol, path = self._breakup_url(aURI)
		return protocol_handlers.handlers[protocol].get_content_type(path)

	def get_document(self, aURI):
		protocol, path = self._breakup_url(aURI)
		return protocol_handlers.handlers[protocol].get_document(path)
