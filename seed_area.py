import os
import signal
import requests
from multiprocessing import Pool

swne = (36.346, -81.568, 39.296, -75.580)

overpass_body = """<?xml version="1.0" encoding="UTF-8"?>
<osm-script output="json" timeout="600">
  <union>
    <query type="way">
      <has-kv k="leisure" v="pitch"/>
      <has-kv k="sport" v="baseball"/>
      <bbox-query s="{}" w="{}" n="{}" e="{}"/>
    </query>
  </union>
  <union>
    <item/>
    <recurse type="down"/>
  </union>
  <print/>
</osm-script>""".format(*swne)

res = requests.post('http://overpass-api.de/api/interpreter', data=overpass_body)

nds = {}
ways = {}
for element in res.json()['elements']:
    if element['type'] == 'node':
        nds[element['id']] = (element['lon'], element['lat'])
    elif element['type'] == 'way':
        ways[element['id']] = [nds[nd] for nd in element['nodes']]

nds = {} # Save a bit of memory
print "Built {} polygons.".format(len(ways))

bboxes = {}
for way_id, ring in ways.iteritems():
    south = 90
    west = 180
    north = -90
    east = -180
    for lon, lat in ring:
        if lat < south:
            south = lat
        elif lat > north:
            north = lat

        if lon < west:
            west = lon
        elif lon > east:
            east = lon

    bboxes[way_id] = (west, north, east, south)

# buffer the bboxes by a little bit
buffer_amount = 0.0001
for way_id, bbox in bboxes.iteritems():
    buffered = (
        bbox[0] - buffer_amount,
        bbox[1] + buffer_amount,
        bbox[2] + buffer_amount,
        bbox[3] - buffer_amount,
    )
    bboxes[way_id] = buffered

ways = {} # Save a bit of memory
print "Built {} bounding boxes.".format(len(bboxes))

def fetch_diamond(way_id, bbox):
    path = 'diamond{}.jpg'.format(way_id)
    if os.path.exists(path):
        print "Skipping {} because it already exists.".format(way_id)
        return

    params = {
        'bbox': ','.join([str(b) for b in bbox]),
        'bboxSR': '4326',
        'size': '256,256',
        'format': 'jpg',
        'f': 'image',
    }

    r = requests.get('http://raster.nationalmap.gov/arcgis/rest/services/Orthoimagery/USGS_EROS_Ortho/ImageServer/exportImage', params=params, stream=True)

    if r.status_code == 200:
        # print r.url
        with open('diamond{}.jpg'.format(way_id), 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
            print "Saved image of way {} to {}.".format(way_id, f.name)
    else:
        print "Could not save way {} because {}".format(way_id, r.text)

def init_worker():
    print "Signal init"
    signal.signal(signal.SIGINT, signal.SIG_IGN)

p = Pool(5, init_worker)

try:
    for way_id, bbox in bboxes.iteritems():
        p.apply_async(fetch_diamond, (way_id, bbox,))

    print "Done inserting"
    p.close()
    p.join()
except KeyboardInterrupt:
    print "Caught KeyboardInterrupt, terminating workers"
    p.terminate()
    p.join()