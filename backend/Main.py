# Fichier où on récupère les fonctions et on liste l'ensemble des RA dans un fichier CSV dans le dossier res
# Input : Etat du réseau => antenne => RA
# On trouve les bridge puis tous les postes en antenne puis pour chaque poste en antenne le

from Antenne import *
from RA import *

# Ouverture de la BDD Reseau
df_rso = pd.read_csv("./data/Etat_reseau.csv")

# On supprime toutes les liaisons HU ou SUAV
df_rso = df_rso[df_rso["Etat"] == "ES"]

# Ouverture de la BDD Poste
df_poste = pd.read_csv("./data/Type_poste.csv")

# On crée le graphe a partir de la BDD
G = nx.from_pandas_edgelist(
    df_rso, source="Poste_A", target="Poste_B", edge_attr="Tension"
)

print(df_rso)

# On extrait tous les pont
bridge_list = list(nx.bridges(G))

# On crée un dataframe res
df_res = pd.DataFrame()

# Fonction qui retourne les RA des postes en antenne
for bridge in bridge_list:
    # Postes en antenne
    arbre = get_poste_en_antenne(G, bridge)
    
    # Pour chaque poste en antenne on trouve le RA
    for poste_P,poste_F in arbre.edges():
        # On trouve les descendants du poste Père
        descendants = get_descendants(arbre, poste_P)
        
        # Si c'est un cycle on passe au suivant
        if descendants is None:
            continue

        # On trouve le type d'antenne
        type_antenne = get_type_antenne_poste(G, descendants, df_poste)

        # On trouve le RA
        RA = get_RA(poste_P, poste_F, type_antenne)

        # On ajoute les RA à la dataframe
        df_res = pd.concat([df_res, pd.DataFrame(RA)], ignore_index=True)
        
# On crée le fichier res
df_res.to_csv("./res/RA.csv", index=False)