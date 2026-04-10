import numpy as np
import urllib.parse
import json
import argparse

import pyomo.environ as pyo

class Solution:
    def __init__(self, model, report):
        self.V = sorted(model.V)
        self.N = sorted(model.N)
        self.K = sorted(model.K)

        self.sequence_set = [self._get_sequence_k(model, k) for k in self.K]
        self.allocation_set = [self._get_allocation_k(model, k) for k in self.K]
        self.time_set = [self._get_time_k(model, k) for k in self.K]

        self.obj = model.obj()
        self.time = report.solver.time

        self._validate_solution()

    def print(self):
        print(f"Objective value: {self.obj}")
        for k in self.K:
            print(f"DAY {k}")
            print(self.sequence_set[k], end='\n\n')
            for (idx, j) in enumerate(self.sequence_set[k]):
                print(f"{j:>4} ({self.time_set[k][idx]:>4.2f})", end=' ->')
            print()

    def ordenate_addresses_k(self, addresses_set, k):
        self.sequence_set[k][-1] = 0
        return [addresses_set[i] for i in self.sequence_set[k]]

    def save(self, file_path):
        solution = {
                "sequeces": self.sequence_set,
                "solve_time": self.time,
                "obj": self.obj
                }
        with open(file_path, 'w') as f:
            json.dump(solution, f, indent=4)


    def _get_sequence_k(self, model, k):
        sequence_k: list[int] = [0]
        i, j = 0, -1
        while j < self.V[-1]:
            j += 1
            if pyo.value(model.x[i, j, k]) < 0.5:
                continue

            sequence_k.append(j)
            i, j = j, -1
        return sequence_k

    def _get_allocation_k(self, model, k):
        allocation_k: list[int] = []
        for i in self.V:
            for j in self.N:
                if pyo.value(model.x[i, j, k]) > 0.5:
                    allocation_k.append(j)
        assert len(allocation_k) == len(np.unique(allocation_k))

        return allocation_k

    def _get_time_k(self, model, k):
        time_k: list[int] = []
        for i in self.sequence_set[k]:
            time_k.append(pyo.value(model.T[i, k]))
        return time_k

    def _validate_solution(self):
        for k in self.K:
            for i in self.allocation_set[k]:
                assert i in self.sequence_set[k]

def generate_maps_link(ordered_addresses):
    if len(ordered_addresses) == 2:
        return ""
    base_url = "https://www.google.com/maps/dir/?api=1"

    origin = urllib.parse.quote(ordered_addresses[0])
    destination = urllib.parse.quote(ordered_addresses[-1])

    if len(ordered_addresses) > 2:
        intermediate = ordered_addresses[1:-1]
        waypoints = "|".join([urllib.parse.quote(addr) for addr in intermediate])
        return f"{base_url}&origin={origin}&destination={destination}&waypoints={waypoints}"

    return f"{base_url}&origin={origin}&destination={destination}"

def get_api_key():
    with open('.api') as f:
        api_key = f.readline().strip()
    return api_key

def get_parse_args():
    parser = argparse.ArgumentParser(
            "VRPTW For a Court Officer",
            "This program solves a instance, provided in JSON, and saves the instance as a JSON file"
            )
    parser.add_argument('instance', type=str)
    parser.add_argument('-v', '--verbose', type=int, default=0)
    return parser.parse_args()
