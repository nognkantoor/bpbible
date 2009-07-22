function get_start_point(){
	return get_current_verse_bounds()[0];
}


function highlight_verse(){
	var [start, end] = get_current_verse_bounds();
	if (start[0]) {
		// Highlight the verse's background
		highlight_range(start[0], end[0]);
	}
}

$(document).ready(function() {
	highlight_verse();
/*	var [start, end] = get_current_verse_bounds();
	scroll_to_current(start);*/
	
});

function get_current_verse() {
	var current_verse = $("#original_segment a.currentverse");
	if(current_verse.length != 1) {
		jsdump("Wrong number of current verses: " + current_verse.length + "\n");
		return current_verse;
	}
	return current_verse;
}

function get_current_verse_ref() {
	var current_verse = get_current_verse();
	return current_verse.attr("osisRef");
}

function get_current_verse_bounds() {
	var osisRef = get_current_verse_ref();
	var start = $('a[name="' + osisRef + '_start"]');
	var end = $('a[name="' + osisRef + '_end"]');
	return [start, end];
}

function get_selected_verse_ref() {
	var range = get_normalized_selection();
	if(!range) {
		var ref = get_current_verse_ref();
		return [ref, ref];
	}
	
	var last = null;
	var start = pick_element("a[name$=_start]", range, true);
	var end = pick_element("a[name$=_end]", range, false);
	
	return [start.getAttribute("osisRef"), end.getAttribute("osisRef")];
}

$('body').bind("mouseup", function() {
	d('up\n');
	var [start, end] = get_selected_verse_ref();
	d(start + ' --- ' + end);
});

