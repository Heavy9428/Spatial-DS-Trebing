import pprint as pprint
import os,sys
import json
import collections
DIRPATH = os.path.dirname(os.path.realpath(__file__))

f=open(DIRPATH+'/WorldData/world_volcanos.json',"r")
data = f.read()
data = json.loads(data)
all_vulcan =[]
i = 0
for v in data:
    if i < 1000:
        vulcan = collections.OrderedDict()
        vulcan['type'] = "Feature"
        vulcan['properties'] = v
        lat1 = v['Lat']
        if lat1 == "":
            lat = 999999999
            lon = 999999999
        else:
            lon1 = v['Lon']
            lat = float(lat1)
            lon = float(lon1)
        del vulcan['properties']['Lat']
        del vulcan['properties']['Lon']
        vulcan["geometry"]={}
        vulcan["geometry"]["type"]="Point"
        vulcan["geometry"]["coordinates"] = [
            lon,
            lat
        ]
        all_vulcan.append(vulcan)
out = open(DIRPATH + '/geo_json/generate_vulcanos.geojson',"w")
out.write(json.dumps(all_vulcan, sort_keys=False,indent=4, separators=(',', ': ')))
out.close()