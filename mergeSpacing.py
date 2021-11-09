#! /usr/bin/python

"""
Merges the spacing information from one base font to your font and produces a new font (keeping the original fonts intact).
It can take any font format that Fontforge can open: .ufo, .otf, .sfd...

Usage:
    python mergeSpacing.py MyFont.ufo BaseFont.ufo SpacedFont.ufo
"""


import fontforge
import sys


font = fontforge.open(sys.argv[1])
original = fontforge.open(sys.argv[2])


# MERGE SPACINGS
for g in font.glyphs():
    try:
        char = g.glyphname
        print(char)
        # Gets original font bearings
        left = original[char].left_side_bearing
        right = original[char].right_side_bearing

        # Sets current bearings to 0
        font[char].left_side_bearing = 0
        font[char].right_side_bearing = 0

        # Gets drawing width
        width = font[char].width

        # Resize the width with original bearings
        font[char].width = left + width + right
        font[char].left_side_bearing = left
        font[char].right_side_bearing = right
    except:
        pass


# EXPORT ORIGINAL FONT AS PFA/AFM TO GET OPENTYPE FEATURES FROM AN AFM FILE
afm = original.generate("%s.pfa" % sys.argv[2])

# MERGE OPENTYPE FEATURES (including kernings)
font.mergeFeature("%s.afm" % sys.argv[2])
#font.mergeLookups(original)
#font.mergeLookupSubtables(original)

 
font.generate(sys.argv[3])
