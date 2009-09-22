# adapted from http://jenda.krynicky.cz/perl/GUIscripts.html
# use this as follows:
# copy xulrunner/xulrunner-stub.exe bpbible-console.exe
# python scripts/consolize_exe.py bpbible-console.exe
import sys
import struct
d = open(sys.argv[1], "r+b")
record = d.read(64)
print len(record)
items = struct.unpack("<H58bL", record)
magic, offset = items[0], items[-1]
if magic != 0x5a4d:
	sys.exit("Not a proper .exe file")

d.seek(offset)
items = struct.unpack("<L16bH", d.read(22))
magic, size = items[0], items[-1]
if magic != 0x4550:
	sys.exit("PE header not there?")

if size != 224:
	sys.exit("Wrong optional header length?")

d.seek(offset + 24 + 68)
#print struct.unpack("H", d.read(2))
d.write(struct.pack("H", 3))
