from .automap_base import AutomapBase
from . import Base_f
from . import SIA405_Base_f


class Noeud_hydraulique(SIA405_Base_f.SIA405_BaseClass):  # Hydraulischer_Knoten(SIA405_Base.SIA405_BaseClass)
    __tablename__ = 'noeud_hydraulique'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Noeud_hydraulique_Texte(SIA405_Base_f.SIA405_TextePos):  # Hydraulischer_Knoten_Text(SIA405_Base.SIA405_TextPos)
    __tablename__ = 'noeud_hydraulique_texte'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Troncon_hydraulique(SIA405_Base_f.SIA405_BaseClass):  # Hydraulischer_Strang(SIA405_Base.SIA405_BaseClass)
    __tablename__ = 'troncon_hydraulique'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Troncon_hydraulique_Texte(SIA405_Base_f.SIA405_TextePos):  # Hydraulischer_Strang_Text(SIA405_Base.SIA405_TextPos)
    __tablename__ = 'troncon_hydraulique_texte'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Conduite(SIA405_Base_f.SIA405_BaseClass):  # Leitung(SIA405_Base.SIA405_BaseClass)
    __tablename__ = 'conduite'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Conduite_Texte(SIA405_Base_f.SIA405_TextePos):  # Leitung_Text(SIA405_Base.SIA405_TextPos)
    __tablename__ = 'conduite_texte'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Lieu_de_fuite(SIA405_Base_f.SIA405_BaseClass):  # Schadenstelle(SIA405_Base.SIA405_BaseClass)
    __tablename__ = 'lieu_de_fuite'
    __table_args__ = {'schema': 'pg2ili_wasser'}

# ABSTRACT !
class Noeud_de_conduite(SIA405_Base_f.SIA405_BaseClass):  # Leitungsknoten(SIA405_Base.SIA405_BaseClass)
    __tablename__ = 'noeud_de_conduite'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Noeud_de_conduite_Texte(SIA405_Base_f.SIA405_TextePos):  # Leitungsknoten_Text(SIA405_Base.SIA405_TextPos)
    __tablename__ = 'noeud_de_conduite_texte'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Organe_de_fermeture(Noeud_de_conduite):  # Absperrorgan(Leitungsknoten)
    __tablename__ = 'organe_de_fermeture'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Hydrant(Noeud_de_conduite):  # Hydrant(Leitungsknoten)
    __tablename__ = 'hydrant'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Composant(Noeud_de_conduite):  # Rohrleitungsteil(Leitungsknoten)
    __tablename__ = 'composant'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Branchement_d_immeuble(Noeud_de_conduite):  # Hausanschluss(Leitungsknoten)
    __tablename__ = 'branchement_d_immeuble'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Connexion_tubulaire(Noeud_de_conduite):  # Muffen(Leitungsknoten)
    __tablename__ = 'connexion_tubulaire'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Autres(Noeud_de_conduite):  # Uebrige(Leitungsknoten)
    __tablename__ = 'autres'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Installation(Noeud_de_conduite):  # Anlage(Leitungsknoten)
    __tablename__ = 'installation'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Station_de_pompage(Noeud_de_conduite):  # Foerderanlage(Leitungsknoten)
    __tablename__ = 'station_de_pompage'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Reservoir_d_eau(Noeud_de_conduite):  # Wasserbehaelter(Leitungsknoten)
    __tablename__ = 'reservoir_d_eau'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Installation_d_approvisionnement_en_eau(Noeud_de_conduite):  # Wassergewinnungsanlage(Leitungsknoten)
    __tablename__ = 'installation_d_approvisionnement_en_eau'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Construction_speciale(SIA405_Base_f.SIA405_BaseClass):  # Spezialbauwerk(SIA405_Base.SIA405_BaseClass)
    __tablename__ = 'construction_speciale'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Construction_speciale_Surface(AutomapBase):  # Spezialbauwerk_Flaeche(AutomapBase)
    __tablename__ = 'construction_speciale_surface'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Construction_speciale_Ligne(AutomapBase):  # Spezialbauwerk_Linie(AutomapBase)
    __tablename__ = 'construction_speciale_ligne'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Construction_speciale_Texte(SIA405_Base_f.SIA405_TextePos):  # Spezialbauwerk_Text(SIA405_Base.SIA405_TextPos)
    __tablename__ = 'construction_speciale_texte'
    __table_args__ = {'schema': 'pg2ili_wasser'}

class Position_plan_d_ensemble(SIA405_Base_f.SIA405_SymbolePos):  # Uebersichtsplanposition(SIA405_Base.SIA405_SymbolPos)
    __tablename__ = 'position_plan_d_ensemble'
    __table_args__ = {'schema': 'pg2ili_wasser'}

