import pandas as pd
import numpy as np

# Ouverture de la BDD
data = pd.read_sql("Element_reseau", "sqlite:///RSO.db", index_col="id")

# On cree un dataframe de pandas
data = pd.DataFrame(data)

print(data)

# Comment vérifier la topo de tous les postes, on commence par les postes qui n'ont qu'un seul voisin
# Puis on remonte dans ces voisins jusqu'à ceux qu'un poste n'est plus un seul voisin ou des antennes

# Fonction qui définit les postes n'ayant qu'une ligne ES comme un poste en antenne
def poste_1_voisin(id_poste, df=data):
    # On convertit le voisin en array numpy
    id_voisin = np.array(df.iloc[id_poste - 1]["voisin"])
    
    # Les ID = position dans la dataframe + 1
    id_voisin = id_voisin - 1
    
    # On vérifie que dans tous ces voisins on à qu'une ligne ES
    df_voisin = df.iloc[id_voisin]

    df_voisin = df_voisin[(df_voisin["type"] == "Ligne") & (df_voisin["etat"] == "ES")]
    
    return len(df_voisin) <= 1
