### PyXPCOM turns optimization off.
### This turns it on back on ASAP
import ctypes

try:
	opt_flag = ctypes.c_int.in_dll(ctypes.pythonapi, "Py_OptimizeFlag")
except Exception, e:
	# when we re-register (e.g. changing build id), we seem to end up here
	# this is somewhat curious
	print "EXCEPTED", e
	opt_flag = None

import __builtin__
old_import = __builtin__.__import__

def defer_unoptimize(name, globals={}, locals={}, fromlist=[], level=-1):
	# if it is off, this was probably XPCOM we just imported
	if opt_flag and opt_flag.value != 0:
		opt_flag.value = 0

		# I don't think we need to keep on coming back here, so set it back
		__builtin__.__import__ = old_import

	return old_import(name, globals, locals, fromlist, level)

__builtin__.__import__ = defer_unoptimize
	
