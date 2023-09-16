import numpy as np
import requests
import haversine as hs
from haversine import Unit

API_KEY = "AIzaSyC3MZiMTmpfuAhD3JCyiVtghDEJzUiQmfk"


# def get_all_distances(origins, destinations):
#     """Get distance matrix between all origins and destinations
#     Returns a matrix of distances between all origins and destinations
#     Returns None if there is an error
#     """

#     assert len(origins) == len(
#         destinations
#     ), f"origins and destinations must be the same length, got {len(origins)} and {len(destinations)}"

#     n = len(origins)

#     headers = {
#         "Content-Type": "application/json",
#         "X-Goog-Api-Key": API_KEY,
#         "X-Goog-FieldMask": "originIndex,destinationIndex,duration,distanceMeters,status,condition",
#     }
#     params = {
#         "origins": [
#             {
#                 "waypoint": {
#                     "location": {
#                         "latLng": {
#                             "latitude": orig[0],
#                             "longitude": orig[1],
#                         }
#                     }
#                 },
#                 "routeModifiers": {"avoid_ferries": True},
#             }
#             for orig in origins
#         ],
#         "destinations": [
#             {
#                 "waypoint": {
#                     "location": {
#                         "latLng": {
#                             "latitude": dst[0],
#                             "longitude": dst[1],
#                         }
#                     }
#                 }
#             }
#             for dst in destinations
#         ],
#         "travelMode": "DRIVE",
#         "routingPreference": "TRAFFIC_UNAWARE",
#     }

#     response = requests.post(
#         "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix",
#         json=params,
#         headers=headers,
#         timeout=60
#     )

#     print(response)

#     # check if response is valid
#     if response.status_code != 200:
#         print(f"status code: {response.status_code}")
#         print("Error: " + response.text)
#         return None

#     distance_matrix = np.zeros((n, n))

#     for result in response.json():
#         from_index = result["originIndex"]
#         to_index = result["destinationIndex"]
#         distance = result["distanceMeters"]

#         distance_matrix[from_index, to_index] = distance

#     distance_matrix /= 1_000 # convert to km

#     return distance_matrix


# def get_distances(origins, destinations):
#     """Get distance between every origin and distance"""

#     distance_matrix = get_all_distances(origins, destinations)

#     distances = distance_matrix.diagonal().tolist()

#     return distances


def get_single_distance(origin, destination):
    """Get distance between origin and destination"""

    distance = hs.haversine(origin, destination, unit=Unit.KILOMETERS)

    return distance

def get_all_distances(origins, destinations):
    n = len(origins)
    m = len(destinations)

    distance_matrix = np.zeros((n, m))

    for origin_index, origin in enumerate(origins):
        for destination_index, destination in enumerate(destinations):
            distance = get_single_distance(origin, destination)
            distance_matrix[origin_index, destination_index] = distance

    return distance_matrix
