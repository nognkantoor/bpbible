/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 * 
 * The contents of this file are subject to the Mozilla Public License
 * Version 1.1 (the "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 * 
 * Software distributed under the License is distributed on an "AS IS"
 * basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
 * License for the specific language governing rights and limitations
 * under the License.
 * 
 * The Original Code is pythonext code.
 * 
 * The Initial Developer of the Original Code is Todd Whiteman.
 * Portions created by the Initial Developer are Copyright (C) 2000-2008
 * the Initial Developer. All Rights Reserved.
 * 
 * Contributor(s):
 *   Todd Whiteman <twhitema@gmail.com> (original author)
 * 
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 * 
 * ***** END LICENSE BLOCK ***** */

Components.utils.import("resource://gre/modules/XPCOMUtils.jsm");
const nsIProtocolHandler = Components.interfaces.nsIProtocolHandler;

// The SFTP Protocol XPCOM class.
function BPBibleProtocol() { }

BPBibleProtocol.prototype = {
	classDescription: "BPBibleProtocol XPCOM Component",
	classID:		  Components.ID("{1f7c9272-17f8-40b2-836e-de1aa1e450b6}"),
	contractID:	   "@mozilla.org/network/protocol;1?name=bpbible",
	QueryInterface: XPCOMUtils.generateQI([nsIProtocolHandler]),

	// Example URI:  "bpbible://myhost/my/path/file.txt"

	scheme: "bpbible",
	protocolFlags : nsIProtocolHandler.URI_NOAUTH |
				nsIProtocolHandler.URI_IS_UI_RESOURCE,//LOADABLE_BY_ANYONE,

	newURI: function(aSpec, aOriginCharset, aBaseURI) {
		url = Components.classes["@mozilla.org/network/standard-url;1"].
				 createInstance(Components.interfaces.nsIStandardURL);
		url.init(Components.interfaces.nsIStandardURL.URLTYPE_STANDARD,
				 80, aSpec, aOriginCharset, aBaseURI);
		return url.QueryInterface(Components.interfaces.nsIURI);
	},
	
	newChannel: function(aURI) {
		var channel = new BPBibleChannel();
		channel.URI = aURI;
		channel.originalURI = aURI;
		return channel;
	},

	allowPort: function(port, scheme) {
		return false;
	}
};

function BPBibleChannel() {
	this.logMessage("Creating Channel");
	this._bpb = Components.classes
				["@bpbible.com/bpBibleChannelHelper;1"]
				.createInstance(Components.interfaces.bpBibleChannelHelper);
	

}

BPBibleChannel.prototype = {
	classDescription: "BPBible XPCOM Component",
	classID:		  Components.ID("{22c2f5a4-56fc-42f4-9bdd-59b143c8a482}"),
	contractID:	   "@pythonext.mozdev.org/SSHChannel;1",
	QueryInterface: XPCOMUtils.generateQI([Components.interfaces.nsIRequest,
										   Components.interfaces.nsIChannel,
	]),

	/* internal */

	_async_type: null,
	_command: null,
	_termType: null,
	_convertStream: null,
	_ssh: null,
	_bpb: null,
	_authSvc: null,
	listener: null,
	context: null,

	logMessage: function(message) {
		var consoleSvc = Components.classes["@mozilla.org/consoleservice;1"].
						   getService(Components.interfaces.nsIConsoleService);
		consoleSvc.logStringMessage(message)
	},
	
	logException: function(message, ex) {
		var consoleSvc = Components.classes["@mozilla.org/consoleservice;1"].
						   getService(Components.interfaces.nsIConsoleService);
		consoleSvc.logStringMessage(message + ": " + ex);
		Components.utils.reportError(ex);
	},

	/* nsIRequest */

	name: "BPBible Channel",
	loadGroup: null,
	loadFlags: 0,
	status: 0,

	isPending: function() {
		return this._isPending;
	},

	cancel: function(status) {
		self.status = status;
	},

	suspend: function() {
		throw Components.results.NS_ERROR_NOT_IMPLEMENTED;
	},

	resume: function() {
		throw Components.results.NS_ERROR_NOT_IMPLEMENTED;
	},

	/* nsIChannel */

	originalURI: "",
	URI: "",
	contentLength: -1,
	contentType: "text/html",
	contentCharset: "UTF-8",
	owner: null,
	notificationCallbacks: null,
	progressCallback: null,
	securityInfo: null,

	open: function() {
		throw Components.results.NS_ERROR_NOT_IMPLEMENTED;
	},

	asyncOpen: function(aListener, aContext) {
		this._isPending = true;
		
		try {
			if (this.loadGroup) {
				this.loadGroup.addRequest(this, null);
			}
			
			this.logMessage("Requesting path: " + this.URI.path);

			var html = this._bpb.getDocument(this.URI.path);//this.getHTML();
			aListener.onStartRequest(this, aContext);
			var converter = Components.classes["@mozilla.org/intl/scriptableunicodeconverter"]
							.createInstance(Components.interfaces.nsIScriptableUnicodeConverter);
			converter.charset = "UTF-8";
			var bst = converter.convertToInputStream(html);
			var len = bst.available();			
			aListener.onDataAvailable(this, aContext, bst, 0, len);						
			//bst.close();
			aListener.onStopRequest(this, aContext, Components.results.NS_OK);
			if (this.loadGroup) {
				this.loadGroup.removeRequest (this, null, Components.results.NS_OK);
			}
			this._isPending = false;
					
		} catch (e) {
			// TODO TODO TODO:
			this.logException("error in asyncOpen", e);
		}
	
	},

};

// XPCOM registration.
var components = [BPBibleProtocol];
function NSGetModule(compMgr, fileSpec) {
	return XPCOMUtils.generateModule(components);
}

