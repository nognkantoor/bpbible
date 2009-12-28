#!/bin/bash
mkdir -p BPBible.app/Contents
mkdir BPBible.app/Contents/Frameworks
mkdir BPBible.app/Contents/MacOS
cd BPBible.app/Contents
#unzip ~/Downloads/pyxulrunner-template.zip
#mv pyxpcom_gui_app Resources
cp -r /Library/Frameworks/XUL.framework/Versions/Current Frameworks/XUL.framework
cd Frameworks/XUL.framework
unzip ~/Downloads/pythonext-2.6.2.20091013-Darwin_universal.xpi

cd ../..
# part two
cp Frameworks/XUL.framework/xulrunner MacOS/xulrunner
#cp installer/MacOSX/Info.plist .

# grab bpbible into here
cp -r ../../bpbible-xul Resources
cp Resources/installer/Info.plist .
