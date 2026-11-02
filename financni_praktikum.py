
# Knjiznice: pip install networkx scipy numpy

import networkx as nx
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix


def c_ind(G):
    vertices = list(G.nodes())
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}

    A = lil_matrix((2 * n, n))
    lower = np.full(2 * n, -np.inf)
    upper = np.full(2 * n, np.inf)

    for v in vertices:
        i = index[v]
        A[i, i] = -2
        A[n + i, i] = 1

        for u in G.neighbors(v):
            j = index[u]
            A[i, j] = 1
            A[n + i, j] = 1

        lower[i] = 0
        upper[n + i] = 3

    result = milp(
        c=-np.ones(n),
        integrality=np.ones(n),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(
            A.tocsr(), lower, upper
        )
    )

    if not result.success:
        raise RuntimeError(result.message)

    S = {
        v for v, x in zip(vertices, result.x)
        if x > 0.5
    }

    return len(S), S


# Ustvarimo grafe
grafi = {
    "K4": nx.complete_graph(4),
    "K3,3": nx.complete_bipartite_graph(3, 3),
    "Prizma": nx.circular_ladder_graph(3),
    "Petersen": nx.petersen_graph(),
    "Franklin": nx.LCF_graph(12, [5, -5], 6)
}


# Izracunamo in preverimo rezultate
for ime, G in grafi.items():
    vrednost, S = c_ind(G)

    H = G.subgraph(S)
    pravilno = all(H.degree(v) == 2 for v in S)

    print(f"\nGraf: {ime}")
    print(f"c_ind(G) = {vrednost}")
    print(f"Mnozica S = {sorted(S)}")
    print(f"2-regularen: {pravilno}")
