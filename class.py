'Première étape on doit créer le réseau on a besoin de connaitre les liens et le type de liens'
'Trois types elements possible postes ligne prod et conso'
'Topo = antenne ou boucle'

class element:
    def __init__(self, id, type, tension, etat, voisin_id, topo):
        self.id = id
        self.type = type
        self.tension = tension
        self.etat = etat
        self.voisin_id = voisin_id
        self.topo = topo
        
e = element(1, "poste", 0, 0, 0, "antenne")

