mongo world_data --eval "db.dropDatabase()"
mongoimport --db world_data --collection airports --type json --file C:\Users\Trebi\Desktop\Spatial-DS-Trebing\Assignments\Program_5\geojson\airports.geojson --jsonArray
mongoimport --db world_data --collection countries --type json --file C:\Users\Trebi\Desktop\Spatial-DS-Trebing\Assignments\Program_5\geojson\countries.geojson --jsonArray
mongoimport --db world_data --collection meteorites --type json --file C:\Users\Trebi\Desktop\Spatial-DS-Trebing\Assignments\Program_5\geojson\meteorite.geojson --jsonArray
mongoimport --db world_data --collection volcanos --type json --file C:\Users\Trebi\Desktop\Spatial-DS-Trebing\Assignments\Program_5\geojson\volcanos.geojson --jsonArray
mongoimport --db world_data --collection earthquakes --type json --file C:\Users\Trebi\Desktop\Spatial-DS-Trebing\Assignments\Program_5\geojson\earthquakes.geojson --jsonArray
mongoimport --db world_data --collection cities --type json --file C:\Users\Trebi\Desktop\Spatial-DS-Trebing\Assignments\Program_5\geojson\world_cities.geojson --jsonArray
mongoimport --db world_data --collection states --type json --file C:\Users\Trebi\Desktop\Spatial-DS-Trebing\Assignments\Program_5\geojson\state_borders.geojson --jsonArray