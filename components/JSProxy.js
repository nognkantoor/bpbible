/*
***** BEGIN LICENSE BLOCK *****
Version: MPL 1.1/GPL 2.0/LGPL 2.1

The contents of this file are subject to the Mozilla Public License Version
1.1 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at
http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
for the specific language governing rights and limitations under the
License.

The Original Code is the XPCOM Python/Javascript Proxy.

The Initial Developer of the Original Code is
Rasjid Wilcox.
Portions created by the Initial Developer are Copyright (C) 2009
the Initial Developer. All Rights Reserved.

Contributor(s):
  Rasjid Wilcox <rasjidw@openminddev.net> (original author)

Alternatively, the contents of this file may be used under the terms of
either the GNU General Public License Version 2 or later (the "GPL"), or
the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
in which case the provisions of the GPL or the LGPL are applicable instead
of those above. If you wish to allow use of your version of this file only
under the terms of either the GPL or the LGPL, and not to allow others to
use your version of this file under the terms of the MPL, indicate your
decision by deleting the provisions above and replace them with the notice
and other provisions required by the GPL or the LGPL. If you do not delete
the provisions above, a recipient may use your version of this file under
the terms of any one of the MPL, the GPL or the LGPL.

***** END LICENSE BLOCK *****
*/

Components.utils.import("resource://gre/modules/XPCOMUtils.jsm");

nativeJSON = Components.classes["@mozilla.org/dom/json;1"].createInstance(Components.interfaces.nsIJSON);

function JSProxy() { };

JSProxy.prototype = {
  // XPCOM stuff
  classDescription: "A Javascript XPCOM proxy to a document element",
  classID:          Components.ID("{c9023a61-1adb-11de-a23c-000c292cf949}"),
  contractID:       "@rasjidw.openminddev.net/jsproxy;1",
  QueryInterface: XPCOMUtils.generateQI([Components.interfaces.nsIJSProxy]),
  
  mArgs: [],
  mResult: null,
  mResultAsString: "",
  mResultType: "",
  mObject: null,
  mObjectRegister: {},  // register to keep objects around so they are not garbage collected too soon 
                        // useful for callbacks / event-listeners
  
  set xpcomObject(obj)          { return this.mObject = obj; },
  get xpcomObject()             { return this.mObject; },

  // get properties and methods
  getPropsMethods: function()
    { var result = {};
      result.properties = [];
      result.methods = [];
      // dump('mObject is: ' + this.mObject.toString() + '\n');
      for (prop in this.mObject) {
        try {
          attr_type = typeof(this.mObject[prop]);
        } catch(e) {
          // get an error doing typeof on window.sessionStorage
          // not sure what to do about it
          // so just 'drop' this attribute for now
          attr_type = 'error';  
          // dump('Error on typeof on ' + prop + ':\n' + e.toString() + '\n');
        };
        // dump('  attr: ' + prop + ' type: ' + attr_type + '\n');        
        if (attr_type === "function") {
          result.methods.push(prop);
        } else if (attr_type == 'error') {
          // do nothing
        } else {
          result.properties.push(prop);
        } ;
      } ;
      return result.properties.join(",") + "|" + result.methods.join(",");
      //return nativeJSON.encode(result);
  },
  
  // argument manipulation
  clearArgs: function()       { this.mArgs = []; },
  addNullArg: function()      { this.mArgs.push(null); },
  addBooleanArg: function()   { this.mArgs.push(arg); },
  addStringArg: function(arg) { this.mArgs.push(arg); },
  addIntArg: function(arg)    { this.mArgs.push(parseInt(arg)); },
  addDoubleArg: function(arg) { this.mArgs.push(arg); },
  addJSONArg: function(arg)   { this.mArgs.push(nativeJSON.decode(arg)); },
  addXPCOMArg: function(arg)  { this.mArgs.push(arg); },
  
  // object register
  registerXPCOMObject: function(obj_id, obj)
                              { this.mObjectRegister[obj_id] = obj; },
  unregisterXPCOMObject: function(obj_id)
                              { delete this.mObjectRegister[obj_id]; },
  
  
  // result type is 'null', 'boolean', 'string', 'number', 'jsonobject', 'xpcomobject' or 'error'
  _processError: function(error) {
    this.mResultType = 'error';
    this.mResult = error;
    this.mResultAsString = nativeJSON.encode(error);
  },
  
  _processResult: function(result) {
    this.mResult = result;

    try {
      this.mResultAsString = result.toString();
    } catch(e) {
      this.mResultAsString = '';
    };
    
    try {
      this.mResultType = typeof(result);
    } catch(e) {
      this._processError(e);
      return;
    };
    
    if (result == null) {
      this.mResultType = 'null'; 
      return;
    };

    if (this.mResultType == 'function') {
      // not currently implemented
      // could be done in a similar manner to the object reference stuff
      this.mResultType = 'error';
      this.mResultAsString = '{"name":"NotImplementedError", "message":"Not implemented!"}'
    } ;
    
    if (this.mResultType == 'object') {
      try {
        this.mResultAsString = nativeJSON.encode(result).toString();
      } catch(e) {
        this.mResultAsString = '';
      };
    }
  },
  
  getProperty: function(prop_name)
    { this.mResult = null;
      this.mResultType = 'null';
      try {
        result = this.mObject[prop_name]; 
      } 
      catch(e) {
        this._processError(e);
        return;
      } ;
      this._processResult(result);
    },

  // sets to arg[0]    
  setProperty: function(prop_name)
    { this.mResult = null;
      this.mResultType = 'null';
      try {
        this.mObject[prop_name] = this.mArgs[0]; 
      } 
      catch(e) {
        this._processError(e);
      } ;
    },                                
    
  callMethod: function(method_name)
    { this.mResult = null;
      this.mResultType = 'null';
      try {
        result = this.mObject[method_name].apply(this.mObject, this.mArgs); 
      } 
      catch(e) {
        this._processError(e);
        return;
      } ;
      this._processResult(result);
    },

  getResultType: function()        { return this.mResultType; },
  getResult: function()            { return this.mResultAsString; },
  getXPCOMResult: function() { return this.mResult ; }
};

var components = [JSProxy];
function NSGetModule(compMgr, fileSpec) {
  return XPCOMUtils.generateModule(components);
}

