import numpy as np
import json

class Instance:
    def __init__(self, time_matrix: np.ndarray, distance_matrix: np.ndarray, time_point: np.ndarray,
                 time_window_a: np.ndarray, time_window_b: np.ndarray, addresses_set: list):
        self.n = time_matrix.shape[0]
        assert time_window_a.shape == (self.n,)
        assert time_window_b.shape == (self.n,)
        assert time_point.shape == (self.n,)
        assert time_matrix.shape == (self.n, self.n)
        assert distance_matrix.shape == (self.n, self.n)

        self.time_matrix = time_matrix
        self.time_point = time_point
        self.distance_matrix = distance_matrix
        self.time_window_a = time_window_a
        self.time_window_b = time_window_b
        self.addresses_set = addresses_set

        self.V = np.array(range(self.time_matrix.shape[0]))
        self.N = np.array(range(1, self.time_matrix.shape[0]-1))
        self.K = np.array([0, 1, 2, 3, 4])

        self.time_dict = self._convert_matrix_to_dict(time_matrix)
        self.distance_dict = self._convert_matrix_to_dict(distance_matrix)

    def _convert_matrix_to_dict(self, matrix):
        this_dict = {}
        for i in self.V:
            for j in self.V:
                this_dict[i, j] = matrix[i][j]

        return this_dict

    def print(self):
        print("Time matrix:")
        self._print_matrix()
        print("\nNode Data")
        self._print_node_data()

    def _print_node_data(self):
        print(f"{"Node":>6} {"a":>7} {"b":>7} {"Service":>7}")
        for i in self.V:
            print(f"{i:>6} {self.time_window_a[i]:>7.2f} {self.time_window_b[i]:>7.2f} {self.time_point[i]:>7.2f}")

    def _print_matrix(self):
        for i in self.V:
            for j in self.V:
                print(f"{self.time_matrix[i, j]:>7.2f}", end=' ')
            print()

    def save(self, file_path: str):
        instance_as_dict = {
                "num_elements": self.n,
                "mandates": [
                    {
                        "address": self.addresses_set[i],
                        "service_time": self.time_point[i],
                        "time_window": {
                            "start": self.time_window_a[i], 
                            "finish": self.time_window_b[i]
                            },
                        }
                    for i in self.V],
                "distance_matrix": self.distance_matrix.tolist(),
                "time_matrix": self.time_matrix.tolist()
                }

        with open(file_path, 'w') as f:
            json.dump(instance_as_dict, f, indent=4)

def load_json_instance(file_path: str):
    with open(file_path, 'r') as f:
        json_instance = json.load(f)
    time_window_a = np.array([addr["time_window"]["start"] for addr in json_instance['mandates']])
    time_window_b = np.array([addr["time_window"]["finish"] for addr in json_instance['mandates']])
    time_point = np.array([addr["service_time"] for addr in json_instance['mandates']])
    distance_matrix = np.array(json_instance['distance_matrix'])
    time_matrix = np.array(json_instance['time_matrix'])
    addresses_set = [addr["address"] for addr in json_instance['mandates']]
    return Instance(time_matrix, distance_matrix, time_point, time_window_a, time_window_b, addresses_set)

def generate_random_instance(n: int, seed: int = 1):
    rng = np.random.default_rng(seed)
    coords = rng.uniform(0, 10, size=(n, 2))
    distance_matrix = np.linalg.norm(
        coords[:, None, :] - coords[None, :, :], axis=2
    )
    time_matrix = distance_matrix + rng.uniform(0, 5, size=(n, n))

    np.fill_diagonal(distance_matrix, 0)
    np.fill_diagonal(time_matrix, 0)

    time_window_a = rng.uniform(0, 50, size=n)
    time_window_b = time_window_a + rng.uniform(50, 1000, size=n)
    time_point = rng.uniform(1, 10, size=n)

    return Instance(
        time_matrix=time_matrix,
        distance_matrix=distance_matrix,
        time_point=time_point,
        time_window_a=time_window_a,
        time_window_b=time_window_b,
        addresses_set=[f"Address {i}" for i in range(n)]
    )
