import pandas as pd
import networkx as nx

# Ouverture de la BDD Poste
df_poste = pd.read_csv("./data/Type_poste.csv")


# Fonction qui retourne l'ensemble des postes mis en antenne
def get_poste_en_antenne(G, bridge):
    # On suprime le pont et on regarde les poches de postes indépendants
    u, v = bridge
    G.remove_edge(u, v)
    descendant = list(nx.connected_components(G))

    # On remet le bridge
    G.add_edge(u, v)

    return min(descendant, key=len)


# Fonction qui pour une poche en antenne trouve quel poste du pont est coté antenne
def poste_RG_antenne(bridge, descendant):
    u, v = bridge
    return (v, u) if u in descendant else (u, v)


# Fonction qui pour des postes en antennes détermine quel type d'antenne il s'agit
def get_type_antenne(descendant, df=df_poste):
    # On récupére la liste des types de poste de la descendant
    types = [df.loc[df["Poste"] == poste]["Type"].values[0] for poste in descendant]

    # On retourne le type unique ou mixte
    return types[0] if all(t == types[0] for t in types) else "Mixte"
