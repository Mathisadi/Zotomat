import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Ouverture de la BDD Reseau
df_rso = pd.read_csv("./data/Etat_reseau.csv")

# On crée le graphe a partir de la BDD
G = nx.from_pandas_edgelist(
    df_rso, source="Poste_A", target="Poste_B", edge_attr=["Tension", "Etat"]
)

nx.draw(G, 
        with_labels=True,      # affiche les noms des postes
        node_color="lightblue",
        node_size=500,
        font_size=8)

plt.show()