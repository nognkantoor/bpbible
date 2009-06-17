$(document).ready(function(){	
	set_columns($('body[columns="true"]').length);
	$("body").bind("DOMAttrModified", function(event) {
		if(event.attrName != "columns") {
			if(event.attrName != "style" && $('body[columns="true"]'.length)) {
				// setting an option, may need to resize
				handle_resize();
			}
			return;			
		}
		set_columns(event.newValue == "true");
	});
});

var hyphenation_setting = true;
var on_loading = true;
function set_columns(to) {
	var was_on_loading = on_loading;
	if(!to) {
		var v = $("#HyphenatorToggleBox");
		if(v.length) {
			//alert("Turning off");
			// Now turn it off just in case
			hyphenation_setting = v[0].firstChild.data == 'Hy-phe-na-ti-on';
			if(hyphenation_setting) 
				Hyphenator.toggleHyphenation();
		
			$(window).unbind('resize', handle_resize);
		}
	} else {
		//alert("Running");
		$("#content").addClass("hyphenate");
		var hyphenatorSettings = {
			onhyphenationdonecallback : function () {
				handle_resize();
				if(was_on_loading) 
					scroll_to_current(null);

				handle_resize(true);
				//handle_resize(true);
				//document.body.height = window.innerHeight - 25;
				$(window).bind('resize', false, handle_resize);
				if(!hyphenation_setting) {
					Hyphenator.toggleHyphenation();
				}
			},
			onerrorhandler : function(e) {
				jserror("Hyphenate error: " + e.message);
				$("#content")[0].style.removeProperty('visibility');

			}
		};
		Hyphenator.config(hyphenatorSettings);
		Hyphenator.run();

	}
	on_loading = false;
	
}


var next = "inherit";
function handle_resize(twice, dont_reflow) {
	var c = $("#content");

	// Body has an 8px margin
	c.height($(window).height() - c.offset().top - 8);
	//dump($(window).height() - c.offset().top - 8 + '\n');

	// OK, I admit it - this is a nasty hack
	// We need the document to reflow, and changing the body height between
	// 100% and inherit makes it do this
	// TODO: remove this hack
	if(!dont_reflow) {
		$(document.body).height(next);
		next = next == "inherit" ? "100%" : "inherit";
	}

	// And when we first load the page, we need to do this twice, or we get a
	// scroll-bar
	if(twice) {
		handle_resize(false);
	}
}

function toggle() {
	if(document.body.getAttribute("columns") == "true")
		document.body.setAttribute("columns", "false");
	else
		document.body.setAttribute("columns", "true");		
}
