# RES sous forme d'un csv
# IC MONO RVL RVB REB RTR 
# Regle 2RA max sauf si câble non protégé
# Donnée d'entrée type de liaisons d'antenne et le bridge

import pandas as pd

df = pd.read_csv("./data/PAP.csv")

def PAP_installe(df, Poste, Dep):
    return not df.loc[(df["Poste"] == Poste) & (df["Dep"] == Dep)].empty

def RTR_possible(df, Poste):
    return not df.loc[df["Poste"] == Poste].empty

def RA_THT_Conso(df, Poste_RG, Poste_Antenne):

    return

def RA_THT_Prod(df, bridge):
    return

def RA_THT_Mixte(df, bridge):
    return

def RA_HT_Conso(df, bridge):
    return

def RA_HT_Prod(df, bridge):
    return

def RA_HT_Mixte(df, bridge):
    return

df = pd.read_csv("./data/Type_liaison.csv")

def get_RA(df, bridge, type_liaison):
    # On extrait les noms des postes du bridge
    u,v = bridge
    
    # On trouve le niveau de tension du pont
    mask = (
        ((df["Poste_A"] == u) & (df["Poste_B"] == v)) |
        ((df["Poste_A"] == v) & (df["Poste_B"] == u))
    )
    tension = df.loc[mask]["Tension"].values[0]
    
    return
