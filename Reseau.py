from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

# Ouverture de la BDD
engine = create_engine("sqlite:///RSO.db", echo=True)

# Définition de la classe
Base = declarative_base()

class Element(Base):
    __tablename__ = "Element_reseau"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    tension = Column(Integer, nullable=False)
    etat = Column(String, nullable=False)
    voisin = Column(JSON)
    topo_poste = Column(String)

    def __repr__(self):
        return f"<Element id={self.id} type={self.type} tension={self.tension} etat={self.etat} voisin={self.voisin} topo={self.topo_poste}>"

# Création d'une session
Session = sessionmaker(bind=engine)
session = Session()

# Ajout d'un nouveau élément
def add_element(type, tension, etat, voisin, topo_poste):
    nouvel_user = Element(type=type, tension=tension, etat=etat, voisin=voisin, topo_poste=topo_poste)
    session.add(nouvel_user)
    session.commit()

"""
Lecture des données
ele = session.query(Element).all()
for u in ele:
    print(u)
"""

# Fermeture
session.close()
