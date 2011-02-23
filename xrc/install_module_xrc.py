# This file was automatically generated by pywxrc.
# -*- coding: UTF-8 -*-

import wx
import wx.xrc as xrc

__res = None

def get_resources():
    """ This function provides access to the XML resources in this module."""
    global __res
    if __res == None:
        __init_resources()
    return __res




class xrcModuleInstallDialog(wx.Dialog):
#!XRCED:begin-block:xrcModuleInstallDialog.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcModuleInstallDialog.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreDialog()
        self.PreCreate(pre)
        get_resources().LoadOnDialog(pre, parent, "ModuleInstallDialog")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.gui_warning_panel = xrc.XRCCTRL(self, "gui_warning_panel")
        self.static_text = xrc.XRCCTRL(self, "static_text")
        self.modules_info = xrc.XRCCTRL(self, "modules_info")
        self.destination = xrc.XRCCTRL(self, "destination")
        self.wxID_OK = xrc.XRCCTRL(self, "wxID_OK")
        self.wxID_CANCEL = xrc.XRCCTRL(self, "wxID_CANCEL")





# ------------------------ Resource data ----------------------

def __init_resources():
    global __res
    __res = xrc.EmptyXmlResource()

    __res.Load('install_module.xrc')

# ----------------------- Gettext strings ---------------------

def __gettext_strings():
    # This is a dummy function that lists all the strings that are used in
    # the XRC file in the _("a string") format to be recognized by GNU
    # gettext utilities (specificaly the xgettext utility) and the
    # mki18n.py script.  For more information see:
    # http://wiki.wxpython.org/index.cgi/Internationalization 
    
    def _(str): pass
    
    _("DUMMY")
    _("Install to:")
    _("Book Installation")

