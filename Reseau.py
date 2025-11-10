from sqlalchemy import create_engine, Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

# Ouverture de la BDD
engine = create_engine("sqlite:///RSO.db", echo=True)

# Définition de la classe
Base = declarative_base()

class Element(Base):
    __tablename__ = "Element_reseau"

    id = Column(Integer, primary_key=True)
    tension = Column(Integer)
    etat = Column(Boolean)
    voisin = Column(JSON)
    topo = Column(String)

    def __repr__(self):
        return f"<Element(id={self.id}, tension={self.tension}, etat={self.etat}, voisin={self.voisin}, topo={self.topo})>"

# Création d'une session
Session = sessionmaker(bind=engine)
session = Session()

# Ajout d'un nouveau élément
def add_element(tension, etat, voisin, topo):
    nouvel_user = Element(tension=tension, etat=etat, voisin=voisin, topo=topo)
    session.add(nouvel_user)
    session.commit()

"""Lecture des données
ele = session.query(Element).all()
for u in ele:
    print(u)
"""

# Fermeture
session.close()
