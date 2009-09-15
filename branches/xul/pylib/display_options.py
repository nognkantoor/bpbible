from util.configmgr import config_manager

options = config_manager.add_section("Options")
options.add_item("columns", False, item_type=bool)
options.add_item("verse_per_line", False, item_type=bool)
options.add_item("continuous_scrolling", True, item_type=bool)
options.add_item("coloured_quotes", True, item_type=bool)

def all_options():
	return options.items.keys()

def get_js_option_value(option):
	assert options.item_types[option] == bool, "Only bools supported at the moment"
	return "true" if options[option] else "false"
