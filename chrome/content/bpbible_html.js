// dump to the js console (xulrunner -jsconsole)
function jsdump(str)
{
	Components.classes['@mozilla.org/consoleservice;1']
			  .getService(Components.interfaces.nsIConsoleService)
			  .logStringMessage(str);
}

function jserror(str)
{
	Components.utils.reportError(str);
}

function get_current_verse() {
	var current_verse = $("a.currentverse");
	if(current_verse.length != 1) {
		jsdump("Wrong number of current verses: " + current_verse.length);
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

function pick_element(selector, range, before) {
	var last = null;
	var done = false;
	$(selector).each(function() {
		var r = range.comparePoint(this, 0);
		if(r > 0 || (before && r == 0)) {
			if(before) {
				/* alert(this.getAttribute("osisRef")); */
				var newRange1 = range.cloneRange();
				newRange1.setEndAfter(this);
				var newRange2 = newRange1.cloneRange();
				newRange2.setStartBefore(this);
				var s1 = newRange1.toString().replace(/$\s+/, '');
				var s2 = newRange2.toString().replace(/$\s+/, '');

				alert(s1 + s2);
				alert("'" + s1 + "'\\\\'" + s2 + "'");
				
				if(s1 == s2) {
					alert("Equal");
					last = this;
					
				}
			}
			
			// We are now past it
			// If before is true, we pick the last one, otherwise we pick this
			// one
			if(before && r == 0 && false) {
				/* Check if we are only nominally in a text node (i.e. we are
				 * right at the end of it, but we don't contain any content)
				 * This can happen if we are selecting verses, and it is
				 * important that if that is the case, we don't include one 
				 * verse too many... */
				if(range.startContainer.nodeType == Node.TEXT_NODE
					&& range.startOffset == range.startContainer.length) {
					// Now we need to check that if it hadn't included the
					// empty previous part, it would have been right on our
					// verse number.
					last = this;
				}
			}
			
			if(!before) last = this;
			
			if(before && !last) {
				alert("Before but not last? pre-something content selected?");
				last = this;
			}
			
			// Stop processing
			done = true;
			return false;
		}
		//if(r == 0) alert("Right on the spot? really?");

		last = this;
		return true;
	});

	if(!done) alert("Didn't finalize element finding " + selector)
	if(!last) alert("Last is null!");

	return last;
}

function get_normalized_selection(){
	var selection = window.getSelection();

	// We ignore multiple selections At the Moment
	var range = selection.getRangeAt(0);
	if(range.collapsed) return null;
	return range;

	// We can move forward over: 
	// . Text nodes where we are at the end
	// . empty <a> tags
	while(
		(range.startContainer.nodeType == Node.TEXT_NODE
			&& range.startOffset == range.startContainer.length)
		|| (range.startContainer.nodeName == "A" &&
			range.startContainer.children.length == 0)
		|| (range.startContainer.nodeName == "BR" &&
			range.startContainer.class	  == "verse_per_line" &&
			range.startContainer.children.length == 0)) {
		alert("Skipping over");
		var next = range.startContainer.nextSibling;
		if(!next) next = range.startContainer.parentNode;
		if(!next) {
			alert("Don't we have a parent or sibling here???");
			return null;
		}

		range.setStart(next, 0);
		if(range.collapsed) {
			alert("Range collapsed while normalizing???");
			return null;
		}
	}
	alert(range.startContainer.nodeName);

	return range;
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

function scroll_to_current(start) {
	if(!start) start = get_current_verse_bounds()[0];
	//alert(start);
	// Now scroll down to the right point
	var off = start.offset();
	var t = off.top;
	var l = off.left;
	/* Try and keep in middle
	 -40 is to correct for verse length, as we do not want start of 
	 verse to start half way down, but the middle to be in the middle */
	t -= window.innerHeight / 2 - 40;
	l -= window.innerWidth / 2;
	
	window.scrollTo(l, t);
}

$(document).ready(function() {
	var [start, end] = get_current_verse_bounds();
	
	// Highlight the verse's background
	highlight_range(start[0], end[0]);
	scroll_to_current(start);
	
});

$(document).ready(function(){
	$('a.footnote').bind("mouseenter", function(){
		dump("Dispatching event\n");
		var element = document.createElement("MyExtensionDataElement");
		element.setAttribute("id", "process_tooltip");
		element.setAttribute("attribute1", "foobar");
		document.documentElement.appendChild(element);

		var evt = document.createEvent("Event");
		evt.initEvent("process_tooltip", true, false);
		element.dispatchEvent(evt);

		/* I hope/presume that dispatchEvent is synchronous... :D */
		element.parentNode.removeChild(element);
	});
});
