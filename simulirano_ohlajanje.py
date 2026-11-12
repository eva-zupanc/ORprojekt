import networkx as nx
import random
import math

from funkcija_c_ind import c_ind


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
    # sodost števila vozlišč izhaja iz leme o rokovanju (stopnja(G) * n = 3 * n mora biti sodo, torej mora biti n sodo)
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

def prestej_kratke_cikle(G, max_dolzina=5):
    """
    Prešteje inducirane cikle dolžine 3, 4, ..., max_dolzina.
    Vrnemo skupno število.
    """
    st_kratkih = 0
    # networkx.find_cycles vrne vse cikle, mi pa filtriramo po dolžini
    for cycle in nx.simple_cycles(G, length_bound=max_dolzina):
        if 3 <= len(cycle) <= max_dolzina:
            st_kratkih += 1
    return st_kratkih

def izracunaj_ceno(G, n, beta=0.5):
    """
    Izračuna skupno 'ceno' grafa.
    Primarni del: Delta(G) = c_ind(G) - n/2
    Sekundarni del: beta * (število kratkih ciklov)
    """
    cind, _ = c_ind(G)
    delta = cind - (n / 2)
    
    if beta > 0:
        st_ciklov = prestej_kratke_cikle(G, max_dolzina=5)
        return delta + (beta * st_ciklov), delta, st_ciklov
    else:
        return delta, delta, 0


# --- Glavna funkcija simuliranega ohlajanja ---

def simulirano_ohlajanje(n, zacetna_temp=1.0, koncna_temp=0.01, ohlajanje=0.9999, iteracij=10000, seme=None, beta=0.5):
    """
    Izvaja simulirano ohlajanje za iskanje kubičnega grafa z n vozlišči 
    in čim manjšo vrednostjo Delta(G).
    """
    if seme is not None:
        random.seed(seme)

    # 1. Začetno stanje    
    trenutni_graf = nakljucni_kubicen_graf(n)
    cena_trenutna, delta_trenutni, cikli_trenutni = izracunaj_ceno(trenutni_graf, n, beta)
    
    najboljsi_graf = trenutni_graf.copy()
    najboljsa_cena = cena_trenutna
    najboljsi_delta = delta_trenutni
    najboljsi_cikli = cikli_trenutni
    najboljsi_cind, _ = c_ind(najboljsi_graf)

    T = zacetna_temp
    
    for i in range(iteracij):
        # 2. Generiraj sosednje stanje (nov graf)
        nov_graf = preklop_povezav(trenutni_graf)
        if nov_graf is None:
            continue
            
        cena_nova, delta_nov, cikli_nov = izracunaj_ceno(nov_graf, n, beta)

        # 3. Razlika v ciljni funkciji (tj. ceni)
        razlika = cena_nova - cena_trenutna
        
        # 4. Odločitev o sprejemu (Metropolisov kriterij)
        # Metropolisov kriterij: koda začasno sprejme slabši graf od trenutnega, kar ji odpre pot do iskanja povsem drugačnih struktur grafov
        if razlika < 0:
            sprejmi = True
        else:
            verjetnost = math.exp(-razlika / T) if T > 0 else 0
            sprejmi = random.random() < verjetnost
            
        if sprejmi:
            trenutni_graf = nov_graf
            cena_trenutna = cena_nova
            delta_trenutni = delta_nov

            # Posodobi najboljšega, če je potrebno
            if cena_trenutna < najboljsa_cena:
                najboljsa_cena = cena_trenutna
                najboljsi_delta = delta_trenutni
                najboljsi_cikli = cikli_nov
                najboljsi_graf = trenutni_graf.copy()
                najboljsi_cind = c_ind(najboljsi_graf)
        
        # 5. Znižaj temperaturo
        T = max(koncna_temp, T * ohlajanje)
            
    # Vrnemo slovar z vsemi pomembnimi podatki
    graph6_zapis = nx.to_graph6_bytes(najboljsi_graf, header=False).decode('ascii').strip()
    return {
        'n': n,
        'zacetna_temp': zacetna_temp,
        'koncna_temp': koncna_temp,
        'ohlajanje': ohlajanje,
        'iteracij': iteracij,
        'seme': seme,
        'c_ind': najboljsi_cind,
        'delta': najboljsi_delta,
        'st_kratkih_ciklov': najboljsi_cikli,
        'graph6': graph6_zapis
    }