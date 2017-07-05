Query 1 : Finding Features 
Note: Not fully working yet issue with points.

How to Run:
From the Command line after you have changed to the location the program is stored in use
python Query1.py [start] [end] [radius], a Example of this would be python Query1.py DFW HOU 500


In theory this will find a flight path from dfw to houston (short i know) and find any features that are by it


Query 2 :Nearest Feature

How to Run: This excepts two diffrent command line commands, one where you give it all the information and click on the map to determine
            Your Lon, Lat and will give you all the features in a radius that is contained in their feature list
            The other is where you just give it a radius and it finds multiple features.
            
 python Query2.py [feature] [field] [field value] [min/max] [max results] [radius]
 feature is either Volcano, Meteorites, Earthquakes
 field some field in the properties section of the geojson files, example wouldd be altitude
 field value some value we want to compare the field to, example altitude of 3000
 min or max will check for any value that is greather then of field value or less then so if max the 3000 and under will print
 radius circle distance in miles
 
 python Query2.py [radius]
 By just giving it a radius will get all three of the above feature's and display them to the screen after you click on a point on the map
 
 Query 3 Clustering
 Known issues : Only runs with volcanos
 Using dbscan it calculates the minimum number of points to print out a bounding box for a feature set on the map
 python query3.py [feature] [min_pts] [eps]
 feature- same as query 2 
 min_pts the minimum amounts of points needed to make a cluster
 eps our dbscan distance
 python query3.py volcanos 3 5
 
 Other information:
 Theses programs utilize MongoDB and a local server must be running to correctly run the programs
 The db is called world_data
 The three main collections names are called Volcanos Earthquakes and Meteorites
 
