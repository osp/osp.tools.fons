#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob
import sys
import fontforge, psMat
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


#def get_alt(code, name):
    #instances = 8
    #alt = ()
    #char = unichr(code)
    #if char.islower():
        #instances = 32
    #elif char.isupper():
        #instances = 16
    #for i in range(1,instances):
        #alt = alt + ("%s.%d" %(name, i),)
    #return alt

def autokern(font):
    print "Auto kerning..."
    font.addLookup(
        "Kern lookup",
        "gpos_pair",
        (),
        (
            ('kern',
                (
                    ('DFLT', ('dflt',)),
                    ('latn', ('dflt',))
                )
            ),
        ))
    font.addLookupSubtable("Kern lookup", "Kern subtable")
    list1 = ["A", "V", "a", "v", "W", "w", "o", "O", "T", "L", "Y", "l", "y", "r", "e"]
    list2 = [ ]
    #for a in list1:
        #list2.append(a)
        #alt = get_alt(font.createMappedChar(a).unicode, a)
        #for b in alt:
            #list2.append(b)
    list1 = list2
    font.autoKern("Kern subtable", 150, list1, list2, onlyCloser=True)

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
    # AutoWidth: separation, MinBearing, MaxBearing


for f in files:
        letter = f.split("/")[-1].replace(".png", "")
        char = fontforge.unicodeFromName(letter)

        if char == -1:
            char = letter.replace("&#", "").replace(";", "")
            letter = fontforge.nameFromUnicode(int(char))
        print "letter: %s" % letter
        print "char: %s" % char
        importGlyph(f, letter, int(char))


bottom = font["h"].boundingBox()[1]
top = font["h"].boundingBox()[3]

height = top - bottom
scale_ratio = 780 / height
scale_matrix = psMat.scale(scale_ratio)
translate_matrix = psMat.translate(0, font.descent * scale_ratio)
matrix = psMat.compose(scale_matrix, translate_matrix)
print matrix

# Series of transformations on all glyphs
font.selection.all()
font.transform(matrix)
font.autoWidth(100, 30) 
font.autoHint()

autokern(font)


font.descent = 216
font.ascent = 780

# create the output ufo file
font.save("%s.sfd" % FONT_NAME)
font.generate("%s.ufo" % FONT_NAME)


