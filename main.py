import pandas as pd
import numpy as np

import timeit

# Ouverture de la BDD
data = pd.read_sql("Element_reseau", "sqlite:///RSO.db", index_col="id")

# On cree un dataframe de pandas
data = pd.DataFrame(data)

# Comment vérifier la topo de tous les postes, on commence par les postes qui n'ont qu'un seul voisin
# Puis on remonte dans ces voisins jusqu'à ceux qu'un poste n'est plus un seul voisin ou des antennes

def poste_voisin(id_poste, df):
    """
    Retourne la liste des postes voisins d'un poste. Ne supprime pas les doublons si deux liaisons relient le même poste il apparaitre deux fois.

    Parameters
    ----------
    id_poste : int
        L'id du poste dont on cherche les voisins
    df : pandas.DataFrame
        La dataframe contenant les informations des postes

    Returns
    -------
    pandas.DataFrame
        La dataframe contenant les informations des postes voisins
    """
    # On convertit le voisin en array numpy
    id_voisin = df.loc[id_poste]["voisin"]

    # On extrait la df des postes voisins
    df_voisin = df.loc[id_voisin]

    # On a besoin des id des postes voisins
    id_poste_voisin = df_voisin[
        (df_voisin["type"] == "Ligne") & (df_voisin["etat"] == "ES")
    ]["voisin"].to_numpy()
    
    # On applatit la liste des id
    id_poste_voisin = np.concatenate(id_poste_voisin)

    # On supprime l'id du poste de départ
    id_poste_voisin = id_poste_voisin[id_poste_voisin != id_poste]

    # On extrait la df des postes voisins
    df_poste_voisin = df.loc[id_poste_voisin]

    # On ne garde que les postes
    df_poste_voisin = df_poste_voisin[(df_poste_voisin["type"] == "Poste")]

    return df_poste_voisin

def poste_en_antenne(id_poste, df):
    # On extrait les postes voisins
    df_poste_voisin = poste_voisin(id_poste, df)

    # On garde que les postes bouclés
    df_poste_voisin = df_poste_voisin[(df_poste_voisin["topo_poste"] == "B")]

    return len(df_poste_voisin) <= 1

def type_antenne(id_poste, df):
    # On extrait les voisins du poste hors postes
    df_voisin = df.loc[id_poste]["voisin"]
    
    # On regarde le nombre de prod conso sur le poste
    nbr_prod = len(df_voisin[(df_voisin["type"] == "Prod") & (df_voisin["etat"] == "ES")])
    nbr_conso = len(df_voisin[(df_voisin["type"] == "Conso") & (df_voisin["etat"] == "ES")])
    
    # On extrait les postes voisins
    df_poste_voisin = poste_voisin(id_poste, df)
    
    # On garde que les postes en antenne
    nbr_ant_conso = len(df_poste_voisin[(df_poste_voisin["topo_poste"] == "A C")])
    nbr_ant_prod = len(df_poste_voisin[(df_poste_voisin["topo_poste"] == "A P")])
    nbr_ant_mixte = len(df_poste_voisin[(df_poste_voisin["topo_poste"] == "A M")])
    
    # Logique
    if nbr_ant_mixte != 0:
        return "A M"
    elif (nbr_ant_prod + nbr_prod) != 0 and (nbr_ant_conso + nbr_conso) != 0:
        return "A M"
    elif (nbr_ant_prod + nbr_prod) != 0 and (nbr_ant_conso + nbr_conso) == 0:
        return "A C"
    elif (nbr_ant_prod + nbr_prod) == 0 and (nbr_ant_conso + nbr_conso) != 0:
        return "A P"
    else:
        return "A"

# Fonction qui met à jour la BDD
def update_database(df):
    df.to_sql("Element_reseau", "sqlite:///RSO.db", if_exists="replace")
    

def antenne_rso(df=data):
    # On crée une pile de tous les postes à vérifier
    id_pile = []

    # On trouve tous les postes à 1 vosin, on change leur type et on les ajoute dans la pile
    df_poste = df[df["type"] == "Poste"]
    
    for id in df_poste.index.to_list():
        if poste_en_antenne(id, df):           
            # On ajoute l'id à la pile
            id_pile.append(id)

    # Tant que la pile n'est pas vide on va chercher à remonter le plus haut possible dans les voisins
    while id_pile:
        # On extrait le poste de la pile
        id_poste = id_pile.pop()

        # On vérifie si le poste est une antenne 
        if poste_en_antenne(id_poste, df) and df.loc[id_poste]["topo_poste"] == "B":
            # On cherche le type d'antenne
            type_ant = type_antenne(id_poste, df)
            
            # On modifie sa topo
            df.loc[id_poste, "topo_poste"] = type_ant

            # On ajoute les voisins de ce poste dans la pile
            df_poste_voisin = poste_voisin(id_poste, df)
            id_voisin = df_poste_voisin.index.to_numpy()
            id_voisin = np.unique(id_voisin).tolist()
            id_pile.extend(id_voisin)
    
    # On met à jour la BDD
    update_database(df)
