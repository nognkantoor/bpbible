# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is the XPCOM Python/Javascript Proxy.
#
# The Initial Developer of the Original Code is
# Rasjid Wilcox.
# Portions created by the Initial Developer are Copyright (C) 2009
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Rasjid Wilcox <rasjidw@openminddev.net> (original author)
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from xpcom import components as Components
import types
import time
# JMM change
#import simplejson as json
from exceptions import Exception

class JSError(Exception):
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        ##for name, value in kwargs:
            ##setattr(self, name, value)
    def __str__(self):
        output = 'JSError:\n'
        for name, value in sorted(self._kwargs):
            output += '  %s: %s\n' % (str(name), str(value))
        return output.strip()

class MethodProxy(object):
    def __init__(self, jsproxy, method_name):
        self.jsproxy = jsproxy
        self.method_name = method_name
    def __call__(self, *args):
        self.jsproxy.addargs(*args)
        self.jsproxy._proxy.callMethod(self.method_name)
        return self.jsproxy.getresult()
class JSProxy(object):
    def __init__(self, xpcom_object):
        ##print 'Creating JSProxy on %s' % str(xpcom_object)
        proxy = Components.classes["@rasjidw.openminddev.net/jsproxy;1"].createInstance(Components.interfaces.nsIJSProxy)
        self._proxy = proxy
        proxy.xpcomObject = xpcom_object
        props, methods = proxy.getPropsMethods().split('|')
        self._properties = sorted(props.split(','))
        self._methods = sorted(methods.split(','))
        self._register = {}
        ##print 'Properties: ', props
        ##print 'Methods: ', methods
    def addargs(self, *args):
        self._proxy.clearArgs()
        for arg in args:
            if arg is None:
                self._proxy.addNullArg()
            elif type(arg) == types.BooleanType:
                self._proxy.addBooleanArg(arg)
            elif type(arg) in types.StringTypes:
                self._proxy.addStringArg(arg)
            elif type(arg) in (types.IntType, types.LongType):
                self._proxy.addIntArg(str(arg))
            elif type(arg) == types.FloatType:
                self._proxy.addDoubleArg(arg)
            else:
                # JMM change.
                self._proxy.addXPCOMArg(arg)
                """
                try:
                    jsonarg = json.dumps(arg)
                    self._proxy.addJSONArg(arg)
                except TypeError:
                    # try passing as XPCOM object
                    self._proxy.addXPCOMArg(arg)
               """
    def getresult(self):
        return_type = self._proxy.getResultType()
        ##print 'Got return type', return_type
        ##print 'Result as string: ', self._proxy.getResult()
        if return_type == 'null':
            return None
        elif return_type == 'boolean':
            convert = {'true': True, 'false': False}
            result = self._proxy.getResult()
            try:
                return convert[result]
            except KeyError:
                raise JSError(name = 'TypeError', message="'%s' is not a valid boolean response" % result)
        elif return_type == 'string':
            return self._proxy.getResult()
        elif return_type == 'number':
            text = self._proxy.getResult()
            # FIXME: special cases for +-infinity?
            try:
                return int(text)
            except ValueError:
                return float(text)
        elif return_type == 'object':
            # JMM change.
            jsonobj = None
            """
            try:
                jsonobj = json.loads(self._proxy.getResult())
            except ValueError:
                jsonobj = None
            """
            # FIXME: error checking here?
            xpcomobj = self._proxy.getXPCOMResult()
            if len(xpcomobj._interfaces_) <= 1 and jsonobj:
                # if the json object is 
                return jsonobj
            else:
                return xpcomobj
        elif return_type == 'error':
            # JMM change.
            #jserror = json.loads(self._proxy.getResult())
            #raise JSError(**jserror.__dict__)
            raise JSError(jsonobj=self._proxy.getResult())
    def __getattr__(self, name):
        #print 'getattr: ', name
        if name in self._methods:
            return MethodProxy(self, name)
        elif name in self._properties:
            self._proxy.getProperty(name)
            return self.getresult()
        #print '** missing attribute ', name
		# JMM change.
        raise AttributeError("JSProxy object has no attribute '%s'" % name)
    def __setattr__(self, name, value):
        #print 'setattr:', name, value
        if name[0] != '_' and name in self._properties:
            self.addargs(value)
            self._proxy.setProperty(name)
        else:
            object.__setattr__(self, name, value)
    def register(self, xpcomobject):
        register_id = str(id(xpcomobject))
        self._register[register_id] = xpcomobject
        self._proxy.registerXPCOMObject(register_id, xpcomobject)
    def unregister(self, xpcomobject):
        register_id = str(id(xpcomobject))
        self._register.pop(register_id)
        self._properties.unregisterXPCOMObject(register_id)
        
    
