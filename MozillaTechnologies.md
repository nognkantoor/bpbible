# Introduction #

The Mozilla Platform has a lot of available functionality.  Much of this functionality is either:
  * Provided by Python in some form;
  * Provided by BPBible current in some form;
  * Able to be done better our way than the Mozilla way.

Some of the technology is very good, so we really need to evaluate it and to decide what is useful and what isn't, and more importantly _why_ we make the decisions that we do.

Note: This is particularly talking about _Mozilla-specific_ functionality.  I am assuming that it is not necessary to discuss using standard web technologies such as HTML and CSS and Javascript (generally including Mozilla specific extensions to these), nor is it necessary to discuss core Mozilla technologies such as XUL which we will not have a Mozilla application without.

We should also use the technologies well if we use them.  For example, check performance best practices (https://wiki.mozilla.org/Performance/Addons/BestPractices).

# Technologies #

## Extensions/Overlays ##
Mozilla's extension system is designed to handle extensibility for a major application like Firefox, using XPI files and the extension manager for distribution and overlays to change the behaviour of the application.  I would think it very unlikely that we could get a much better system for extending a XUL application than Mozilla extensions, and it could take considerable effort to do it.  Unless we have a very good reason not to use it, any extensibility provided for the application should use Mozilla extensibility.

Overlays are used by extensions to add elements and scripts to an existing chrome URL.  This would be pretty much required.  However, also worth considering is whether they can help the internal design of the application.  Should some behaviour be overlaid rather than coded into the main window?  Should we be trying to make the different parts of our application like internal "extensions"? (not necessarily that they can be uninstalled or disabled by the user, just that a part of the application can be completely self-contained and define where to put its menu items, etc. in an overlay rather than having to alter the main form whenever you want to add a new menu item).

## XBL ##

XBL can be used to abstract the behaviour and presentation of a component into a single component that can be bound to different XML elements.  This could be handy for increasing the modularity of the system and having proper components that can be used in multiple places.

XBL 2 looks like a much cleaner version of XBL (see http://www.w3.org/TR/xbl-primer/).  Unfortunately, it's probably not well supported by Mozilla yet.  There is an implementation in Javascript at http://code.google.com/p/xbl/, though I don't know how good it is.

Mozilla XBL homepage at https://developer.mozilla.org/en/XBL.

## Commands ##
Mozilla uses a command framework for handling actions as well as allowing direct access to events.  It's probably somewhat similar to the action frameworks in Qt, Swing, etc.  This may be worth thinking about using.

## XPCOM ##
XPCOM is the Mozilla system for giving objects interfaces in a cross-language way (similar in intent to COM, CORBA, ...).  It will almost certainly be necessary to use XPCOM to communicate with Mozilla and to implement Mozilla interfaces.  It will possibly also be necessary to use it to communicate between Javascript and a Python backend.

If we do provide XPCOM interfaces, we also need to consider to what extent they are binding and frozen (I know Ben will want them utterly unfrozen and able to be changed at any time, while extension developers will want them more stable.  Some compromise is probably necessary).

## RDF ##
RDF is used in Mozilla as a persistent storage mechanism for configuration files, etc.  It could be used to replace our existing configuration files.

It is also used in data sources, where it can be used to create a UI with RDF templates.  Things like the Places API and History are also available as RDF data sources, and this allows any UI using the data source to be automatically updated when the data source is updated.  Some of our things might be worth exposing as data sources.

However, RDF can not (it appears) be used in an editable way with editable trees.  This rules out its use in places like Topic Management.

Mozilla RDF homepage at https://developer.mozilla.org/en/RDF.

## Internationalisation ##
The Mozilla internationalisation framework is based on named entities and DTD stylesheets for those entities.  It looks quite cumbersome to maintain the DTD files, but we might want to have our own intermediate format anyway.  This is probably worth at least considering using (though it will be harder for the developers than the current "Just wrap an "_" around a string)._

## Bookmarks / Places ##

The Mozilla bookmarks window and Places API has many similarities to BPBible's topic management (at least in part because BPBible's manage topics window was based on the Firefox Bookmarks window).

This should probably not be reused, as some of our future plans for user editable content (e.g. mapping to a user editable module) are unlikely to be compatible.  However, some of the UI / backend logic may be able to be reused.

Mozilla Places homepage at https://developer.mozilla.org/en/Places.

## Protocol handling ##
We can use a protocol handler to encapsulate access to any module content, using module specific URLs (like the sword:// URL, though we would be much better to use bpbible:// to ensure no conflicts breaking our application).

This is actually present in basic form in SVN, but could get very tricky very quickly if we are trying to encapsulate too much of the state of the Window (think about the URL for having the ESV, the KJV and the AB in parallel for Genesis 3: 2 - 7, with the KJV displaying WoC and Strong's Numbers and the others having all display settings turned off).

## Utility classes and methods ##
Mozilla provides many things that are part of the standard library in Python (and probably are necessary to make Javascript able to implement real applications).  However, if we are able to get them from Python, we will probably get a better and more "Pythonic" interface, and be better able to use existing Python code.  Networking and file access are prime examples.  However, some classes provided by Mozilla may still be more useful than the Python equivalent and should be considered.

### Threading ###
While Python does provide threading support, mixing it with the Mozilla threading support could be quite dangerous and have unexpected side-effects.  I think it's probably worth considering using the Mozilla implementation just to ensure that we avoid nasty (and possibly OS or environment specific) interactions.

Possibly relevant articles:
  * https://developer.mozilla.org/En/The_Thread_Manager
  * https://developer.mozilla.org/En/NSPR_API_Reference/Threads
  * https://developer.mozilla.org/En/Code_snippets/Threads

Nowadays, Mozilla seems to prefer recommending web workers rather than using threads raw.