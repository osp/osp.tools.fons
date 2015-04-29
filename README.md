FONS
====
A tool to make fonts out of bitmap images.

Tools needed
------------
- Gimp
- Gimp G'MIC plugin
- Autotrace
- Fontforge with Autotrace



Process
-------

### Preparing the image


#### Get a bitmap image of characters (crop unnecessary white parts for a faster process, you can use Gimp's automatic crop for that).

![](http://osp.kitchen/api/osp.tools.fons/raw/input/scan_bitmap.jpg)
:    A scan in bitmap

![](http://osp.kitchen/api/osp.tools.fons/raw/input/scan_gray_1200dpi.jpg)
:    A scan in gray levels

![](http://osp.kitchen/api/osp.tools.fons/raw/input/characters-table.svg)
:    A rasterized font: to typeset it, you can use the template characters-table.svg in the `/input/` folder






#### Levels (have a white background, black characters but still shades of gray)

![](http://osp.kitchen/api/osp.tools.fons/raw/documentation/01-bitmap_levels.png)



#### Small boost 

Scale up the image to something like 254% with the "Sinc (Lanczos 3)" algorithm. We choose on purpose a non-round number of scaling to break the bitmap patterns.

![](http://osp.kitchen/api/osp.tools.fons/raw/documentation/02-scale-254percent.png)



#### Sharpen with "Unsharp mask"

Put the amount to the maximum and then search for the point where you don't see 

![bad](http://osp.kitchen/api/osp.tools.fons/raw/documentation/03-sharpen-too_few.png)
:    Radius too small

![ok](http://osp.kitchen/api/osp.tools.fons/raw/documentation/03-sharpen-ok.png)

![bad](http://osp.kitchen/api/osp.tools.fons/raw/documentation/03-sharpen-too_much.png)



#### Big boost

Scale up to 403% (check on notebook or with PierreH if it's enough)

![](http://osp.kitchen/api/osp.tools.fons/raw/documentation/04-big_boost.png)



#### Threshold


![bad](http://osp.kitchen/api/osp.tools.fons/raw/documentation/05-threshold-bad.png)


![ok](http://osp.kitchen/api/osp.tools.fons/raw/documentation/05-threshold-ok.png)


#### Baseline

When importing a bitmap, Fontforge scales up/down the bitmap so that it fits into the glyph box. If we use GlyphTracer 1.4, this ends up with different scales of glyphs. In order to prevent this, we can put a black rectangle of the height of the maximum ascendant and maximum descendant.

![baseline](http://osp.kitchen/api/osp.tools.fons/raw/documentation/06-baseline.png)


#### Bitmap

- Change the color mode to Indexed mode with 1 black/white bit.
- Save as a .bmp file.


### GlyphTracer

- To launch GlyphTracer, there are two possibilities:
    - from your file manager, double-click on the file `glyphtracer` inside the `glyphtracer-1.4` folder
    - from the terminal, go to the `glyphtracer-1.4` folder and run `./glyphtracer`. This will let you know more output in case of errors.
- Feed in the .bmp image in 1 bit (otherwise it will complain).
- For each given glyph, click on the letter you want to use.
- Change the characters subset in the bottom left dropdown menu to select more glyphs.



### Post-production

#### Merging fonts

In case you want to complete an existing font, you can use the script `mergeFonts.py`.

    python mergeFonts.py fonte1.ufo fonte2.ufo ...  fonte17.ufo fonte-out.ufo


#### Metrics and kernings

A big part of type design is about managing the white space around the letters (metrics) and exceptions for specific couples of letters (kernings).

- For the metrics, we make an auto-spacing while generating the .sfd file with GlyphTracer.
- For the kernings, you can try the tool (Kernagic)[https://github.com/hodefoting/kernagic].

But if you want to get back metric and kerning data from an existing font, you can use the script `mergeSpacing.py`. It can be any font format than `.otf`.

   python mergeSpacing.py font.otf original-font.otf spaced-font.otf



Troubleshooting
---------------

### My image is too big to manipulate it.
Split it into several images and generate several .sfd files. Then you can merge the fonts with the script `mergeFonts.py`.


### From the terminal, I have the following error:

    File "./glyphtracer", line 415
        except Exception, e:
                          ^
    SyntaxError: invalid syntax

This means your fontforge runs with python3, whereas the majority of installs run still with python2. I didn't find a convenient way yet to maintain both versions at the same time. Let me know and I send you the version for python3 which I use.
