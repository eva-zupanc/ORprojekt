import networkx as nx
from funkcija_c_ind import c_ind

def generalized_petersen(n, k):
    G = nx.Graph()

    for i in range(n):
        # Zunanji cikel
        G.add_edge(i, (i + 1) % n)

        # Notranje povezave
        G.add_edge(n + i, n + (i + k) % n)

        # Povezava med zunanjim in notranjim vozliščem
        G.add_edge(i, n + i)

    return G



rezultati = []

for n in range(31,35):
    for k in range(1, (n - 1) // 2 + 1):
        G = generalized_petersen(n, k)

        vrednost, S = c_ind(G)
        delta = vrednost - G.number_of_nodes() // 2

        pravilno = all(d == 2 for _, d in G.subgraph(S).degree())
        if not pravilno:
            raise ValueError(f"Napaka pri P({n},{k})")

        rezultati.append((n, k, vrednost, delta))

        print(f"P({n},{k}): c_ind={vrednost}, delta={delta}")

print("\nNAJMANJSA NAJDENA DELTA:")
najmanjsa = min(r[3] for r in rezultati)

for n, k, vrednost, delta in rezultati:
    if delta == najmanjsa:
        print(f"P({n},{k}): c_ind={vrednost}, delta={delta}")

# za n od 12 do 31
#NAJMANJSA NAJDENA DELTA:
#P(13,2): c_ind=16, delta=3
#P(13,3): c_ind=16, delta=3
#P(13,4): c_ind=16, delta=3
#P(13,6): c_ind=16, delta=3

# za n od 31 do 34
#NAJMANJSA NAJDENA DELTA:
#P(31,2): c_ind=40, delta=9
#P(31,15): c_ind=40, delta=9

# Ker ima petersenov graf v bistvu 2*n vozlišč smo pregledali do 68 vozlišč.
# Vrednost delte se povečuje z večanjem n, zato sedaj le te opustimo.