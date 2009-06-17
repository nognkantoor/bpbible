/**
Function to be run when the BPBible window is loaded.
*/
function onLoad() {
	window.gFindBar = document.getElementById('FindToolbar');
}

window.addEventListener("load", onLoad, false);

document.addEventListener("process_tooltip", function(evt) { 
	var broadcaster = document.getElementById(evt.target.id);
	broadcaster.removeAttribute("attribute1");
	broadcaster.setAttribute("attribute1", 
		evt.target.getAttribute("attribute1"));
}, false, true);

