import numpy as np

import vrptw

if __name__ == '__main__':
    addresses_set = [
            "Avenida Antônio Apolônio de Oliveira, Caruaru Pernambuco",
            "Cosmopolitan Shopping Caruaru Pernambuco",
            "Rua Cleto Campelo Caruaru Pernambuco",
            "Tribunal de Justiça de Pernambuco 1ª Câmara Regional",
            "Shopping Difusora Caruaru Pernambuco",
            "Insano's Hamburgueria Caruaru Pernambuco",
            "Escapecar Caruaru Pernambuco",
            "Cerpe Avenida Agamenon Magalhães Caruaru Pernambuco",
            "Unidade de Saúde da Família Padre Inácio Caruaru Pernambuco",
            ]

    durations, distances = vrptw.get_geodata_osrm(addresses_set, duplicate_base=True)
    V = range(durations.shape[0])
    time_point = np.array([10*60.0 for _ in V])
    time_point[0] = 0.0
    time_point[-1] = 0.0
    a = np.array([0.0 for _ in V])
    b = np.array([8*60*60.0 for _ in V])
    b[-1] = 9*60*60.0
    addresses_set.append(addresses_set[0])

    instance = vrptw.Instance(durations, distances, time_point, a, b, addresses_set)
    instance.save('instanceOSRM.json')
