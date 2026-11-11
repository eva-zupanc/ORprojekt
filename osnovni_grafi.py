import networkx as nx
from funkcija_c_ind import c_ind

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

    n = G.number_of_nodes()
    delta = vrednost - n // 2

    H = G.subgraph(S)
    pravilno = all(H.degree(v) == 2 for v in S)

    print(f"\nGraf: {ime}")
    print(f"c_ind(G) = {vrednost}")
    print(f"Mnozica S = {sorted(S)}")
    print(f"2-regularen: {pravilno}")
    print(f"Delta(G) = {delta}")

#Graf: K4
#c_ind(G) = 3
#Mnozica S = [1, 2, 3]
#2-regularen: True
#Delta(G) = 1
#
#Graf: K3,3
#c_ind(G) = 4
#Mnozica S = [1, 2, 3, 5]
#2-regularen: True
#Delta(G) = 1
#
#Graf: Prizma
#c_ind(G) = 4
#Mnozica S = [0, 2, 3, 5]
#2-regularen: True
#Delta(G) = 1
#
#Graf: Petersen
#c_ind(G) = 6
#Mnozica S = [0, 1, 3, 4, 6, 8]
#2-regularen: True
#Delta(G) = 1
#
#Graf: Franklin
#c_ind(G) = 6
#Mnozica S = [0, 1, 2, 3, 4, 5]
#2-regularen: True
#Delta(G) = 0