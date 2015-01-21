FONS
====
A tool to make fonts out of bitmap images.

Process
-------

### Image

#### Get a bitmap image of characters (crop unnecessary white parts for a faster process, you can use Gimp's automatic crop for that).

![](http://git.constantvzw.org/?p=osp.tools.fons.git;a=blob_plain;f=input/scan_bitmap.jpg)
:    A scan in bitmap

![](http://git.constantvzw.org/?p=osp.tools.fons.git;a=blob_plain;f=input/scan_gray_1200dpi.jpg)
:    A scan in gray levels

![](http://git.constantvzw.org/?p=osp.tools.fons.git;a=blob_plain;f=input/rasterized_ospDIN.png)
:    A rasterized font





#### Levels (have a white background, black characters but still shades of gray)

![](http://git.constantvzw.org/?p=osp.tools.fons.git;a=blob_plain;f=documentation/01-bitmap_levels.png)



#### Small boost 

Scale up the image to something like 254% with the "Sinc (Lanczos 3)" algorithm. We choose on purpose a non-round number of scaling to break the bitmap patterns.

![](http://git.constantvzw.org/?p=osp.tools.fons.git;a=blob_plain;f=documentation/02-scale-254percent.png)



#### Sharpen

Put the amount to the maximum and then search for the point where you don't see 

![](http://git.constantvzw.org/?p=osp.tools.fons.git;a=blob_plain;f=documentation/03-sharpen-too_few.png)
:    Radius too small

![](http://git.constantvzw.org/?p=osp.tools.fons.git;a=blob_plain;f=documentation/03-sharpen-ok.png)

![](http://git.constantvzw.org/?p=osp.tools.fons.git;a=blob_plain;f=documentation/03-sharpen-too_much.png)



#### Big boost


#### Split with G'MIC "extract objects" as layers

#### Export layers as .png




### Web split tool

#### Adjust the overall baseline and letter by letter when needed

#### Name each glyph/png with a text field





### Fontforge

#### Import each .png into Fontforge

#### Autotrace each glyph (arguments dans Fichier/Paramètres)

#### Rescale all glyphs according to higher letter + adjust y offset accordingly

#### Auto-width all glyphs (in the unicode view, not in glyph view)


