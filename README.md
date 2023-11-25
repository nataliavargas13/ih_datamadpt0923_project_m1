# Project-Module-1: Madrid Embassy-Bike Stations Integration
This Python script integrates information from Madrid's bike sharing stations (BiciMAD and BiciPark) and embassy/consulate locations in Madrid. The script determines the closest bike sharing stations (both BiciMAD and BiciPark) for each embassy/consulate based on their geographical coordinates.

# Prerequisites
Before running the script, ensure you have the required dependencies installed. You can install them using the following:

pip install pandas geopandas requests

# Usage
1. Data Loading:

df_bicimad = pd.read_csv('./data/bicimad_stations.csv', delimiter='\t')
df_bicipark = pd.read_csv('./data/bicipark_stations.csv', delimiter=';')
df_embajadas = pd.read_json("https://datos.madrid.es/egob/catalogo/201000-0-embajadas-consulados.json")['@graph']

2. Data Processing:

Process data to extract latitude and longitude:
df_bicipark['longitude'] = df_bicipark['geometry.coordinates'].apply(lambda x: float(x.split(',')[0].replace('[', ''))) 
df_bicipark['latitude'] = df_bicipark['geometry.coordinates'].apply(lambda x: float(x.split(',')[1].replace(']', '')))
df_bicimad['longitude'] = df_bicimad['geometry.coordinates'].apply(lambda x: float(x.split(',')[0].replace('[', ''))) 
df_bicimad['latitude'] = df_bicimad['geometry.coordinates'].apply(lambda x: float(x.split(',')[1].replace(']', '')))

3. Geospatial Operations:

Find the closest BiciMAD and BiciPark stations for each embassy:
def get_min_distance(lat_origin, long_origin, bici_points):   
	closest_station = None
	min_distance = 1000000.0
	for station in bici_points:
		distance = float(distance_meters(lat_origin, long_origin, station[0], station[1])) 
		if distance < min_distance:
			min_distance = distance 
			closest_station = station
	return closest_station

4. Results:

Results are stored in df_embajadas, including embassy type, address, and the nearest BiciMAD and BiciPark stations.


# Functions

to_mercator(lat, long): Transforms latitude/longitude data in degrees to pseudo-mercator coordinates in meters.
distance_meters(lat_start, long_start, lat_finish, long_finish): Returns the distance in meters between two latitude/longitude pairs.
get_min_distance(lat_origin, long_origin, bici_points): Finds the closest station from a list of bike station coordinates.
# Folder Structre
└── project
    ├── __trash__
    ├── .gitignore
    ├── requeriments.txt
    ├── README.md
    ├── main_script.py
    ├── notebooks
    │   ├── project1_dataframes.ipynb
    ├── modules
    │   ├── geo_calculations.py
    │  
    └── data
        ├── bicimad_stations.csv
        ├── bicipark_stations.csv

# Additional Notes

- Ensure the required data files (bicimad_stations.csv, bicipark_stations.csv) are present in the specified locations.
- The script fetches embassy/consulate data from a Madrid open data portal URL, so an internet connection is required.
- The resulting DataFrame df_embajadas contains information about embassies/consulates, their types, addresses, and the closest BiciMAD and BiciPark stations.
- Feel free to modify the code and adapt it to your specific needs.
