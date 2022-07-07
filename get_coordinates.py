import googlemaps
import numpy as np

KEY = "AIzaSyAbb2t4_FeLiNyd4M8JoO1lLDOe8SCrcEo"
gmaps = googlemaps.Client(key=KEY)

def get_coordinates(address):
    geocode_result = gmaps.geocode(str(address),region='WLS')
    if len(geocode_result) > 0:
        return list(geocode_result[0]['geometry']['location'].values())
    else:
        return [np.NaN, np.NaN]

# def get_rev_coordinates(long,lat):
#
#     reverse_geocode_result = gmaps.reverse_geocode((long, lat))
#     if len(reverse_geocode_result) > 0:
#         return list(reverse_geocode_result[0]['geometry']['location'].values())
#     else:
#         return [np.NaN]

