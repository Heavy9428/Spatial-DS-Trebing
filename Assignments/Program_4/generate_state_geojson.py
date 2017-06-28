import pprint as pprint
import os,sys
import json
import collections
DIRPATH = os.path.dirname(os.path.realpath(__file__))
f=open(DIRPATH+'/WorldData/state_borders.json',"r")
data = f.read()
data = json.loads(data)
all_State_Borders = []
for s in data:
    state = collections.OrderedDict()
    state['type'] = "Feature"
    state['properties'] = s
    state["geometry"]={}
    state["geometry"]["type"] = "MultiPolygon"
    state["geometry"]["coordinates"] = s.pop('borders')
    all_State_Borders.append(state)
out = open(DIRPATH + '/geo_json/generate_state.geojson',"w")
out.write(json.dumps(all_State_Borders, sort_keys=False,indent=4, separators=(',', ': ')))
out.close()