detect-baseball-diamonds
========================

Various attempts at scanning aerial imagery to detect baseball diamonds.

## Neural network

Based on a [friend's suggestion](https://twitter.com/justinvf/status/487707114001821696), I'm going to try training a neural network to detect baseball diamonds from aerial imagery.

### Finding source images

To start with, I wrote a script that finds baseball diamonds in OSM and then extracts them from the NationalMap's [Orthoimagery ImageServer](http://raster.nationalmap.gov/arcgis/rest/services/Orthoimagery/USGS_EROS_Ortho/ImageServer/exportImage?format=jpeg&bboxSR=4326&bbox=-93.6080387%2C44.8931306%2C-93.607018%2C44.8923663&f=html&size=256%2C256). The [`seed_area.py`](seed_area.py) script is the start of this.

Once I grabbed a suitable number of images (a small area around Minneapolis turned up ~1000 images), I got tired of looking through them one-by-one and used ImageMagick's [montage tool](http://www.imagemagick.org/script/montage.php) to put them together into a pretty neat image like this:

`montage diamond*.jpg montage.jpg`

Resulting in:

![https://www.flickr.com/photos/yellowbkpk/14457773107/sizes/o/](https://farm6.staticflickr.com/5491/14457773107_0659643181.jpg)
