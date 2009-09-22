from gui.tree_view import BasicTreeView, LazyTreeItem
from swlib.pysw import ImmutableTK
from backend.bibleinterface import biblemgr

class GenbookTreeView(BasicTreeView):
	def __init__(self, module_name):
		super(GenbookTreeView, self).__init__()
		self.module_name = module_name

		tk = biblemgr.genbook.GetKey()
		itk = ImmutableTK(tk)
		self.setup(LazyTreeItem(itk), is_root=True)

	def go_to_key(self, genbook_key_text):
		tk = biblemgr.genbook.GetKey(genbook_key_text)
		ref_to_aim_for = ImmutableTK(tk)
		
		# position both at root
		tk.root()
		root_item = self.model

		def look_for(tree_item, index):
			while tk != ref_to_aim_for:
				succeeded = tk.nextSibling()
				if not succeeded or tk > ref_to_aim_for:
					if succeeded:
						# too far, go back
						tk.previousSibling()
					
					# now try in the children
					result = tk.firstChild()
					assert result, \
						"Couldn't get child even though should have a child"

					if tree_item != self.model: 
						self.expand_item(tree_item)
					assert len(tree_item.children) > 0
					tree_item = tree_item.children[0]

					look_for(tree_item, 0)
					return
				else:
					assert tree_item.has_next_sibling()
					index += 1
					tree_item = tree_item.parent.children[index]
			
			index = self.visibleData.index(tree_item)
			self.selection.select(index)
			self.scroll_to_row(index)
		
		look_for(root_item, 0)
