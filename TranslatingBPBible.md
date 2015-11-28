# Introduction #

BPBible 0.4 adds the ability to translate the user interface. This page details how to do it.

# Details #
You need to find the abbreviation for your language. This is typically a two letter string (for example, vi for Vietnamese). This may have a country-specific postfix (for example, en\_AU would be for Australian English). Note: your language must be supported by wxWidgets.

To find the abbreviation for your language, find the line with your language in resources/iso-639-2.data. It should also have a two letter name (or if it doesn't, try using the three letter - but it may not work).

There are three files you have to edit to translate the BPBible user interface. If you are having difficulty with it, the Vietnamese locale is a good example to copy.

## Configuration file ##
The locale configuration file is where the language is registered with BPBible. This will be put at locales/_language\_abbrev_/locale.conf
It can have three sections, as seen in this example (Vietnamese):
```
[Language]
Description=Vietnamese

[SWORD]
locale=vi
abbreviations=vi_abbrev

[Text]
English=Tiếng Anh
BM test=Kiểm Tra BM
Vietnamese=Tiếng Việt
```

The SWORD section can have two items, locale and abbreviations. These correspond to the Bible book names files, but without .conf on the end. abbreviations is optional; it defaults to the value of locale.

The Text section is intended to have messages which apply to BPBible but don't have a more widespread application. At the moment, language names go in here.

## Application messages ##
The application messages makes up the bulk of the translation work.
To start, copy the messages.pot file in the locales directory and name it _language\_abbreviation_.po.
Then edit the file. [Poedit](http://www.poedit.net/) will do the editing for you; this should be very easy to use. Go Catalog > Settings to set up the language and name of the project.

There is one special string which needs special consideration: translator-credits.  Please use this to provide brief attribution to you for your translation, according to a format something like "_Language_ translation provided by _Your Name_" or something like that.

When you make changes, you should compile it to see the effects. Running bpbible with a -d flag from the command line (`bpbible.exe -d` if you are running the compiled executable; `python bpbible.py -d` otherwise) will give a debug menu. Going Debug > Locale > compile will compile the .po file; using Debug > Locale > restart will restart BPBible to work with the new locale changes.  If you don't get a Debug > Locale menu item, you can get Poedit to compile your language file for you. To do this, go to File > Preferences > Editor > Behavior, and make sure that "Automatically compile .mo file on save" is ticked.  Then save your .po file, and a .mo file will be created in the same directory.  You will need to manually move it from the locales\_language\_abbreviation_.mo directory to locales\_language\_abbreviation_\LC\_MESSAGES\messages.mo, and then after reloading the BPBible interface, it should work.

Note: if you do not have the configuration file mentioned above in place, the language will not show up in File > Languages, and it will not compile it.

### Special formatting ###
Sometimes special formatting is used in messages; this needs to be understood to translate the message properly.

`%s` is used for inserting a string into another one.
So for an example,
```
msgid "Show the %s pane"
```

Here `%s` represents the name of the pane (which is defined elsewhere). When displayed to the user, this will be substituted in. `%d` is similar; it is used for integers.

Another variation is `%(name)s`. This is used in strings which would need more than one `%s`, so that they can be reordered.

So for example from the en\_AU test locale:
```
#: swlib/pysw.py:109 swlib/pysw.py:412
msgid "There are only %(chapters)d chapters in %(book)s (given %(given)d)"
msgstr ""
"You seem to think %(book)s has %(given)d chapters, but %(book)s really has %"
"(chapters)d chapters"
```

This allows rearranging of the order of the inserted strings. You don't need to translate what is inside the brackets (and shouldn't - it will break it), as these are just the identifiers for the string. Also, make sure the letter after the bracket (s or d) is still there - it won't work without this.

`&` is used for the accelerator in menus and for controls. So `&Language` would make L the accelerator for Language - it would generally put an underline under the L, and pressing L would go to that item in the menu.

## Bible Book names ##
Lastly, there are the bible book names. You will need to produce a .conf file for the book names, and also for abbreviations if you want them. Before you make one, see if there are any [here](http://crosswire.org/svn/sword/trunk/locales.d/) for your language already. If there are any for your language, download them and use them.

Follow the steps mentioned [here](http://crosswire.org/wiki/DevTools:SWORD) to produce a file for use.

NOTE: BPBible allows dashes in booknames. After following the steps from the page above (that is, without dashes in the booknames), add extra entries of the form `BookName=Book-Name.`

For example, the Vietnamese locale has `Mathiơ=Ma-thi-ơ`

These files should go in the locales/locales.d folder

### Display Menu ###
There are items in the display menu such as Footnotes, Cross-references, etc. These are translated using the bible book name .conf file above. Under the bible booknames in the [Text](Text.md) section, you will need to add strings of the form `Footnotes=Notes of foot`

So at the end of the list of booknames you may have:
```
...
Revelation of John=The Apocalypse

Footnotes=Notes of foot
...
```

The strings you may need to translate are list below.
```
Hebrew Cantillation
Toggles Hebrew Cantillation Marks
Greek Accents
Toggles Greek Accents
Hebrew Vowel Points
Toggles Hebrew Vowel Points
Textual Variants
Switch between Textual Variants modes
Primary Reading
Secondary Reading
All Readings
```

## Directory Structure ##
The final directory structure for your language files will look something like this (where language\_abbrev is the abbreviation for your language, e.g. "zh\_CN" for Simplified Chinese, "vi" for Vietnamese, "de" for German).
  * locales
    * _language\_abbrev_.po
    * locales.d
      * _language\_abbrev__`_`_abbrev.conf
      * _language\_abbrev_.conf
    * _language\_abbrev_
      * locale.conf
      * LC\_MESSAGES
        * messages.mo

If you create a zip file with these files in it, this can be extracted onto other installations to install the language.

# History and History Toolbar #
"History" and "History Toolbar" should not be translated the same. Due to technical restrictions, translating them to the same word(s) will stop the history panel being usable.