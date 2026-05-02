import pandas as pd
import networkx as nx


# Fonction qui retourne l'ensemble des postes mis en antenne et la racine
def get_poste_en_antenne(G, bridge):
    u, v = bridge
    G.remove_edge(u, v)
    composantes = list(nx.connected_components(G))
    G.add_edge(u, v)

    composante = min(composantes, key=len)

    # La racine est le nœud du pont qui appartient à la petite composante
    racine = u if u in composante else v

    # Sous-graphe isolé
    sous_graphe = G.subgraph(composante).copy()

    # BFS depuis la racine → donne les relations parent-enfant
    arbre = nx.bfs_tree(sous_graphe, racine)

    return arbre


# Fonction qui pour une poche en antenne trouve quel poste du pont est coté antenne
def poste_cote_antenne(poste, dep, arbre):
    # Si un des poste n'est pas dans l'arbre il est forcement le poste cote RG
    if poste not in arbre:
        return dep
    else:
        # Est-ce que le pere du poste est le dép = cote antenne
        return dep if arbre.predecessors(poste) == dep else poste


# Fonction qui pour une poche en antenne trouve quel poste du pont est coté RG
def poste_cote_RG(poste, dep, arbre):
    # Si un des poste n'est pas dans l'arbre il est forcement le poste cote RG
    if poste not in arbre:
        return poste
    else:
        # Est-ce que le pere du poste est le.dep = cote RG
        return poste if arbre.predecessors(poste) == dep else dep

# Fonction qui retourne les descendants d'un poste et retourne None si il y a un cycle = pas de RA à reprendre
def get_descendants(arbre, poste):
    visites = set()
    pile = [poste]
    
    while pile:
        noeud = pile.pop()
        if noeud in visites:
            return None  # cycle détecté
        visites.add(noeud)
        pile.extend(arbre.successors(noeud))
    
    return visites

# Fonction qui pour des postes en antennes détermine quel type d'antenne il s'agit
def get_type_antenne_poste(G, descendants, df):

    # On récupére la liste des types de poste de la composante
    types = [df.loc[df["Poste"] == p]["Type"].values[0] for p in descendants]

    # On retourne le type unique ou mixte
    return types[0] if all(t == types[0] for t in types) else "Mixte"
