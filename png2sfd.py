#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob
import sys
import fontforge
#from xml.dom.minidom import parse as parseXml

# svg2ufo v0.4
# Copyleft 2014 Christoph Haag and Stéphanie Vilayphiou
#
# BASED ON:
# svg2ttf v0.1
# Copyleft 2008-2009 Ricardo Lafuente

# generates a .ufo file from a set of .svg files autotraced in its centerlines
#
# it then imports the glyph inside the original font file BASE_FONT
#
# you might also want to edit the metadata (title, license, etc.) before
# saving it, or just edit the .ufo file afterwards
#
# finally, change the LETTERS_DIR value to the folder where your .svg
# files are; they ought to be named according to their unicode value

LETTERS_DIR = "./output_gmic"
FONT_NAME = "%s" % sys.argv[1]
BLANK_FONT = "./utils/blank_unicode.sfd"
#BASE_FONT = "./base_font/%s.sfd" % FONT_NAME
#STROKE_FONT = "%s-stroke.ufo" % FONT_NAME


files = glob.glob("%s/*.png" % LETTERS_DIR)

#original = fontforge.open(BASE_FONT)
font = fontforge.open(BLANK_FONT)

def importGlyph(f, letter, char): 

    # make new glyph
    font.createMappedChar(letter)
    font.createChar(char)

    # Import outline file
    font[char].importOutlines(f)
    font[char].autoTrace()

    # Set bearings to 0
    font[char].left_side_bearing = 0
    font[char].right_side_bearing = 0

for f in files:
        letter = f.split("/")[-1].replace(".png", "")
        char = fontforge.unicodeFromName(letter)

        if char == -1:
            char = letter.replace("&#", "").replace(";", "")
            letter = fontforge.nameFromUnicode(int(char))
        print "letter: %s" % letter
        print "char: %s" % char
        importGlyph(f, letter, int(char))


# create the output ufo file
font.save("%s.sfd" % FONT_NAME)
font.generate("%s.ufo" % FONT_NAME)

