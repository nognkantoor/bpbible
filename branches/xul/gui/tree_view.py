from util.observerlist import ObserverList
from util.debug import dprint, ERROR
from xpcom import components

class TreeItem(object):
	def __init__(self, text, data=None, is_open=False, 
			filterable=True, level=0):
		self._children = []
		self._text = text
		self.data = data
		self.filterable = filterable
		self.is_open = is_open
		self.level = level
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
		return TreeItem(self.text, self.data, level=self.level)

	def null_item(self):
		# shouldn't be seen, so no i18n needed
		return TreeItem("No items")

class LazyTreeItem(TreeItem):
	"""Builds up a tree lazily based on a data object which supports 
	__iter__ and __unicode__"""
	def __init__(self, data, has_children=None):
		super(LazyTreeItem, self).__init__(unicode(data), data)
		self.expanded = False

	@property
	def children(self):
		if self.expanded:
			return self._children

		for item in self.data:
			self.add_child(unicode(item), LazyTreeItem(item))

		self.expanded = True
		return self._children
	
	def has_children(self):
		if hasattr(self.data, "has_children"):
			return self.data.has_children()

		return super(LazyTreeItem, self).has_children()


class BasicTreeView(object):
	_com_interfaces_ = components.interfaces.nsITreeView

 	def __init__(self):
		self.on_selection = ObserverList()
		self.treeBox = None
		self.selection = None
		self.visibleData = []
		self._suppress_selection = False

	def setup(self, root_items, is_root=False):
		self.visibleData = []
		if is_root:
			self.model = root_items
		else:
			self.model = TreeItem("Dummy root item")

		self.model.level = -1
		if not is_root:
			for item in root_items:
				self.model.add_child(text=None, item=item)
		self.model = self.model
		self.visibleData = list(self.model.children)
		dprint(ERROR, "Visible data", self.visibleData)
	
	def filter(self, text):
		def get_filtered_items(model_item):
			return_item = model_item.clone_item()
			for item in model_item.children:
				ansa = get_filtered_items(item)
				if ansa:
					return_item.add_child(text=None, item=ansa)

			# if we are not filterable, or the text is not in our text, and we
			# haven't any children matching, return None
			if (not model_item.filterable 
				or text.upper() not in model_item.text.upper()) \
				and not return_item.children:
				return None

			return return_item

		root = get_filtered_items(self.model)
		if not root:
			root = self.model.null_item()

		l = len(self.visibleData)
		if l:
			self.selection.clearSelection()

		self.visibleData = list(root.children)
		diff = len(root.children) - l
		self.rowCountChanged(0, diff)
		self.expand_all()
		return len(self.visibleData)

	def expand_all(self):
		self.expand_items(self.visibleData, recursive=True)

	def setup_tree_events(self, tree):
		self.tree = tree
		self.tree.addEventListener("select", self.select_item, True)
		self.tree.addEventListener("dblclick", self.double_click_on_item, True)

	def select_item_without_event(self, item):
		self._suppress_selection = True
		try:
			self.selection.select(item)
		finally:
			self._suppress_selection = False

	def select_item(self, event):
		if not self._suppress_selection:
			self.on_selection("select", self.visibleData[self.tree.currentIndex])

	# XXX: Double click isn't the right event.  You get double clicks even
	# when you double click on the tree's scroll bars, and you don't get an
	# event if enter is pressed.
	# Should investigate performAction(), to see which actions it passes.
	def double_click_on_item(self, event):
		self.on_selection("dblclick", self.visibleData[self.tree.currentIndex])

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
	def canDrop(self, index, orientation): return False

class ListTreeView(object):
	"""This tree view is used as a wrapper for lists of strings.

	This is used by the dictionary lazy topic list.
	"""
	_com_interfaces_ = components.interfaces.nsITreeView

 	def __init__(self, items=None):
		self.treeBox = None
		self.items = items
		self.selection = None

	# nsITreeView methods.
 	def get_rowCount(self):
		return len(self.items)

	def setTree(self, treeBox):
		self.treeBox = treeBox

	def getCellText(self, index, column):
		return self.items[index]

	def isContainer(self, index):
		return False

	def isContainerOpen(self, index):
		return False

	def isContainerEmpty(self, index):
		return False

	def isSeparator(self, index):
		return False

	def isSorted(self):
		return False

	def isEditable(self, index, column):
		return False

	def getParentIndex(self, index):
		return -1

	def getLevel(self, index):
		return 0

	def hasNextSibling(self, index, after):
		return index != (len(self.items) - 1)

	def toggleOpenState(self, index):
		assert False, "It is not possible to open items in a string list."

	def rowCountChanged(self, index, number_of_items):
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
	def canDrop(self, index, orientation): return False	

	def scroll_to_row(self, row):
		# scroll nicely to a row
		# scrollToRow will scroll so that the given row is at the top, looks
		# bad for the last row...
		# ensureRowIsVisible ends up down the bottom
		# this ends up about 1/5th of the way down, or where it is on screen
		first = self.treeBox.getFirstVisibleRow()
		last = self.treeBox.getLastVisibleRow()
		# if it is already on the view, good
		# note we still move it if it is last
		if first <= row < last:
			return
		
		rows_shown = self.treeBox.height / self.treeBox.rowHeight 

		# this puts this row at the top
		max_items = self.get_rowCount()
		chosen_item = row - rows_shown * 0.2
		if chosen_item < 0: 
			chosen_item = 0
		else:
			if chosen_item + rows_shown > max_items:
				chosen_item = max_items - rows_shown

		self.treeBox.scrollToRow(chosen_item)


