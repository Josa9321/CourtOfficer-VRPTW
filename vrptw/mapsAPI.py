from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import requests
import numpy as np

from time import sleep
from geopy.geocoders import Nominatim

def get_geodata_osrm(addresses_set, duplicate_base=True):
    coordinates = _get_geodata_addresses(addresses_set)
    times, distances = _get_geodata_distances_and_times(coordinates)
    if duplicate_base:
        times = _duplicate_base(times)
        distances = _duplicate_base(distances)
    return times, distances

def _get_geodata_addresses(addresses_set, retries=3):
    geolocator = Nominatim(user_agent='courtOfficer')
    coords = []

    for address in addresses_set:
        for attempt in range(retries):
            sleep(3)
            try:
                location = geolocator.geocode(address)
                if location is None:
                    print(f'Address not found: {address}')
                else:
                    coords.append((location.longitude, location.latitude))

                break
            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                print(f'Retry {attempt+1} for address {address}... \n\t{e}')

    return coords

def _get_geodata_distances_and_times(coords):
    coord_str = ';'.join([f'{lon},{lat}' for lon, lat in coords])
    try:
        response = requests.post(f'https://router.project-osrm.org/table/v1/driving/{coord_str}?annotations=distance,duration')
        response.raise_for_status()
        geo_data = response.json()
        return (np.array(geo_data['durations']), np.array(geo_data['distances']))
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return (np.array([]), np.array([]))

def _duplicate_base(matrix: np.ndarray):
    new_row = matrix[0].copy()
    aux = np.vstack((matrix, new_row))
    new_col = aux[:, 0].reshape(-1, 1)
    result = np.hstack((aux, new_col)) 
    return result

def get_geodata_google(addresses_set, api_key):
    url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"

    waypoints = [{"waypoint": {"address": addr}} for addr in addresses_set]

    payload = {
        "origins": waypoints,
        "destinations": waypoints,
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE"
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "originIndex,destinationIndex,duration,distanceMeters,status,condition"
    }

    response = requests.post(url, json=payload, headers=headers)
    distance_matrix = np.zeros((len(addresses_set)+1, len(addresses_set)+1))
    time_matrix = np.zeros((len(addresses_set)+1, len(addresses_set)+1))

    if response.status_code == 200:
        results = response.json()
        for element in results:
            origin_idx = element['originIndex']
            destination_idx = element['destinationIndex']
            distance_matrix[origin_idx][destination_idx] = element.get('distanceMeters', 0) / 1000
            time_matrix[origin_idx][destination_idx] = float(element.get('duration', '0s')[:-1])

        for i in range(len(addresses_set)):
            time_matrix[-1][i] = time_matrix[0][i]
            distance_matrix[-1][i] = distance_matrix[0][i]

            time_matrix[i][-1] = time_matrix[i][0]
            distance_matrix[i][-1] = distance_matrix[i][0]
    else:
        print(f"Error {response.status_code}: {response.text}")

    return distance_matrix, time_matrix
