﻿#summary Searching in BPBible
#labels Featured,User-Documentation

# Introduction #

BPBible provides its own searching technology, allowing cross-verse searches.
It also allows slower searches, using the SWORD library.

# Indexed Searches #
To run the cross verse search, you will have to index the book beforehand. If you do not index it, you will be restricted to the SWORD searches, which are much slower and do not provide cross-verse searching.

## Wild cards ##
You can use wild cards in your multi word and phrase searches to make your searches more flexible.

Wild cards allowed:
  * `+` matches at least one letter
  * `?` matches any letter
  * `*` matches zero or more letters
  * `[letters]` will match one of the letters inside the square brackets
  * `\d` will match a single digit. This will match `1` but not `one`
  * `(word, or, word2)` will match one of the words in the brackets

Wild card examples:
  * `foot+` matches any word beginning with foot except foot
  * `b?ll` wil match any of ball, bill, bell or bull
  * `bapti*` matches any word starting with bapti, including baptist and baptize
  * `b[ai]ll` will match either ball or bill
  * `12\d` will match 120, 121, ..., 129, but will not match 1234
  * `(humble, humility)` will find all references which have the words humble in, as well as all those with humility in.
  * `"Son of (God, Man)"` will match the phrase `Son of God`, as well as the phrase `Son of Man`

## Multi Word Searches ##
Multi Word search will search for words within a certain distance of each other (approximately the proximity in words). For example, searching for `God love` will find all verses where God is close to love (either before it or after it).

The default value for proximity is 15 words - this means that for this
example, God will be within about 15 words or love. It is also possible to
search within a given number of verses/entries, by selecting Verses or entries
in the proximity options. Searching within 1 verse will return results that
are all within a single verse. This gives the same behaviour as many other
Bible software products.

### Stemming ###
Multi-word searches will perform stemming. Stemming refers to the process of
removing the ends of words, to find similar words. For example, searching for
`test` will now return results for tests, tested and testing as well. If you
want to search for the exact word, put a plus in front of the word (for
example, `+test`).

Stemming is not performed when the case-sensitive flag is on.

## Phrase searches ##
Phrase search will search for the given phrase. For example, searching for `"Son of man"` will match all verses where the three words Son of man occur in a phrase.

## Regular Expression Searches ##
Regular expression searches allow you to apply advanced pattern matching to your searches. For a guide on how to use these regular expressions, look at http://docs.python.org/lib/re-syntax.html

Also, all punctuation has been removed, so searches on punctuation will not work.

Example:
`/\bSon of (Man|God)\b/`

## Field Searches ##
Field searches allow you to search for certain data.
There are three different fields currently supported - Strong's numbers,
morphology and verse references. You can easily search for them by right
clicking on one of the links for that field and selecting search.

### Strong's numbers ###
If you want to find where Strong's number (for example, G3692) occurs in a
book, search for `strongs:G3962`.

### Morphology ###
If you want to find where a given morphological tag is used
(for example, Robinson code V-2AAO-3S) in a book, search for
`morph:robinson:V-2AAO-3S`.

### Verse References ###
If you want to find where a given verse is referenced in a book (for example,
Matthew 6:11), search for `ref:"Matthew 6:11"`

This will return results which have Matthew 6:11 in them, including ones which
have a range which include Matthew 6:11. For example, if there was a reference
to Matthew 6:9-13, that would be shown. A range of references can be specified
(for example, searching for `ref:"Matthew 6"` would return all places where a
book has references to anywhere in Matthew 6)

## Combined ##
You can combine the different types of search. This allows you to mix multi-word, phrase and regular expression searches.

To use multi-word search just put the words together, like in a multi-word search.
e.g. `God love`

To search for a phrase, put double quotes around your search.
e.g. `"Son of man"`

To search for a regular expression, put forward slashes around your search.
e.g. `/\bSon of (Man|God)\b/`

These can be combined:
`Jesus /\bSon of (Man|God)\b/ "said to them"` will match Jesus near one of the phrases "Son of Man" or "Son of God", as long as it is also near the phrase "said to them"

To exclude certain words, phrases or regular expressions, put a `-` in front of them.
For example, `grace -mercy` will find verses that have grace in, but don't have mercy.

`Jesus -/\bSon of (Man|God)\b/` will find verses which have Jesus in, but don't have "Son of Man" or "Son of God" in them.

## Cross Verse Searching Example ##
Indexed search supports matches across verse boundaries. One search term can be in one verse, and another in the next.

Fill in the dialog as follows:
  * Search Type: Combined
  * Find: `"Fruit of the spirit" self-control`

Now click Search.
This will give 1 reference, Galatians 5:22-23, as expected.

## Keypad ##
If you have an indexed search, you will see a keyboard button next to the
search text. Pressing this will give a list of the letters used in this book.
You can then click on the letters to type words in.

# Unindexed searches #
It is possible to search without first indexing the Bible you are trying to search. These searches are known as SWORD searches, and are much slower, and do not search across verse boundaries. These searches allow multiword, phrase and regular expression search, but not search on fields.