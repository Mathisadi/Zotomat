'L objectif est de connaitre la topo du réseau et en fonction on réajuste les automates'
'Pour savoir si c est une antenne c est un poste ou il y a qu une ligne ou plusieurs ligne mais qu une pas en antente'

def antenne(element_poste):
    'On trouve les liens connecté au poste'
    voisin_id = element_poste.voisin
    
    