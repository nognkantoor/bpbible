/* Highlighting utilities */
function extract_range(r) {
	/* pull out a range and replace with a span. 
	 * Note: the way we use this can end up with (for example) <span>'s
	 * being the parents of <div>'s. I'm not sure if this is strictly legal...
	 */
	if(!r.collapsed) {
		var newNode = document.createElement("span");
		newNode.className = "highlight";
		r.surroundContents(newNode);
	}
}

function highlight_range(start, end) {
	var range = document.createRange();
	range.setStartAfter(start);
	range.setEndBefore(end);
	var common_parent = range.commonAncestorContainer;
	var r = document.createRange();
	
	// We need to travel up from our start point, collecting all to the 
	// right of our start node.
	var s = start;
	while (s.parentNode != common_parent) {
		r.selectNodeContents(s.parentNode);
		r.setStartAfter(s);
		extract_range(r);
		s = s.parentNode;
	}
	
	var e = end;
	// Now, we need to travel up from our end point, collecting everything to
	// the left of our start node.
	while (e.parentNode != common_parent) {
		r.selectNodeContents(e.parentNode);
		r.setEndBefore(e);
		extract_range(r);
		e = e.parentNode;
	}

	/* and now we need to get the part at the top of our range, between the
	 * two topmost points */
	r.setStartBefore(s);
	r.setEndAfter(e);
	extract_range(r);
}
