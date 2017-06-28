import pprint as pprint
import os,sys
import json
import collections
DIRPATH = os.path.dirname(os.path.realpath(__file__))
f=open(DIRPATH+'/WorldData/earthquakes-1960-2017.json',"r")
data = f.read()
data = json.loads(data)
all_quakes=[]
i = 0
for k,c in data.items():
    quakes = collections.OrderedDict()
    for item in c:
        if i < 1000:
            quakes['type'] = "Feature"
            quakes['properties'] = item
            lat = item['geometry']['coordinates'][0]
            lon = item['geometry']['coordinates'][1]
            del quakes['properties']['geometry']
            quakes['geometry'] = {}
            quakes['geometry']['type']="Point"
            quakes['geometry']['coordinates']=[
                lon,
                lat
            ]
        all_quakes.append(quakes)
        i = i +1
out = open(DIRPATH + '/geo_json/generate_earthquake.geojson',"w")
out.write(json.dumps(all_quakes, sort_keys=False,indent=4, separators=(',', ': ')))
out.close()