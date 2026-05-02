# RES sous forme d'un csv
# IC MONO RVL RVB REB RTR
# Regle 2RA max sauf si câble non protégé
# Donnée d'entrée type de liaisons d'antenne et le bridge

import pandas as pd

# On extrait les BDD utilisées
df_pap = pd.read_csv("./data/PAP.csv")
df_rtr = pd.read_csv("./data/RTR.csv")
df_liaison = pd.read_csv("./data/Type_liaison.csv")


def PAP_installe(poste, dep, df=df_pap):
    return not df.loc[(df["Poste"] == poste) & (df["Dep"] == dep)].empty


def RTR_possible(poste, df=df_rtr):
    return not df.loc[df["Poste"] == poste].empty


def RA_THT_Conso(Poste_RG, Poste_Antenne):

    
    RA_RG = {
        "Poste": Poste_RG,
        "Dep": Poste_Antenne,
        "IC": True,
        "Mono": PAP_installe(Poste_Antenne, Poste_RG),
        "RVL": 12,
        "RVB": 12,
        "REB": 2,
        "2RA": None,
        "RTR": None,
    }

    return RA_RG


def RA_THT_Prod(Poste_RG, Poste_Antenne):

    RA_ANTENNE = {
        "Poste": Poste_Antenne,
        "Dep": Poste_RG,
        "IC": False,
        "Mono": True,
        "RVL": 0,
        "RVB": 1,
        "REB": 0,
        "2RA": None,
        "RTR": None,
    }

    RA_RG = {
        "Poste": Poste_RG,
        "Dep": Poste_Antenne,
        "IC": False,
        "Mono": True,
        "RVL": 1,
        "RVB": 1,
        "REB": 0,
        "2RA": None,
        "RTR": None,
    }

    return [RA_ANTENNE, RA_RG]


def RA_THT_Mixte(Poste_RG, Poste_Antenne):

    RA_ANTENNE = {
        "Poste": Poste_Antenne,
        "Dep": Poste_RG,
        "IC": False,
        "Mono": True,
        "RVL": 0,
        "RVB": 1,
        "REB": 0,
        "2RA": None,
        "RTR": None,
    }

    RA_RG = {
        "Poste": Poste_RG,
        "Dep": Poste_Antenne,
        "IC": False,
        "Mono": PAP_installe(Poste_Antenne, Poste_RG),
        "RVL": 1,
        "RVB": 1,
        "REB": 0,
        "2RA": None,
        "RTR": None,
    }

    return [RA_ANTENNE, RA_RG]


def RA_HT_Conso(Poste_RG, Poste_Antenne):

    RA_RG = {
        "Poste": Poste_RG,
        "Dep": Poste_Antenne,
        "IC": True,
        "Mono": None,
        "RVL": 12,
        "RVB": 12,
        "REB": 2,
        "2RA": True,
        "RTR": RTR_possible(Poste_Antenne),
    }

    return RA_RG


def RA_HT_Prod(Poste_RG, Poste_Antenne):

    RA_ANTENNE = {
        "Poste": Poste_Antenne,
        "Dep": Poste_RG,
        "IC": False,
        "Mono": None,
        "RVL": 0,
        "RVB": 1,
        "REB": 0,
        "2RA": False,
        "RTR": False,
    }

    RA_RG = {
        "Poste": Poste_RG,
        "Dep": Poste_Antenne,
        "IC": False,
        "Mono": None,
        "RVL": 1,
        "RVB": 1,
        "REB": 0,
        "2RA": False,
        "RTR": False,
    }

    return [RA_ANTENNE, RA_RG]


def RA_HT_Mixte(Poste_RG, Poste_Antenne):

    RA_ANTENNE = {
        "Poste": Poste_Antenne,
        "Dep": Poste_RG,
        "IC": False,
        "Mono": None,
        "RVL": 0,
        "RVB": 1,
        "REB": 0,
        "2RA": False,
        "RTR": False,
    }

    RA_RG = {
        "Poste": Poste_RG,
        "Dep": Poste_Antenne,
        "IC": False,
        "Mono": None,
        "RVL": 1,
        "RVB": 1,
        "REB": 0,
        "2RA": False,
        "RTR": False,
    }
    return [RA_ANTENNE, RA_RG]


def get_RA(Poste_RG, Poste_Antenne, type_antenne, df=df_liaison):

    # On trouve le niveau de tension de la liaison
    mask = ((df["Poste_A"] == Poste_RG) & (df["Poste_B"] == Poste_Antenne)) | (
        (df["Poste_A"] == Poste_Antenne) & (df["Poste_B"] == Poste_RG)
    )

    tension = df.loc[mask]["Tension"].values[0]

    # En fonction de la tension et du type d'antenne on retourne le bon RA
    if tension > 63 and type_antenne == "Conso":
        return RA_THT_Conso(Poste_RG, Poste_Antenne)

    elif tension > 63 and type_antenne == "Prod":
        return RA_THT_Prod(Poste_RG, Poste_Antenne)

    elif tension > 63 and type_antenne == "Mixte":
        return RA_THT_Mixte(Poste_RG, Poste_Antenne)

    elif tension == 63 and type_antenne == "Conso":
        return RA_HT_Conso(Poste_RG, Poste_Antenne)

    elif tension == 63 and type_antenne == "Prod":
        return RA_HT_Prod(Poste_RG, Poste_Antenne)

    elif tension == 63 and type_antenne == "Mixte":
        return RA_HT_Mixte(Poste_RG, Poste_Antenne)

    # Message d'erreur on n'est pas censé être dans ce cas
    return "Erreur configuration impossible GET_RA"
