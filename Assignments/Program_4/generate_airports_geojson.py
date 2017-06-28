import pprint as pprint
import os,sys
import json
import collections
DIRPATH = os.path.dirname(os.path.realpath(__file__))
f = open(DIRPATH +'/WorldData/airports.json',"r")
data = f.read()
data=json.loads(data)
all_airports = []
for k,v in data.items():
    if(len(all_airports)<1000):
        gj = collections.OrderedDict()
        gj['type'] = "Feature"
        gj['properties'] = v
        lat = v['lat']
        lon = v['lon']
        del gj['properties']['lat']
        del gj['properties']['lon']
        gj["geometry"] = {}
        gj["geometry"]["type"]="Point"
        gj["geometry"]["coordinates"] = [
            lon,
            lat
            ]
        all_airports.append(gj)
out = open(DIRPATH + '/geo_json/generate_airports.geojson',"w")
out.write(json.dumps(all_airports, sort_keys=False,indent=4, separators=(',', ': ')))
out.close()