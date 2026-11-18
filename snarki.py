import networkx as nx
from funkcija_c_ind import c_ind
import csv

N = 30
grafi = nx.read_graph6(f"snarki/snarki{N}.g6")

print("Stevilo grafov:", len(grafi))

rezultati = []

for i, G in enumerate(grafi, start=1):
    n = G.number_of_nodes()
    c, S = c_ind(G)
    delta = c - n // 2
    rezultati.append([i, n, c, delta])
    if i % 1000 == 0 or i == len(grafi):
        print(f"Pregledanih {i}/{len(grafi)} grafov")

min_delta = min(r[3] for r in rezultati)
najboljsi_grafi = [r for r in rezultati if r[3] == min_delta]
print("Najmanjsa delta:", min_delta)
print("Stevilo grafov z najmanjso delto:", len(najboljsi_grafi))
print("\nNAJMANJSA NAJDENA DELTA:")

for i, n, c, delta in najboljsi_grafi:
    print(f"Snark {i}: n={n}, c_ind={c}, delta={delta}")

with open(f"snarki/rezultati_snarki{N}.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["graf", "n", "c_ind", "delta"])
    writer.writerows(rezultati)

print("\nPOVZETEK:")
print("Stevilo pregledanih grafov:", len(grafi))
print("Najmanjsa delta:", min_delta)
print("Stevilo grafov z najmanjso delto:", len(najboljsi_grafi))

# N = 26, girth vsaj 5
# NAJMANJSA NAJDENA DELTA:
# Snark 92: n=26, c_ind=16, delta=3
# Snark 130: n=26, c_ind=16, delta=3
# POVZETEK:
# Stevilo pregledanih grafov: 280
# Najmanjsa delta: 3
# Stevilo grafov z najmanjso delto: 2

# N = 26, girth vsaj 4
# NAJMANJSA NAJDENA DELTA:
# Snark 271: n=26, c_ind=16, delta=3
# Snark 422: n=26, c_ind=16, delta=3
# POVZETEK:
# Stevilo pregledanih grafov: 1297
# Najmanjsa delta: 3
# Stevilo grafov z najmanjso delto: 2

# N = 28
# POVZETEK:
# Stevilo pregledanih grafov: 2900
# Najmanjsa delta: 4
# Stevilo grafov z najmanjso delto: 259
