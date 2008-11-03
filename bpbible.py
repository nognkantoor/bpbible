#!/usr/bin/env python

from util.debug import dprint, MESSAGE, WARNING, is_debugging
dprint(MESSAGE, "Importing wx")

import wx
dprint(MESSAGE, "importing wx.xrc")

dprint(MESSAGE, "/importing wx")

# make sure contribs can be imported...
import contrib

import config, guiconfig
from util import osutils
from util.configmgr import config_manager

import util.i18n
import gui.i18n


#from search import mySearchPanel

class MyApp(wx.App):
	def Initialize(self):
		# for py2exe
		import mainframe
		
		was_restarted = self.restarting
		self.starting = self.restarting = False
		config_manager.load()
		util.i18n.initialize()
		gui.i18n.initialize()
		
		frame = self.res.LoadFrame(None,  "MainFrame" )
		if(frame == None):
			wx.MessageBox("Could not load MainFrame from auifrm.xrc", \
				"Fatal Error", style = wx.ICON_ERROR)
			return False


		frame.SetIcons(guiconfig.icons)
		#frame.SetIcon(icon_bundle.GetIcon((32,32)))

		self.SetTopWindow(frame)
		frame.Show(False)
		if was_restarted:
			frame.Raise()
		
	
	def OnInit(self):
		picture = 'splashscreen.png'
		self.bitmap = wx.BitmapFromImage(
			wx.Image(config.graphics_path + picture)
		)
		
		#from splashscreen import SplashScreen
		self.splash = wx.SplashScreen(
			self.bitmap, 
			wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_NO_TIMEOUT,
			0,
			None,
			style=wx.FRAME_NO_TASKBAR|wx.BORDER_NONE
		)
		self.splash.Show()
		self.splash.Raise()
		
		self.starting = True
		self.restarting = False
	
		dprint(MESSAGE, "App Init")
		
		wx.InitAllImageHandlers()

		icon_bundle = wx.IconBundle()
		for item in "16 32 48 64 128".split():
			path = config.graphics_path
			icon = wx.Image("%(path)sbible-%(item)sx%(item)s.png" % locals())
			if icon.IsOk():
				# on windows 2000, transparency is 1 bit, so convert it 
				# to one bit
				if osutils.is_win2000():
					icon.ConvertAlphaToMask()

				bmp = wx.BitmapFromImage(icon)
				icon_bundle.AddIcon(wx.IconFromBitmap(bmp))

		guiconfig.icons = icon_bundle
		dprint(MESSAGE, "Loaded icon")
		

		from wx import xrc
		self.res = xrc.XmlResource(config.xrc_path+"auifrm.xrc" )
		return True
	


def main():
	inspection_imported = False
	try:
		from wx.lib.mixins.inspect import InspectionMixin
		inspection_imported = True
	except ImportError, e:
		try:
			from wx.lib.mixins.inspection import InspectionMixin
			inspection_imported = True
		except ImportError, e:
			pass
			
	if inspection_imported and is_debugging():
		class InspectableApp(MyApp, InspectionMixin):
			def OnInit(self):
				return_value = super(InspectableApp, self).OnInit()
				if not return_value:
					return False
				self.Init()
				return True

		app = InspectableApp(0)
	else:
		if is_debugging():
			dprint(WARNING, "Could not load inspection")

		app = MyApp(0)
	
	dprint(MESSAGE, "App created")
	
	guiconfig.app = app
	while app.starting or app.restarting:
		app.Initialize()
		app.MainLoop()

if __name__ == '__main__':
	main()
