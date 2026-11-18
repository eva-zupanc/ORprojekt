import networkx as nx
from funkcija_c_ind import c_ind
import csv

N = 42
girth = 8
grafi = nx.read_graph6(f"girth/girth{N}_{girth}.g6")

print("Stevilo grafov:", len(grafi))

rezultati = []

for i, G in enumerate(grafi, start=1):
    n = G.number_of_nodes()
    c, S = c_ind(G)
    delta = c - n // 2
    rezultati.append([i, n, c, delta])
    print(f"Graf {i}: n = {n}, c_ind = {c}, delta = {delta}")

min_delta = min(r[3] for r in rezultati)
najboljsi_grafi = [r for r in rezultati if r[3] == min_delta]
print("Najmanjsa delta:", min_delta)
print("Stevilo grafov z najmanjso delto:", len(najboljsi_grafi))
print("\nNAJMANJSA NAJDENA DELTA:")

for i, n, c, delta in najboljsi_grafi:
    print(f"Graf {i}: n={n}, c_ind={c}, delta={delta}")

with open(f"girth/rezultati_girth{N}_{girth}.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["graf", "n", "c_ind", "delta"])
    writer.writerows(rezultati)

print("\nPOVZETEK:")
print("Stevilo pregledanih grafov:", len(grafi))
print("Najmanjsa delta:", min_delta)
print("Stevilo grafov z najmanjso delto:", len(najboljsi_grafi))

# girth 7, N = 30
# POVZETEK:
# Stevilo pregledanih grafov: 546
# Najmanjsa delta: 5
# Stevilo grafov z najmanjso delto: 12

# girth 8, N = 42
# POVZETEK:
# Stevilo pregledanih grafov: 4337
# Najmanjsa delta: 6
# Stevilo grafov z najmanjso delto: 1