# Introduction #
There are two ways to run BPBible:
  1. Run binaries under Windows
  1. Run from source

Under Windows, you probably want to run the binaries. Under Linux, you need to run from source. Once you have run it, you may want to [install books](InstallingBooks.md).

# Running binaries under Windows #
To run the binaries under Windows, download the BPBible installer (`bpbible-x.x-setup.exe`). For the installer, run it and follow the prompts. Now run bpbible.exe in the application directory, or use the Start Menu, Desktop and Quick Launch shortcuts, if you chose to create them.

# Running from source #
## Dependencies ##
To build from source, you will need to have the following:
  1. wxPython 2.8 (preferably at least 2.8.12)
  1. Python 2.6 or 2.7 (though older versions may work - the Windows build currently uses 2.6.6)
  1. SWORD 1.6.0
  1. PyStemmer (BPBible will work without this, but stemming will not be supported when searching).
  1. wxWebConnect and the XULRunner 1.9.2 binaries for your platform.
  1. Windows, Linux or Mac

BPBible works mostly under Mac. Certain features, like the quickselectors, do not appear correctly. Also, users must compile it themselves - there is no binary distribution yet.

## Using the binaries under Linux ##

You can try downloading the bindings at http://sites.google.com/site/jmmorganswordmodules/Home/sword-1.6-bindings.tar.bz2 (for Python 2.6, 32-bit).  Extract the bindings into your Python site dir.

## Building the SWIG bindings ##
The SWIG bindings are located in the bindings/swig directory of the SWORD
source code. Instructions on how to build are supplied in the README file in
that directory.

If you want to install them under Linux, the procedure will probably be:
```
<change into the bindings/swig directory of the SWORD source code>
cd package
./configure
make pythonswig
make python_make
cd python
python setup.py install
```

If you try running BPBible and it gives errors about a missing symbol
uncompress, you need to modify the setup.py. Replace the line
```
libraries=[('sword')],
```

with
```
libraries=['sword', 'z', 'curl'],
```

Then run `python setup.py install` again.

## Running BPBible ##
Once the SWIG bindings are installed, unzip the BPBible source. From there, run `python bpbible.py`.