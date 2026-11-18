import networkx as nx
from funkcija_c_ind import c_ind
import csv
import subprocess
import os


N = 20
m = (N + 4) // 2

if not os.path.exists(f"planarni/planarni{N}.g6"):
    subprocess.run([
        r"C:\msys64\ucrt64\bin\plantri.exe",
        "-dg",
        str(m),
        f"planarni/planarni{N}.g6"
    ], check=True)

grafi = nx.read_graph6(f"planarni/planarni{N}.g6")

print("Stevilo grafov:", len(grafi))

rezultati = []

with open(f"planarni/rezultati_planarni{N}.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["graf", "n", "c_ind", "delta"])
    for i, G in enumerate(grafi, start=1):
        n = G.number_of_nodes()
        c, S = c_ind(G)
        delta = c - n // 2
        rezultati.append([i, n, c, delta])
        writer.writerow([i, n, c, delta])
        f.flush()
        if i % 1000 == 0 or i == len(grafi):
            print(f"Pregledanih {i}/{len(grafi)} grafov")

min_delta = min(r[3] for r in rezultati)
najboljsi_grafi = [r for r in rezultati if r[3] == min_delta]

print("\nNAJMANJSA NAJDENA DELTA:")

for i, n, c, delta in najboljsi_grafi:
    print(f"Graf {i}: n={n}, c_ind={c}, delta={delta}")

print("\nPOVZETEK:")
print("Stevilo pregledanih grafov:", len(grafi))
print("Najmanjsa delta:", min_delta)
print("Stevilo grafov z najmanjso delto:", len(najboljsi_grafi))

# N = 18
# NAJMANJSA NAJDENA DELTA:
# Graf 166: n=18, c_ind=11, delta=2
# Graf 215: n=18, c_ind=11, delta=2
# POVZETEK:
# Stevilo pregledanih grafov: 1249
# Najmanjsa delta: 2
# Stevilo grafov z najmanjso delto: 2

# N = 20
# NAJMANJSA NAJDENA DELTA:
# Graf 4150: n=20, c_ind=12, delta=2
# Graf 4198: n=20, c_ind=12, delta=2
# Graf 7272: n=20, c_ind=12, delta=2
# Graf 7279: n=20, c_ind=12, delta=2
# POVZETEK:
# Stevilo pregledanih grafov: 7595
# Najmanjsa delta: 2
# Stevilo grafov z najmanjso delto: 4