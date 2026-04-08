import requests
import numpy as np

def get_distances_and_time_matrix(addresses_set, api_key):
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
