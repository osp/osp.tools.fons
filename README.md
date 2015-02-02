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

### Image

#### Get a bitmap image of characters (crop unnecessary white parts for a faster process, you can use Gimp's automatic crop for that).

![](










http://osp.kitchen/api/osp.tools.fons/raw/input/scan_bitmap.jpg)
:    A scan in bitmap

![](
http://osp.kitchen/api/osp.tools.fons/raw/input/scan_gray_1200dpi.jpg)
:    A scan in gray levels

![](
http://osp.kitchen/api/osp.tools.fons/raw/input/rasterized_ospDIN.png)
:    A rasterized font





#### Levels (have a white background, black characters but still shades of gray)

![](
http://osp.kitchen/api/osp.tools.fons/raw/documentation/01-bitmap_levels.png)



#### Small boost 

Scale up the image to something like 254% with the "Sinc (Lanczos 3)" algorithm. We choose on purpose a non-round number of scaling to break the bitmap patterns.

![](
http://osp.kitchen/api/osp.tools.fons/raw/documentation/02-scale-254percent.png)



#### Sharpen

Put the amount to the maximum and then search for the point where you don't see 

![](
http://osp.kitchen/api/osp.tools.fons/raw/documentation/03-sharpen-too_few.png)
:    Radius too small

![](
http://osp.kitchen/api/osp.tools.fons/raw/documentation/03-sharpen-ok.png)

![](
http://osp.kitchen/api/osp.tools.fons/raw/documentation/03-sharpen-too_much.png)



#### Big boost

Scale up to 403% (check on notebook or with PierreH if it's enough)

![](
http://osp.kitchen/api/osp.tools.fons/raw/documentation/04-big_boost.png)




#### Split with G'MIC "extract objects" as layers

Use the "Extract Objects" filter in G'MIC plugin in Gimp. You can play with the "Color tolerance" slider to adjust the plitting of letters.
Use "New image" as output so that it leaves your original image clean.

![](
http://osp.kitchen/api/osp.tools.fons/raw/documentation/05-gmic_extractObjects.png)





#### Export layers as .png

To export each layer into a .png file, run this script into the Filters/Python-fu/Console: 




	def save_all_layers(image, directory, name_pattern):
	    for layer in image.layers:
	        try:
	            layer.remove_mask(0)
	        except: 
	            pass
	        filename = directory + (name_pattern % layer.name)
	        raw_filename = name_pattern % layer.name
	        pdb.gimp_file_save(image, layer, filename, raw_filename)

	# This lists all opened image in Gimp
	gimp.image_list()
	
	# This should list the latest image opened which is the one we just made. Check with the command before if it correct.
	img = gimp.image_list()[0]
	
	# Change the path to where you want your images to be saved
	save_all_layers(img, "/path/to/save/directory/", "%s.png")



### Web split tool

#### Adjust the overall baseline and letter by letter when needed

#### Name each glyph/png with a text field





### Fontforge

#### Import each .png into Fontforge

#### Autotrace each glyph (arguments dans Fichier/Paramètres)

#### Rescale all glyphs according to higher letter + adjust y offset accordingly

#### Auto-width all glyphs (in the unicode view, not in glyph view)


