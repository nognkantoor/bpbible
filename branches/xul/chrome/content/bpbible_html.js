function get_current_verse() {
	var current_verse = $("a.currentverse");
	if(current_verse.length != 1) {
		alert("Wrong number" + current_verse.length);
		return null;
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

$(document).ready(function() {
	var [start, end] = get_current_verse_bounds();
	
	// Highlight the verse's background
	highlight_range(start[0], end[0]);
	
	// Now scroll down to the right point
	var off = start.offset();
	var t = off.top;
	var l = off.left;
	/* Try and keep in middle
	 -40 is to correct for verse length, as we do not want start of 
	 verse to start half way down, but the middle to be in the middle */
	t -= window.innerHeight / 2 - 40;
	window.scrollTo(l, t);
});
