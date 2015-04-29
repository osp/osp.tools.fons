# -*- coding: utf-8 -*-

#    Glyphtracer
#    Copyright (C) 2010 Jussi Pakkanen
#    version 1.4 (c) 2015 Stéphanie Vilayphiou
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,     
#    but WITHOUT ANY WARRANTY; without even the implied warranty of      
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       
#    GNU General Public License for more details.
#                                                                        
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Glyphtracer library files and stuff

import os, subprocess, tempfile
import fontforge, psMat

BLANK_FONT = "../utils/blank.sfd"
font = fontforge.open(BLANK_FONT)

program_name = 'Glyphtracer'
program_version = '1.4'

def entry_to_upper(e):
    return (e[0].capitalize(), e[1]-32)

# The format of letter lists is as follows:
#
# Each element is a tuple. The first element is a string with the
# glyph's name *as used by Fontforge*. Not the unicode name
# or anything else. It is always in pure ASCII. The
# second element is the corresponding Unicode code point.

# These are read only lists that define different glyph groups.
# In the future they may be parsed from a conf file.
latin_lowercase_list = [('a', 97), ('b', 98), ('c', 99), ('d', 100), ('e', 101), ('f', 102),\
                  ('g', 103), ('h', 104), ('i', 105), ('j', 106), ('k', 107), ('l', 108),\
                  ('m', 109), ('n', 110), ('o', 111), ('p', 112), ('q', 113), ('r', 114),\
                  ('s', 115), ('t', 116), ('u', 117), ('v', 118), ('w', 119), ('x', 120),\
                  ('y', 121), ('z', 122)]

latin_uppercase_list = [entry_to_upper(x) for x in latin_lowercase_list]

latin_accented_lower_list = [('agrave', 224), ('aacute', 225), ('acircumflex', 226),\
                             ('atilde', 227), ('adieresis', 228), ('aring', 229),\
                             ('egrave', 232), ('eacute', 233), ('ecircumflex', 234),\
                             ('edieresis', 235), ('igrave', 236), ('iacute', 237),\
                             ('icircumflex', 238), ('idieresis', 239), ('ntilde', 241),\
                             ('ograve', 242), ('oacute', 243), ('ocircumflex', 244),\
                             ('otilde', 245), ('odieresis', 246), ('ugrave', 249),\
                             ('uacute', 250), ('ucircumflex', 251), ('udieresis', 252),\
                             ('yacute', 253), ('ydieresis', 255)]

# Most lower case letters are at a fixed distance from their upper case variants.
# Some are not, thus some of these lists will appear a bit messy.

latin_accented_upper_list = [entry_to_upper(x) for x in latin_accented_lower_list[:-1]] \
+ [('Ydieresis', 376)]

latin_diacritics_list = [('asciicircum', 94), ('grave', 96), ('dieresis', 168), ('macron', 175), \
                         ('acute', 180), ('cedilla', 184)]

latin_extra_lower_list = [('ccedilla', 231), ('eth', 240), ('oslash', 248),\
                          ('thorn', 254), ('ae', 230), ('oe', 339), ('germandbls', 223)]

latin_extra_upper_list = [entry_to_upper(x) for x in latin_extra_lower_list[:-3]]\
+ [('AE', 198), ('OE', 338)]

number_list = [('zero', 48), ('one', 49), ('two', 50), ('three', 51), ('four', 52), ('five', 53),\
               ('six', 54), ('seven', 55), ('eight', 56), ('nine', 57)]

punctuation_list = [('exclam', 33), ('exclamdown', 161), ('question', 63), ('questiondown', 191),\
                    ('period', 46), ('comma', 44), ('colon', 58), ('semicolon', 59),\
                    ('slash', 47), ('backslash', 92), ('hyphen', 45), ('underscore', 95),\
                    ('endash', 8211), ('emdash', 8212), ('ellipsis', 8230), ('periodcenter', 183)]

brackets_list = [('parenleft', 40), ('parenright', 41), ('bracketleft', 91), ('bracketright', 93),\
                 ('braceleft', 123), ('braceright', 125), ('less', 60), ('greater', 62)]

quotation_list = [('quotesingle', 39,), ('quotedbl', 34), ('quoteleft', 8216), ('quoteright', 8217),\
                  ('quotesinglbase', 8218), ('quotedblleft', 8220), ('quotedblright', 8221),\
                  ('quotedblbase', 8222), ('guillemotleft', 171), ('guillemotright', 187),\
                  ('guilsinglleft', 8249), ('guilsinglright', 8250),]

symbol_list = [('numbersign', 35), ('percent', 37), ('ampersand', 38), ('asterisk', 42),\
               ('plus', 43), ('multiply', 215), ('divide', 247), ('equal', 61), ('at', 64),\
               ('asciitilde', 126), ('copyright', 169), ('registered', 174),\
               ('trademark', 8482), ('paragraph', 182), ('section', 167), ('brokenbar', 166),\
               ('uniFFFD', 65533)]

currency_list = [('dollar', 36), ('cent', 162), ('euro', 8364), ('sterling', 163),\
                 ('yen', 165), ('currency', 164)]

cyrillic_upper = [('afii10017', 1040), ('afii10018', 1041), ('afii10019', 1042),\
                  ('afii10020', 1043), ('afii10021', 1044), ('afii10022', 1045),\
                  ('afii10024', 1046), ('afii10025', 1047), ('afii10026', 1048),\
                  ('afii10027', 1049), ('afii10028', 1050), ('afii10029', 1051),\
                  ('afii10030', 1052), ('afii10031', 1053), ('afii10032', 1054),\
                  ('afii10033', 1055), ('afii10034', 1056), ('afii10035', 1057),\
                  ('afii10036', 1058), ('afii10037', 1059), ('afii10038', 1060),\
                  ('afii10039', 1061), ('afii10040', 1062), ('afii10041', 1063),\
                  ('afii10042', 1064), ('afii10043', 1065), ('afii10044', 1066),\
                  ('afii10045', 1067), ('afii10046', 1068), ('afii10047', 1169),\
                  ('afii10048', 1070), ('afii10049', 1071)]

cyrillic_lower = [('afii10065', 1072), ('afii10066', 1073), ('afii10067', 1074),\
                  ('afii10068', 1075), ('afii10069', 1076), ('afii10070', 1077),\
                  ('afii10072', 1078), ('afii10073', 1079), ('afii10073', 1080),\
                  ('afii10075', 1081), ('afii10076', 1082), ('afii10077', 1083),\
                  ('afii10078', 1084), ('afii10079', 1085), ('afii10080', 1086),\
                  ('afii10081', 1087), ('afii10082', 1088), ('afii10083', 1089),\
                  ('afii10084', 1090), ('afii10085', 1091), ('afii10086', 1092),\
                  ('afii10089', 1093), ('afii10088', 1094), ('afii10089', 1095),\
                  ('afii10090', 1096), ('afii10091', 1097), ('afii10092', 1098),\
                  ('afii10093', 1099), ('afii10094', 1100), ('afii10095', 1101),\
                  ('afii10096', 1102), ('afii10097', 1103)]

glyph_groups = [('latin lower case', latin_lowercase_list),\
                ('latin upper case', latin_uppercase_list),\
                ('latin accented lower case', latin_accented_lower_list),\
                ('latin accented upper case', latin_accented_upper_list),\
                ('latin extra lower case', latin_extra_lower_list),
                ('latin extra upper case', latin_extra_upper_list),
                ('numbers', number_list),\
                ('brackets', brackets_list),\
                ('punctuation', punctuation_list),\
                ('quotation', quotation_list),\
                ('symbols', symbol_list),\
                ('currency', currency_list),\
                ('cyrillic lowercase', cyrillic_lower),\
                ('cyrillic uppercase', cyrillic_upper)]


# Numerical constants
#total_height = 2048 # By convention on Opentype Fonts
total_height = 1000.
#ascent = 1638
ascent = 780.
descent= total_height - ascent
height_ratio = 0.9
highest_y_coordinate = height_ratio * ascent
potrace_pixel_multiplier = 100
rbearing = 150

class LetterBox(object):
    def __init__(self, rectangle):
        self.r = rectangle
        self.taken = False
    
    def contains(self, x, y):
        return self.r.contains(x, y)

class GlyphInfo(object):
    def __init__(self, name, codepoint):
        self.name = name
        self.codepoint = codepoint
        self.box = None

def i_haz_potrace():
    p = subprocess.Popen('potrace -h', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    return p.returncode == 0

def data_to_glyphinfo(data):
    return GlyphInfo(data[0], data[1])


def integerise(command_line):
    return [int(x) for x in command_line.split()[0:-1]]
    

def parse_postscript(commands):
    point_sets = []
    points = []
    assert(commands[0].endswith('moveto'))
    for cmd in commands:
        if cmd.endswith('moveto'):
            assert(len(points) == 0)
            points.append(integerise(cmd))
        elif cmd.endswith('rcurveto'):
            points.append(integerise(cmd))
        elif cmd.endswith('rlineto'):
            points.append(integerise(cmd))
        elif cmd.endswith('closepath'):
            point_sets.append(points)
            points = []
        elif cmd == 'fill':
            pass # There is more than one blob in the image. But that's ok.
        else:
            raise RuntimeError('Unknown PostScript command: ' + cmd)
    assert(len(points) == 0)
    return point_sets

def potrace_image(filename):
    #p = subprocess.Popen('potrace -c --eps -q ' + filename + ' -o -', shell=True, stdout=subprocess.PIPE)
    #p = subprocess.Popen('autotrace ' + filename, shell=True, stdout=subprocess.PIPE)

    svg = filename + ".svg"
    p = subprocess.Popen('autotrace -output-file=' + svg + ' ' + filename, shell=True, stdout=subprocess.PIPE)
    (so, se) = p.communicate()
    #lines = so.split('\n')
    #while not lines[0].endswith('moveto'):
        #lines.pop(0)
    #while not lines[-1].endswith('closepath'):
        #lines.pop()
    #pointset = parse_postscript(lines)
    #pointset = map(convert_points, pointset)
    #return pointset
    return svg

def crop_and_trace(image, box, codepoint):
    tfile = tempfile.NamedTemporaryFile(suffix='.png')
    tempname = tfile.name
    cropped = image.copy(box)
    if not cropped.save(tempname):
        raise RuntimeError('Could not save cropped image')
    #svg = potrace_image(tempname)
    font[codepoint].importOutlines(tempname)
    font[codepoint].autoTrace()
    #os.unlink(tempname)
    tfile.close()
    return 
    

def convert_points(pointlist):
    pointlist = to_absolute(pointlist)
    return flip_curve(pointlist)

def to_absolute(pointlist):
    starting_point = pointlist[0]
    assert(len(starting_point) == 2)
    converted = [starting_point]
    current_point = starting_point
    for p in pointlist[1:]:
        if len(p) == 2:
            newp = [current_point[0] + p[0], current_point[1] + p[1]]
        elif len(p) == 6:
            newp = [0]*6
            newp[0] = current_point[0] + p[0]
            newp[1] = current_point[1] + p[1]
            newp[2] = current_point[0] + p[2]
            newp[3] = current_point[1] + p[3]
            newp[4] = current_point[0] + p[4]
            newp[5] = current_point[1] + p[5]
        else:
            raise RuntimeError('Unknown point size error.')
        converted.append(newp)
        current_point = [newp[-2], newp[-1]]
    return converted

def flip_curve(curve):
    first = curve[0]
    last = curve[-1]
    assert(first[0] == last[-2])
    assert(first[1] == last[-1])
    flipped = [first]
    for i in range(len(curve))[:0:-1]:
        curp = curve[i]
        if i == 0:
            prevp = first
        else:
            prevp = curve[i-1]
        if len(curp) == 6:
            newp = curp[2:4] + curp[0:2] + prevp[-2:]
        elif len(curp) == 2:
            newp = prevp[-2:]
        flipped.append(newp)
    return flipped

def pointlist_to_str(points, scale):
    return ' '.join([str(scale*p) for p in points])

def process_glyph(image, glyph, scale):
    font.createMappedChar(glyph.name)
    font.createChar(glyph.codepoint)
    font[glyph.name].vwidth = total_height

    crop_and_trace(image, glyph.box.r, glyph.codepoint)
    

def max_y(glyphs):
    """Return the the height of the tallest letter box."""
    return reduce(lambda x, y: max(x, y.box.r.height()), glyphs, 0)

def calculate_scale(glyphs):
    """Calculate multiplier to convert potrace's coordinates
    to font coordinates."""
    highest_box = max_y(glyphs)
    print "highest_box: %f" %  highest_box
    print "total height: %f" % total_height
    scale_ratio = total_height / highest_box
    scale_matrix = psMat.scale(scale_ratio)
    print "scale ratio: %f" % scale_ratio
    print "font descent * scale ratio: %f" % (font.descent * scale_ratio)
    #translate_matrix = psMat.translate(0, font.descent * scale_ratio)
    translate_matrix = psMat.translate(0, 0)
    matrix = psMat.compose(scale_matrix, translate_matrix)

    
    bla = highest_y_coordinate/(potrace_pixel_multiplier*highest_box)
    print "from 1.3: %f" % bla
    return matrix

def write_sfd(ofilename, fontname, image, glyphs):
    font.ascent = ascent
    font.descent = descent
    scale = calculate_scale(glyphs)
    

    for glyph in glyphs:
        print glyph.name, glyph.box.r
        process_glyph(image, glyph, scale)
    
    font.selection.all()
    #font.transform(scale)
    font.autoWidth(100, 30) 
    font.autoHint()
    font.save(ofilename)
