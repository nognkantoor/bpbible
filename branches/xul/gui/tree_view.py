from util.observerlist import ObserverList
from util.debug import dprint, ERROR
from xpcom import components

class TreeItem(object):
	def __init__(self, text, data=None, is_open=False, filterable=True):
		self._children = []
		self._text = text
		self.data = data
		self.filterable = filterable
		self.is_open = is_open
		self.level = 0
		self.parent = None

	@property
	def text(self):
		return self._text

	@property
	def children(self):
		return tuple(self._children)

	def has_children(self):
		return len(self.children) > 0

	def has_next_sibling(self):
		return not self.parent.is_last_child(self)

	def add_child(self, text, item=None, data=None, filterable=True):
		if item is None:
			item = TreeItem(text, data, filterable)

		self._children.append(item)
		item.level = self.level + 1
		item.parent = self
		return item

	def is_last_child(self, item):
		last_child = self._children[-1]
		return item is last_child

	def clone_item(self):
		return TreeItem(self.text, self.data)

	def null_item(self):
		# shouldn't be seen, so no i18n needed
		return TreeItem("No items")

class BasicTreeView(object):
	_com_interfaces_ = components.interfaces.nsITreeView

 	def __init__(self):
		self.on_selection = ObserverList()
		self.treeBox = None
		self.selection = None
		self.visibleData = []

	def setup(self, root_items):
		self.visibleData = []
		self.dummy_root_item = TreeItem("Dummy root item")
		self.dummy_root_item.level = -1
		for item in root_items:
			self.dummy_root_item.add_child(text=None, item=item)
		self.visibleData = root_items
		dprint(ERROR, "Visible data", self.visibleData)

	def expand_all(self):
		self.expand_items(self.visibleData, recursive=True)

	def setup_tree_events(self, tree):
		self.tree = tree
		self.tree.addEventListener("dblclick", self.double_click_on_item, True)

	def double_click_on_item(self, event):
		self.on_selection(self.visibleData[self.tree.currentIndex])

	def expand_items(self, items, recursive=False):
		for item in items:
			self.expand_item(item, recursive)

	def expand_item(self, item, recursive=False):
		if not item.is_open:
			self.toggleOpenState(self.visibleData.index(item))

		if recursive and item.has_children():
			self.expand_items(item.children, recursive)

	# nsITreeView methods.
 	def get_rowCount(self):
		return len(self.visibleData)

	def setTree(self, treeBox):
		self.treeBox = treeBox

	def getCellText(self, index, column):
		return self.visibleData[index].text

	def isContainer(self, index):
		return self.visibleData[index].has_children()

	def isContainerOpen(self, index):
		return self.visibleData[index].is_open

	def isContainerEmpty(self, index):
		return False

	def isSeparator(self, index):
		return False

	def isSorted(self):
		return False

	def isEditable(self, index, column):
		return False

	def getParentIndex(self, index):
		if self.isContainer(index):
			return -1

		for new_index in range(index - 1, -1, -1):
			if self.isContainer(new_index):
				return new_index

	def getLevel(self, index):
		return self.visibleData[index].level

	def hasNextSibling(self, index, after):
		return self.visibleData[index].has_next_sibling()

	def toggleOpenState(self, index):
		item = self.visibleData[index]
		if not item.has_children():
			return

		item.is_open = not item.is_open
		num_children = len(item.children)

		if item.is_open:
			# Opening.
			for child_index, child in enumerate(item.children):
				self.visibleData.insert(index + 1 + child_index, child)
			# XXX: This won't handle the case when multiple levels are closed
			# at once.
			self.rowCountChanged(index + 1, len(item.children))
		else:
			# Closing.
			current_level = item.level
			num_children = 0
			for child_index in xrange(index + 1, len(self.visibleData)):
				if self.visibleData[child_index].level <= current_level:
					break
				num_children += 1
			del self.visibleData[index + 1: index + 1 + num_children]
			self.rowCountChanged(index + 1, -num_children)
		self.invalidateRow(index)

	def rowCountChanged(self, index, number_of_items):
		# If you call expand_all() before this is associated with a tree box
		# then it will fail.
		if self.treeBox:
			self.treeBox.rowCountChanged(index, number_of_items)

	def invalidateRow(self, index):
		# If you call expand_all() before this is associated with a tree box
		# then it will fail.
		if self.treeBox:
			self.treeBox.invalidateRow(index)

	def getImageSrc(self, index, column): pass
	def getProgressMode(self, index, column): pass
	def getCellValue(self, index, column): pass
	def cycleHeader(self, col): pass
	def selectionChanged(self): pass
	def cycleCell(self, index, column): pass
	def performAction(self, action): pass
	def performActionOnCell(self, action, index, column): pass
	def getRowProperties(self, index, column): pass
	def getCellProperties(self, index, column, prop): pass
	def getColumnProperties(self, column, element): pass
