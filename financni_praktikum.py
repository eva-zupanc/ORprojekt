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

