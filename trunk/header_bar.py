import wx
from swlib import pysw
from backend import chapter_headings
from protocols import protocol_handler
from displayframe import DisplayFrame
from gui import guiutil
from tooltip import Tooltip 
import guiconfig
from util.observerlist import ObserverList


def on_headings_hover(frame, href, url, x, y):
	if url is None:
		url = SW.URL(href)
	
	ref = url.getHostName()
	ref = pysw.GetBookChapter(ref)
	html = '<font size=+1><b><a href="nbible:%s">%s</a></b></font>' % (ref,ref)
	vk = pysw.VK((ref, ref))
	html += ": %d verses<br>" % len(vk)
	
	html += "<ul>"
	
	for vk, text in chapter_headings.get_chapter_headings(ref):
		html += '<li><a href="nbible:%s">%s</a>' % (vk, text)
	html += "</ul>"
	
	frame.tooltip.SetText(html)

	screen_x, screen_y = frame.ClientToScreen((x, y))
	
	frame.tooltip.set_pos(screen_x, screen_y)
	frame.tooltip.is_biblical = False
	frame.tooltip.Start()

protocol_handler.register_hover("headings", on_headings_hover)
protocol_handler.register_handler("headings", DisplayFrame.on_link_clicked_bible)

def get_line_colour():
	return wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW)

	
class ChapterItem(wx.Panel):
	"""
	A chapter item in the header bar. 
	Handles mouse over and drawing itself
	"""

	# how much border around the text do we want?
	border = 3

	def __init__(self, parent, chapter, display=None, is_current=False):
		super(ChapterItem, self).__init__(parent)
		
		self.chapter = chapter
		if display is None:
			self.display = chapter
		else:
			self.display = display
		self.is_current = is_current
		self.Bind(wx.EVT_PAINT, self.on_paint)

		# we have a buffered drawing, so we don't care about erasing the
		# background
		self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)
		
		# callafter as under MSW, enter seems to come before leave in
		# places
		self.Bind(wx.EVT_ENTER_WINDOW, 
			lambda evt:wx.CallAfter(self.on_enter, evt.X, evt.Y))
		self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
		self.Bind(wx.EVT_LEFT_UP, lambda evt: 
			self.Parent.on_click(self.chapter)
		)
		

		# draw our bitmapped version, and set our size based on it
		self.draw()
	
	def set_chapter(self, chapter, display=None):
		if self.chapter == chapter:
			return

		if display is None:
			self.display = chapter
		else:
			self.display = display

		self.chapter = chapter
		self.draw()
		self.Refresh()

	def on_enter(self, x, y):
		self.Parent.current_target = self
		if self.Parent.tooltip.target == self:
			return

		protocol_handler.on_hover(self.Parent, 
			"headings:%s" % self.chapter, x, y)

	def on_leave(self, event):
		self.Parent.current_target = None
	
		self.Parent.tooltip.MouseOut(None)
		
		#if (not self.Parent.tooltip.IsShown() or 
		#	not self.Parent.tooltip.mouse_is_over):
		#	self.Parent.tooltip.Stop()

	def draw(self):
		# create a memory dc
		dc = wx.MemoryDC()

		# set its font to the window font
		dc.SetFont(self.Font)
		
		# get the size of the text
		text = str(self.display)
		text_width, text_height = dc.GetTextExtent(text)

		# and of the window
		width = text_width + self.border * 2
		height = text_height + self.border * 2
		
		# create a bitmap of the given size and select it into the DC
		bmp = wx.EmptyBitmap(width, height)
		dc.SelectObject(bmp)
		
		# set up the dc
		dc.SetBrush(wx.Brush(self.BackgroundColour))
		pen = wx.TRANSPARENT_PEN
		dc.SetPen(pen)
		
		# do the drawing
		dc.DrawRectangle(0, 0, width, height)
		dc.DrawText(text, self.border, self.border)
		
		dc.Pen = wx.Pen(get_line_colour())
		
		
		if self.is_current:
			# draw top, left and right borders
			dc.DrawLine(0, 0, 0, height)
			dc.DrawLine(0, 0, width-1, 0)
			dc.DrawLine(width-1, 0, width-1, height)
		else:
			# draw bottom border
			dc.DrawLine(0, height-1, width, height-1)
			
			

		
		# assign the resultant bitmap
		del dc
		self.bmp = bmp
		
		# and set our size
		self.SetSize((width, height))
		#self.SetMinSize((width, height))
		
	
	def on_paint(self, event):
		# paint it on
		wx.BufferedPaintDC(self, self.bmp)
	
	def set_background_colour(self, colour):
		self.SetBackgroundColour(colour)
		self.draw()

class Line(wx.Window):
	"""A rectangle of colour"""
	def __init__(self, parent):
		super(Line, self).__init__(parent)
		self.Bind(wx.EVT_PAINT, self.paint)
	
	def paint(self, event):
		dc = wx.PaintDC(self)
		dc.Background = wx.Brush(get_line_colour())
		dc.Clear()
	
class HeaderBar(wx.Panel):
	def __init__(self, parent, current_chapter, style=wx.NO_BORDER):
		super(HeaderBar, self).__init__(parent, style=style)
		
		self.current_chapter = current_chapter
		self.Bind(wx.EVT_SIZE, self.on_size)
		self.on_click = ObserverList()
		
		# if we are at either end of the Bible, this line fills in the rest of
		# the bottom line.
		self.line = Line(self)

		self.create_item()
		
		self.MinSize = -1, self.item.Size[1] + 1

		
		self.tooltip = Tooltip(guiutil.toplevel_parent(self), 
				style=wx.NO_BORDER,
				html_type=DisplayFrame, logical_parent=self)
		
		# For compatibility with display frame:
		# code in displayframe wants it to have an _tooltip member (MouseIn)
		self._tooltip = self.tooltip
		# and a logical_parent
		self.logical_parent = None

		if guiconfig.mainfrm:
			guiconfig.mainfrm.add_toplevel(self.tooltip)

		self.items = [[], []]
	
	
	def create_item(self):
		self.item = ChapterItem(self, self.current_chapter, is_current=True)
		self.item.Position = 0, 0
		font = self.item.Font
		font.SetWeight(wx.FONTWEIGHT_BOLD)
		#font.PointSize += 2
		self.item.Font = font
		
		self.item.set_background_colour("White")
		
	def set_current_chapter(self, chapter):
		guiutil.FreezeUI(self)
	
		# stop tooltip
		self.tooltip.Stop()

		# set new current item
		self.current_chapter = chapter
		self.item.set_chapter(chapter)
		
		# and refresh everything else
		self.on_size()

	def get_next_chapter(self, book_chapter, dir=1, short=True):
		vk = pysw.VK(book_chapter)
		vk.chapter += dir
		if vk.Error():
			return None, None

		if short:
			items = (vk.getBookAbbrev(), vk.chapter)
		else:
			items = (vk.getBookName(), vk.chapter)
			

		return ("%s %s" % items), vk.chapter

	def on_size(self, event=None):
		guiutil.FreezeUI(self)
		
		self.line.Hide()

		# keep a new list of the previous and next items
		new_items = [[], []]

		item = self.item

		# position our main item
		item.Position = (self.Size[0] -item.Size[0]) / 2, 1#item.Position[1]
	
		for dir, is_left in (1, False), (-1, True):
			last_item = item
			
			break_next = False

			# an array of the old items on this side
			items = self.items[not is_left]

			while not break_next:
				next_chapter, chapter_number = \
					self.get_next_chapter(last_item.chapter, dir)

				# if there is no next chapter, we have reached the start or
				# end of the Bible, so stop
				if next_chapter is None:
					self.line.Show()
					w, h = self.Size
					if is_left:
						self.line.MoveXY(0, h-1)
						self.line.Size = (last_item.Position[0] + 1, 1)
					else:
						last_end = last_item.Position[0] + last_item.Size[0]
						self.line.MoveXY(last_end, h - 1)
						self.line.Size = (self.Size[0] - last_end, h-1)
						
					break
				
				# if we've run out of items on this side, start creating new
				# ones
				if not items:
					next_item = ChapterItem(self, next_chapter)
					#, chapter_number)
					next_item.set_chapter(next_chapter)
					next_item.set_background_colour(
						wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE)
					)
					

				# Otherwise, remove the old ones from the list and move on
				else:
					next_item = items.pop(0)
					next_item.set_chapter(next_chapter)#, chapter_number)

				# find the item's position
				break_next = self.position_item(next_item, last_item, is_left)
	
				# and add it to our list of new items
				new_items[not is_left].append(next_item)

				# and update last item and chapter
				last_item = next_item
				last_chapter = next_chapter

		# delete the items we haven't used this time
		for item in self.items[0] + self.items[1]:
			item.Destroy()

		# and update our list of items
		self.items = new_items
		
	def position_item(self, next_item, last_item, is_left):
		"""Positions an item based on the previous one and the direction
		
		Returns True if this is the last item to do on this side"""
		if is_left:
			next_item.Position = (
				last_item.Position[0] - next_item.Size[0],
				last_item.Position[1]
			)
		else:
			next_item.Position = (
				last_item.Position[0] + last_item.Size[0],
				last_item.Position[1]
			)
		
		if is_left:
			if next_item.Position[0] <= 0:
				# on or past the left hand border
				return True
		else:
			if next_item.Position[0] + next_item.Size[0] >= self.Size[0]:
				# on or past the right hand border
				return True
			
if __name__ == '__main__':
	a = wx.App(0)
	f = wx.Frame(None)
	h = HeaderBar(f, "Psalms 150")#Revelation 20")
	h.on_click += lambda ref:h.set_current_chapter(ref)
	f.Fit()
	f.Show()
	a.MainLoop()
