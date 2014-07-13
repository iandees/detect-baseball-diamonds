detect-baseball-diamonds
========================

Various attempts at scanning aerial imagery to detect baseball diamonds.

## Neural network

Based on a [friend's suggestion](https://twitter.com/justinvf/status/487707114001821696), I'm going to try training a neural network to detect baseball diamonds from aerial imagery.

### Finding source images

To start with, I wrote a script that finds baseball diamonds in OSM and then extracts them from the NationalMap's [Orthoimagery ImageServer](http://raster.nationalmap.gov/arcgis/rest/services/Orthoimagery/USGS_EROS_Ortho/ImageServer/exportImage?format=jpeg&bboxSR=4326&bbox=-93.6080387%2C44.8931306%2C-93.607018%2C44.8923663&f=html&size=256%2C256). The [`seed_area.py`](seed_area.py) script is the start of this.

