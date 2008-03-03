import sys
import sgmllib
from swlib.pysw import SW

import config
from backend import thmlparser, osisparser


# keep a list of all our items so they don't get GC'ed
items = []

bm_items = []
class MarkupInserter(SW.MarkupCallback):
	def __init__(self, biblemgr):
		super(MarkupInserter, self).__init__()
		self.thisown=False
		self.biblemgr = biblemgr

		for item in bm_items:
			item.set_biblemgr(biblemgr)
		items.append(self)
	
	def run(self, module):
		try:
			markup = self.get_filter(module)
			if markup is not None:
				module.AddRenderFilter(markup)
				return True
			return False

		except Exception, e:
			import traceback
			dprint(ERROR, "EXCEPTION: ", e)
			try:
				traceback.print_exc()
			except Exception, e2:
				dprint(ERROR, "Couldn't print exception - exception raised", e2)
	
	def get_filter(self, module):
		m = ord(module.Markup())
		markups = {SW.FMT_OSIS:osis, SW.FMT_THML:thml}
		if m in markups:
			return markups[m]
		return None
	
	def get_alternate_filter(self, module):
		m = ord(module.Markup())
		markups = {SW.FMT_OSIS:osis2, SW.FMT_THML:thml2}
		if m in markups:
			return markups[m]
		return None
	
	

def make_thml():
	thmlrenderer = thmlparser.THMLRenderer()
	items.append(thmlrenderer)
	thml = SW.PyThMLHTMLHREF(thmlrenderer)
	thml.thisown=False
	#thmlrenderer
	return thml

def make_osis():
	osisrenderer = osisparser.OSISRenderer()
	items.append(osisrenderer)
	bm_items.append(osisrenderer)
	
	
	osis = SW.PyOSISHTMLHREF(osisrenderer)
	osis.thisown=False
	return osis
 
osis = make_osis()
thml = make_thml()
osis2 = SW.OSISHTMLHREF()
thml2 = SW.ThMLHTMLHREF()

items.extend([osis2, thml2])

