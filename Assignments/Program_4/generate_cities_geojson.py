import pprint as pprint
import os,sys
import json
import collections
DIRPATH = os.path.dirname(os.path.realpath(__file__))
f=open(DIRPATH+'/WorldData/world_cities_large.json',"r")
data = f.read()
data = json.loads(data)
all_cities =[]
for k,c in data.items():
    cities = collections.OrderedDict()
    for item in c:
        if (len(all_cities)<1000):
            cities['type'] = "Feature"
            cities['properties'] = item
            lat1 = item['lat']
            lon1 = item['lon']
            lat = float(lat1)
            lon = float(lon1)
            del cities['properties']['lat']
            del cities['properties']['lon']
            cities["geometry"] = {}
            cities["geometry"]["type"]="Point"
            cities["geometry"]["coordinates"] = [
                lon,
                lat
                ]
            all_cities.append(cities)
out = open(DIRPATH + '/geo_json/generate_cities.geojson',"w")
out.write(json.dumps(all_cities, sort_keys=False,indent=4, separators=(',', ': ')))
out.close()
