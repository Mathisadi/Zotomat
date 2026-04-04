import pandas as pd
import networkx as nx

# Ouverture de la BDD Reseau
df_rso = pd.read_csv("Etat_reseau.csv")

# On supprime toutes les liaisons HU ou SUAV
df_rso = df_rso[df_rso["Tension"] == "ES"]

# On crée le graphe a partir de la BDD
G = nx.from_pandas_edgelist(
    df_rso, source="Poste_A", target="Poste_B", edge_attr="Tension"
)


# Fonction qui retourne l'ensemble des postes mis en antenne
def get_poste_en_antenne(G, bridge):
    # On suprime le pont et on regarde les poches de postes indépendants
    u, v = bridge
    G.remove_edge(u, v)
    composante = list(nx.connected_components(G))

    # On remet le bridge
    G.add_edge(u, v)

    return min(composante, key=len)


# Fonction qui pour une poche en antenne trouve quel poste du pont est coté antenne
def poste_cote_antenne(G, bridge, composante):
    u, v = bridge
    return u if u in composante else v


# Ouverture de la BDD Poste
df_poste = pd.read_csv("Type_poste.csv")


# Fonction qui pour des postes en antennes détermine quel type d'antenne il s'agit
def get_type_antenne(G, composante, df):
    # On récupére la liste des types de poste de la composante
    types = [df.loc[df["Poste"] == poste]["Type"].values[0] for poste in composante]

    # On retourne le type unique ou mixte
    return types[0] if all(t == types[0] for t in types) else "Mixte"
