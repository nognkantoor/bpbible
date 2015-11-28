# Introduction #

How to set up a XUL and PyXPCOM instance to use with BPBible.

# Source #
The source is currently in SVN in branches/xul.

# Setup #
Start off looking at http://pyxpcomext.mozdev.org/no_wrap/tutorials/pyxulrunner/python_xulrunner_about.html.

Take your BPBible configuration files and BPBible binary libraries from an existing BPBible installation.

Copy xulrunner/xulrunner-stub to bpbible, and use it (see the tutorial above for more detailed explanations of setting up XULRunner). You should probably have set PYTHONPATH=.

# Possibly useful tools and Firefox extensions #
PyShell (http://pyxpcomext.mozdev.org/samples.html).  Already present in SVN.

DOM Inspector: Already present in SVN.

XPCOMViewer (https://addons.mozilla.org/en-US/firefox/addon/7979)

Venkman (Javascript debugger, contains some of the layout we might want) (http://www.mozilla.org/projects/venkman/).

ChromeBug: Nice extension, but still in alpha and haven't yet found a XULRunner application apart from Firefox that it works on.  Tried to integrate it and so far have failed.

Extension Developer's extension: Live XUL editor, Javascript shell, ...  Already present in SVN.

# Notes #
XULRunner has this annoying habit of letting a XULRunner instance hang around, and using that instance in future.  This causes problems if components are added and not registered on startup because a new instance is not being created.  Periodically run through in Task Manager and kill everything with your XULRunner stub name to make sure.

To show the Error Console, run with bpbible -jsconsole.  utils.debug.dprint() and utils.debug.dump() will write debugging printouts and status messages to the Error Console.

If you ever want to change the components in the components directory, they will not be re-registered.  The easiest way to force them to re-register is to change the build ID in the application.ini file, then run bpbible (then please change it back so we don't have spurious changes to it in SVN).

If you are wishing to install an extension in the extensions directory, make sure that it goes in a directory marked by its ID (typically a GUID, find it in install.rdf).  Also change the overlay (in the extension's chrome.manifest) to overlay onto chrome://bpbible/content/bpbible.xul rather than chrome://browser/content/browser.xul (which will work if it is just adding items to the Tools menu), and if it has an update URL that is http:// then remove it or comment it out (again in install.rdf).

# Using BPBible under Mac #
First download and install xulrunner. Then download the pythonext extension xpi into ~/Downloads. Checkout branches/xul into a directory bpbible-xul. Now run `bpbible-xul/installer/mk_bpbibleapp.sh`. This will create BPBible.app, which should have everything needed into it except the SWORD bindings, which you will need to build for Python 2.6 (32 bit). Once you have built this, copy `Sword.py` and `_Sword.so` into BPBible.app/Content/Resources/pylib.

You can run it either by calling `open -a BPBible`, double clicking BPBible in the Finder or running BPBible.app/Content/MacOS/xulrunner (if you want a console).

The files checked out from SVN are accessible in BPBible.app/Content/Resources and can be edited as desired.