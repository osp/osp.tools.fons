#! /usr/bin/python

"""
Merges several font files into a new font (keeping the original fonts intact).
It can take any font format that Fontforge can open: .ufo, .otf, .sfd...

Usage:
    python mergeFonts.py fonte1.ufo fonte2.ufo ...  fonte17.ufo fonte-out.ufo
"""


import fontforge
import sys


font1 = fontforge.open(sys.argv[1])
font2 = sys.argv[2]
args = len(sys.argv) - 1
print(args)


i = 0
for arg in sys.argv:
    print(i)
    if i > 1 and i < args:
        print(arg)
        font1.mergeFonts(arg)
    i += 1
        


font1.generate(sys.argv[-1])
