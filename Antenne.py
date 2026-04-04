import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Ouverture de la BDD
data = pd.read_csv("Etat_reseau.csv")

print(data)
# On crée le graphe a partir de la BDD
G = nx.from_pandas_edgelist(
    data, source="Poste_A", target="Poste_B", edge_attr=["Tension", "Etat"]
)

print(list(nx.bridges(G)))