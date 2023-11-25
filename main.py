from shapely.geometry import Point
import geopandas as gpd
import requests
import pandas as pd
import re
import json
import math
import os       

print("Imports done!!!")

df_bicimad = pd.read_csv('./data/bicimad_stations.csv',delimiter ='\t')
print(df_bicimad.iloc[:5,:])

df_bicimad['longitude'] = df_bicimad['geometry.coordinates'].apply(lambda x: float(x.split(',')[0].replace('[', ''))) 
df_bicimad['latitude'] = df_bicimad['geometry.coordinates'].apply(lambda x: float(x.split(',')[1].replace(']', '')))
print (df_bicimad.iloc[:5,:])
print("biciMad oficial")

df_bicipark = pd.read_csv('./data/bicipark_stations.csv', delimiter = ';')
print(df_bicipark.iloc[:5,:])

df_bicipark['longitude'] = df_bicipark['geometry.coordinates'].apply(lambda x: float(x.split(',')[0].replace('[', ''))) 
df_bicipark['latitude'] = df_bicipark['geometry.coordinates'].apply(lambda x: float(x.split(',')[1].replace(']', '')))
print(df_bicipark.iloc[:5,:])
print("biciPark oficial")

url = "https://datos.madrid.es/egob/catalogo/201000-0-embajadas-consulados.json"
response = requests.get(url)
print(response.status_code)

json_data = response.json()
data = json_data['@graph']
print(data)
df_embajadas = pd.DataFrame.from_dict(data)

df_embajadas = df_embajadas[df_embajadas['location'].notna()]
df_embajadas = df_embajadas.reset_index(drop=True)
df_embajadas['longitude'] = df_embajadas['location'].apply(lambda x: x['longitude']) 
df_embajadas['latitude'] = df_embajadas['location'].apply(lambda x: x['latitude'])
df_embajadas= df_embajadas.drop('location', axis=1)
print(df_embajadas.iloc[:5,:])


def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between to latitude/longitude pair points in degrees 
    # (e.g.: Start Point -> 40.4400607 / -3.6425358 End Point -> 40.4234825 / -3.6292625)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish).values[0]

def get_min_distance(lat_origin, long_origin, bici_points):   
	closest_station = None
	min_distance = 1000000.0
	for station in bici_points:
		distance = float(distance_meters(lat_origin, long_origin, station[0], station[1])) 
		if distance < min_distance:
			min_distance = distance 
			closest_station = station
	return closest_station 

bicipark_points = df_bicipark[['latitude', 'longitude']].values.tolist()
print(bicipark_points)

df_embajadas['closest_bicipark_point'] = df_embajadas.apply(lambda embajada: get_min_distance(embajada['latitude'], embajada['longitude'], bicipark_points), axis=1) 

bicimad_points = df_bicimad[['latitude', 'longitude']].values.tolist()
print(bicimad_points)

df_embajadas['closest_bicimad_point'] = df_embajadas.apply(lambda embajada: get_min_distance(embajada['latitude'], embajada['longitude'], bicimad_points), axis=1)
print(df_embajadas)


def get_bicipark(coords_station): 
    df_station = df_bicipark[(df_bicipark['latitude'] == coords_station[0]) & (df_bicipark['longitude'] == coords_station[1])] 
    station = df_station.iloc[0]
    return station
df_embajadas['Bicipark_station_name'] = df_embajadas['closest_bicipark_point'].apply(lambda x: get_bicipark(x)['stationName'])

def get_bicimad(coords_station): 
    df_station = df_bicimad[(df_bicimad['latitude'] == coords_station[0]) & (df_bicimad['longitude'] == coords_station[1])] 
    station = df_station.iloc[0]
    return station
df_embajadas['Bicimad_station_name'] = df_embajadas['closest_bicimad_point'].apply(lambda x: get_bicimad(x)['name'])

df_embajadas['Bicipark_station_address'] = df_embajadas['closest_bicipark_point'].apply(lambda x: get_bicipark(x)['address'])
df_embajadas['Bicimad_station_address'] = df_embajadas['closest_bicimad_point'].apply(lambda x: get_bicimad(x)['address'])
print(df_embajadas)

df_embajadas['address'] = df_embajadas['address'].apply(lambda embajada: embajada['street-address'])
print(df_embajadas)

def get_type_of_place(place_name):
    place_name = place_name.lower() # name en minusculas
    if 'consulado' in place_name:
        return 'Consulado'
    else:
        return 'Embajada'
    
df_embajadas['Type of Place'] = df_embajadas['title'].apply(lambda embajada_name: get_type_of_place(embajada_name))
df_embajadas = df_embajadas[df_embajadas.columns[df_embajadas.columns.isin(['title', 'Type of Place', 'address', 'Bicipark_station_name', 'Bicipark_station_address', 'Bicimad_station_name', 'Bicimad_station_address' ])]] # botando lo que no necesito
df_embajadas = df_embajadas[['title', 'Type of Place', 'address', 'Bicipark_station_name', 'Bicipark_station_address', 'Bicimad_station_name', 'Bicimad_station_address' ]] # reordenar columnas
df_embajadas = df_embajadas.rename(columns={'title': 'Place of interest', 'address': 'Place address'})
print(df_embajadas)

