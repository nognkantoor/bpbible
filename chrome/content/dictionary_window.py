import cgi
import datetime
from gui.tree_view import ListTreeView
from backend.bibleinterface import biblemgr
from backend.dictionary import date_to_mmdd
from util.debug import dump, dprint, ERROR
from util.unicode import to_str
from contrib.jsproxy import JSProxy

list_view = None
do_not_change_textbox_value = False

def on_load():
	global list_view
	initialise_module_name()
	list_view = ListTreeView(window.dictionary_topic_list)
	dictionary_list = document.getElementById("dictionary_list")
	dictionary_list.view = list_view
	dictionary_list.addEventListener("select", dictionary_list_select, True)
	if window.is_calendar:
		today = datetime.date.today()
		document.getElementById("dictionary_textbox").value = today.strftime("%B ") + str(today.day)
		dictionary_textbox_input(None)
		dp = document.getElementById("datepicker")
		window.datepicker = JSProxy(dp)
		dp.addEventListener("change", datepicker_change)
		document.getElementById("datepicker_panel").addEventListener("popupshowing", datepicker_showing)
		
	else:
		load_dictionary_entry_by_index(0)

	document.getElementById("datepicker_button").hidden = not window.is_calendar
	document.getElementById("dictionary_textbox").addEventListener("input", dictionary_textbox_input)

def dictionary_list_select(event):
	index = document.getElementById("dictionary_list").currentIndex
	load_dictionary_entry_by_index(index)
	if not do_not_change_textbox_value:
		document.getElementById("dictionary_textbox").value = window.dictionary_topic_list[index]

def datepicker_change(event):
	date = datetime.date(window.datepicker.year, window.datepicker.month + 1, window.datepicker.date)
	formatted_date = date.strftime("%B ") + str(date.day)
	document.getElementById("dictionary_textbox").value = formatted_date
	dictionary_textbox_input(event)

def datepicker_showing(event):
	selected_date = date_to_mmdd(document.getElementById("dictionary_textbox").value, return_formatted=False)
	dprint(ERROR, "selected date", selected_date)
	if selected_date is None:
		selected_date = datetime.date.today()
	window.datepicker.value = selected_date.isoformat()

def dictionary_textbox_input(event):
	global do_not_change_textbox_value
	topics = window.dictionary_topic_list
	text = document.getElementById("dictionary_textbox").value
	if window.is_calendar:
		mmdd = date_to_mmdd(text)
		if mmdd:
			text = mmdd
	idx = topics.mod.getEntryForKey(
		to_str(text, topics.mod)
	)

	idx = min(len(topics) - 1, idx)
	dprint(ERROR, "Dictionary index", str(idx))
	if idx >= 0:
		from xpcom import components
		dictionary_list = document.getElementById("dictionary_list")
		do_not_change_textbox_value = True
		dictionary_list.view.selection.select(idx)
		do_not_change_textbox_value = False
		list_view.scroll_to_row(idx)

def load_dictionary_entry_by_index(index):
	browser = document.getElementById("browser")
	# Clear the window.
	browser.setAttribute("src", "bpbible://")
	# Get the dictionary entry.
	# This is got by index to avoid issues with case-sensitive key names and case-insensitive URLs.
	browser.setAttribute("src", "bpbible://content/page/%s/%d" % (window.mod_name, index))
	document.title = get_window_title(index)

def get_window_title(index):
	return u"%s (%s) - BPBible" % (window.dictionary_topic_list[index], window.mod_name)

def initialise_module_name():
	module_name = "ISBE"
	if window.location.search:
		parameters = cgi.parse_qs(window.location.search[1:])
		if parameters.has_key("module_name"):
			module_name = parameters["module_name"][0]
	dprint(ERROR, "Initialising module name to %s" % module_name)
	window.mod_name = module_name
	biblemgr.dictionary.SetModule(module_name, notify=False)
	window.dictionary_topic_list = biblemgr.dictionary.GetTopics(user_output=True)
	window.is_calendar = biblemgr.dictionary.is_daily_devotional
