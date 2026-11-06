# VELIK GIRTH z GENG

import csv # Pythonova knjižnica za delo z datotekami CSV
import subprocess # Knjižnica, ki omogoča, da zaženemo drug program (tu nauty-geng)
from pathlib import Path

import networkx as nx # Knjižnica za delo z grafi
from financni_praktikum import c_ind


# Stevila vozlisc, ki jih zelimo pregledati
velikosti = [24]

# Mapa projekta
mapa = Path(__file__).resolve().parent


for n in velikosti:
    datoteka = mapa / f"grafi{n}.g6" # datoteka, ki vsebuje ustvarjene grafe
    rezultati_csv = mapa / f"rezultati_girth{n}.csv" # vsebuje rezultate izračunov

    # Ce datoteka se ne obstaja, ustvarimo grafe z geng
    if not datoteka.exists():
        print(f"\nGeneriram grafe s {n} vozlisci ...", flush=True)

        with open(datoteka, "wb") as f:
            # Ustvarim datoteko, v katero bo program zapisal grafe
            subprocess.run(
                ["wsl", "nauty-geng", "-c", "-d3", "-D3", "-tf", str(n)],
                stdout=f,
                check=True
            )
            # Zaženem program nauty-geng

    # Ce rezultati ze obstajajo, jih ne racunamo ponovno
    if rezultati_csv.exists():
        print(f"\nRezultati za n={n} ze obstajajo. Preskocim.")
        continue

    print(f"\nAnaliziram grafe s {n} vozlisci ...", flush=True)

    rezultati = []
    najmanjsa = None
    najboljsi = []

    # Beremo grafe enega po enega
    with open(datoteka, "rb") as f:
        for i, vrstica in enumerate(f, start=1):
            if not vrstica.strip():
                continue

            G = nx.from_graph6_bytes(vrstica.strip()) # networkx iz formata graph6 pretvori v objekt G
            vrednost, S = c_ind(G) # uporabimo našo funkcijo

            delta = vrednost - n // 2

            if not all(d == 2 for _, d in G.subgraph(S).degree()):
                raise ValueError(f"Napaka pri grafu {i}, n={n}")

            rezultati.append([i, n, vrednost, delta])

            if najmanjsa is None or delta < najmanjsa:
                najmanjsa = delta
                najboljsi = [i]
            elif delta == najmanjsa:
                najboljsi.append(i)
            # zapomnimo si najboljše grafe

            if i % 100 == 0:
                print(f"Pregledanih {i} grafov za n={n}", flush=True)

    # Shranimo rezultate v CSV - NE VEM ČE JE TO RES POTREBNO, lahko naknadno izbrišemo
    with open(rezultati_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["graf", "n", "c_ind", "delta"])
        writer.writerows(rezultati)

    print(f"\nREZULTATI ZA n={n}")
    print(f"Stevilo pregledanih grafov: {len(rezultati)}")
    print(f"Najmanjsa delta: {najmanjsa}")
    print(f"Grafi z najmanjso delto: {najboljsi}")
    print(f"Shranjeno v: {rezultati_csv.name}")


#REZULTATI ZA n=16
#Stevilo pregledanih grafov: 49
#Najmanjsa delta: 2
#Grafi z najmanjso delto: [2, 3, 7, 8, 16, 23, 24, 26, 28, 30, 39, 42, 44, 45, 47]
#Shranjeno v: rezultati_girth16.csv
#
#REZULTATI ZA n=18
#Stevilo pregledanih grafov: 455
#Najmanjsa delta: 1
#Grafi z najmanjso delto: [3]
#Shranjeno v: rezultati_girth18.csv
#
#REZULTATI ZA n=20
#Stevilo pregledanih grafov: 5783
#Najmanjsa delta: 2
#Grafi z najmanjso delto: [1, 4, 5, 7, 8, 9, 30, 43, 72, 105, 125, 190, 209, 286, 310, 321, 345, 356, 408, 449, 574, 1214, 1217, 1219, 1233, 1267, 1302, 1480, 1510, 1532, 1814, 1880, 2020, 2609, 2652, 2719, 2768, 2859, 3112, 3143, 3888, 4115, 4260, 4544, 4824, 4858, 4917, 5202, 5214, 5216, 5265, 5273, 5339, 5500, 5503, 5508, 5527, 5742, 5747, 5758, 5764, 5780]
#Shranjeno v: rezultati_girth20.csv
#
#REZULTATI ZA n=22
#Stevilo pregledanih grafov: 90938
#Najmanjsa delta: 1
#Grafi z najmanjso delto: [26]
#Shranjeno v: rezultati_girth22.csv

# Za n=24 bi trajalo predolgo, sem dala girth vsaj 6 (zamenjala tf s tfp)
#REZULTATI ZA n=24
#Stevilo pregledanih grafov: 7574
#Najmanjsa delta: 2
#Grafi z najmanjso delto: [49, 51, 53, 142, 152, 973]
#Shranjeno v: rezultati_girth24.csv