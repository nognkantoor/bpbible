/**
Function to be run when the BPBible window is loaded.
*/
function onLoad() {
	window.gFindBar = document.getElementById('FindToolbar');
	var browser = document.getElementById("browser");
	browser.setAttribute("tooltip", "aHTMLTooltip");
	var tt = document.createElement("tooltip")
	tt.id="aHTMLTooltip" 
	tt.addEventListener("popupshowing",
		function(event) {
			var done = FillInHTMLTooltip(document.tooltipNode);
			if (!done) event.preventDefault();
		}, false);
	
	browser.parentNode.insertBefore(tt, browser);
}

window.addEventListener("load", onLoad, false);

document.addEventListener("process_tooltip", function(evt) { 
	var broadcaster = document.getElementById(evt.target.id);
	broadcaster.setAttribute("firer", evt.target.getAttribute("firer"));
	broadcaster.setAttribute("leaving", evt.target.getAttribute("leaving"));
	broadcaster.removeAttribute("href");
	broadcaster.setAttribute("href", 
		evt.target.getAttribute("href"));
}, false, true);

/** BM note: this has been copied from firefox (browser.js). 
 ** If that is updated, this should this be as well**/

/**
 * Content area tooltip.
 * XXX - this must move into XBL binding/equiv! Do not want to pollute
 *       browser.js with functionality that can be encapsulated into
 *       browser widget. TEMPORARY!
 *
 * NOTE: Any changes to this routine need to be mirrored in ChromeListener::FindTitleText()
 *       (located in mozilla/embedding/browser/webBrowser/nsDocShellTreeOwner.cpp)
 *       which performs the same function, but for embedded clients that
 *       don't use a XUL/JS layer. It is important that the logic of
 *       these two routines be kept more or less in sync.
 *       (pinkerton)
 **/

function FillInHTMLTooltip(tipElement)
{
  var retVal = false;
  if (tipElement.namespaceURI == "http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul")
    return retVal;

  const XLinkNS = "http://www.w3.org/1999/xlink";


  var titleText = null;
  var XLinkTitleText = null;
  var direction = tipElement.ownerDocument.dir;

  while (!titleText && !XLinkTitleText && tipElement) {
    if (tipElement.nodeType == Node.ELEMENT_NODE) {
      titleText = tipElement.getAttribute("title");
      XLinkTitleText = tipElement.getAttributeNS(XLinkNS, "title");
      var defView = tipElement.ownerDocument.defaultView;
      // XXX Work around bug 350679:
      // "Tooltips can be fired in documents with no view".
      if (!defView)
        return retVal;
      direction = defView.getComputedStyle(tipElement, "")
        .getPropertyValue("direction");
    }
    tipElement = tipElement.parentNode;
  }

  var tipNode = document.getElementById("aHTMLTooltip");
  tipNode.style.direction = direction;
  
  for each (var t in [titleText, XLinkTitleText]) {
    if (t && /\S/.test(t)) {

      // Per HTML 4.01 6.2 (CDATA section), literal CRs and tabs should be
      // replaced with spaces, and LFs should be removed entirely.
      // XXX Bug 322270: We don't preserve the result of entities like &#13;,
      // which should result in a line break in the tooltip, because we can't
      // distinguish that from a literal character in the source by this point.
      t = t.replace(/[\r\t]/g, ' ');
      t = t.replace(/\n/g, '');

      tipNode.setAttribute("label", t);
      retVal = true;
    }
  }

  return retVal;
}

