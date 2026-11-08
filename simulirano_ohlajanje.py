import networkx as nx
import random
import math
import time
import csv
import os

from financni_praktikum import izracunaj_cind


# --- Pomožne funkcije za grafe ---

def je_povezan_in_kubicen(G):
    """Preveri, ali je graf povezan in ali imajo vsa vozlišča stopnjo 3."""
    if not nx.is_connected(G):
        return False
    for node in G.nodes():
        if G.degree(node) != 3:
            return False
    return True

def nakljucni_kubicen_graf(n):
    """Generira naključen povezan kubičen graf z n vozlišči."""
    if n % 2 != 0 or n < 4:
        raise ValueError("n mora biti sodo in vsaj 4.")
    # Uporabimo networkx generator, nato preverimo pogoje
    while True:
        G = nx.random_regular_graph(3, n)
        if nx.is_connected(G):
            return G

def preklop_povezav(G):
    """
    Izvede 2-switch (preklop povezav) na kopiji grafa G.
    Vrne nov graf ali None, če preklop ni mogoč.
    """
    H = G.copy()
    edges = list(H.edges())
    
    # Poskusimo najti dve povezavi, ki se ne dotikata
    for _ in range(100):
        e1, e2 = random.sample(edges, 2)
        u, v = e1
        x, y = e2
        
        # Zagotovimo, da so 4 vozlišča različna
        if len({u, v, x, y}) < 4:
            continue
            
        # Preverimo, ali nova povezava že obstaja
        if H.has_edge(u, x) or H.has_edge(v, y):
            continue
            
        # Izvedemo preklop: odstranimo e1, e2 in dodamo (u,x), (v,y)
        H.remove_edge(u, v)
        H.remove_edge(x, y)
        H.add_edge(u, x)
        H.add_edge(v, y)
        
        # Preverimo, ali je graf še vedno povezan
        if nx.is_connected(H):
            return H
        else:
            # Če ni povezan, razveljavimo in poskusimo znova
            H = G.copy()
            
    return None

def delta_vrednost(G, c_ind):
    """Izračuna Delta(G) = c_ind(G) - n/2."""
    return c_ind - (len(G) / 2)

# --- Glavna funkcija simuliranega ohlajanja ---

def simulirano_ohlajanje(n, zacetna_temp=1.0, koncna_temp=0.01, ohlajanje=0.9999, iteracij=10000, seme=None):
    """
    Izvaja simulirano ohlajanje za iskanje kubičnega grafa z n vozlišči 
    in čim manjšo vrednostjo Delta(G).
    """
    if seme is not None:
        random.seed(seme)
        
    print(f"Začenjam iskanje za n={n}...")
    
    # 1. Začetno stanje
    trenutni_graf = nakljucni_kubicen_graf(n)
    c_ind_trenutni, _ = izracunaj_cind(trenutni_graf)
    delta_trenutni = delta_vrednost(trenutni_graf, c_ind_trenutni)
    
    # Najboljše stanje do zdaj
    najboljsi_graf = trenutni_graf.copy()
    najboljsi_delta = delta_trenutni
    najboljsi_c_ind = c_ind_trenutni
    
    T = zacetna_temp
    
    for i in range(iteracij):
        # 2. Generiraj sosednje stanje (nov graf)
        nov_graf = preklop_povezav(trenutni_graf)
        if nov_graf is None:
            continue  # Preklop ni uspel, poskusi znova
            
        c_ind_nov, _ = izracunaj_cind(nov_graf)
        delta_nov = delta_vrednost(nov_graf, c_ind_nov)
        
        # 3. Razlika v ciljni funkciji
        razlika = delta_nov - delta_trenutni
        
        # 4. Odločitev o sprejemu (Metropolisov kriterij)
        # Metropolisov kriterij: koda začasno sprejme slabši graf od trenutnega, kar ji odpre pot do iskanja povsem drugačnih struktur grafov
        if razlika < 0:
            # Nov graf je boljši, vedno ga sprejmi
            sprejmi = True
        else:
            # Nov graf je slabši, sprejmi ga z določeno verjetnostjo
            verjetnost = math.exp(-razlika / T) if T > 0 else 0
            sprejmi = random.random() < verjetnost
            
        if sprejmi:
            trenutni_graf = nov_graf
            delta_trenutni = delta_nov
            
            # Posodobi najboljšega, če je potrebno
            if delta_trenutni < najboljsi_delta:
                najboljsi_delta = delta_trenutni
                najboljsi_graf = trenutni_graf.copy()
                najboljsi_c_ind = c_ind_nov
                print(f"  Iteracija {i}: Našli smo boljši graf! Delta = {najboljsi_delta}")
        
        # 5. Znižaj temperaturo
        T = max(koncna_temp, T * ohlajanje)
        
        # Začasni izpis napredka (za vsako tisočo iteracijo)
        if (i + 1) % 1000 == 0:
            print(f"  Iteracija {i+1}/{iteracij}, T={T:.4f}, Trenutna Delta={delta_trenutni}, Najboljša Delta={najboljsi_delta}")
            
    return najboljsi_graf, najboljsi_c_ind, najboljsi_delta

# --- Zagon in shranjevanje ---

if __name__ == "__main__":
    # Parametri za zagon
    N_VOZLISCA = 24  # Primer za n=24
    ITERACIJE = 5000  # Za resne poskuse povečajte na 50000+
    
    print(f"--- Simulirano ohlajanje za n={N_VOZLISCA} ---")
    
    # Izvedi iskanje
    naj_graf, naj_cind, naj_delta = simulirano_ohlajanje(n=N_VOZLISCA, iteracij=ITERACIJE)
    
    print("\n--- KONČNI REZULTAT ---")
    print(f"Najboljša najdena Delta(G): {naj_delta}")
    print(f"c_ind(G): {naj_cind}")
    
    # Shranjevanje grafa v format graph6
    graph6_zapis = nx.to_graph6_bytes(naj_graf, header=False).decode('ascii').strip()
    print(f"Graf6 zapis: {graph6_zapis}")
    
    # Shranjevanje v CSV
    csv_datoteka = 'najboljsi_grafi_ohlajanje.csv'
    file_exists = os.path.isfile(csv_datoteka)
    
    with open(csv_datoteka, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['n', 'c_ind', 'Delta', 'graph6', 'cas'])
        
        cas = time.strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([N_VOZLISCA, naj_cind, naj_delta, graph6_zapis, cas])
        
    print(f"Rezultat shranjen v {csv_datoteka}.")
