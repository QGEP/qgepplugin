class Hydraulischer_Knoten(SIA405_Base.SIA405_BaseClass):  # Noeud_hydraulique(SIA405_Base_f.SIA405_BaseClass)
    pass

class Hydraulischer_Knoten_Text(SIA405_Base.SIA405_TextPos):  # Noeud_hydraulique_Texte(SIA405_Base_f.SIA405_TextePos)
    pass

class Hydraulischer_Strang(SIA405_Base.SIA405_BaseClass):  # Troncon_hydraulique(SIA405_Base_f.SIA405_BaseClass)
    pass

class Hydraulischer_Strang_Text(SIA405_Base.SIA405_TextPos):  # Troncon_hydraulique_Texte(SIA405_Base_f.SIA405_TextePos)
    pass

class Leitung(SIA405_Base.SIA405_BaseClass):  # Conduite(SIA405_Base_f.SIA405_BaseClass)
    pass

class Leitung_Text(SIA405_Base.SIA405_TextPos):  # Conduite_Texte(SIA405_Base_f.SIA405_TextePos)
    pass

class Schadenstelle(SIA405_Base.SIA405_BaseClass):  # Lieu_de_fuite(SIA405_Base_f.SIA405_BaseClass)
    pass

# ABSTRACT !
class Leitungsknoten(SIA405_Base.SIA405_BaseClass):  # Noeud_de_conduite(SIA405_Base_f.SIA405_BaseClass)
    pass

class Leitungsknoten_Text(SIA405_Base.SIA405_TextPos):  # Noeud_de_conduite_Texte(SIA405_Base_f.SIA405_TextePos)
    pass

class Absperrorgan(Leitungsknoten):  # Organe_de_fermeture(Noeud_de_conduite)
    pass

class Hydrant(Leitungsknoten):  # Hydrant(Noeud_de_conduite)
    pass

class Rohrleitungsteil(Leitungsknoten):  # Composant(Noeud_de_conduite)
    pass

class Hausanschluss(Leitungsknoten):  # Branchement_d_immeuble(Noeud_de_conduite)
    pass

class Muffen(Leitungsknoten):  # Connexion_tubulaire(Noeud_de_conduite)
    pass

class Uebrige(Leitungsknoten):  # Autres(Noeud_de_conduite)
    pass

class Anlage(Leitungsknoten):  # Installation(Noeud_de_conduite)
    pass

class Foerderanlage(Leitungsknoten):  # Station_de_pompage(Noeud_de_conduite)
    pass

class Wasserbehaelter(Leitungsknoten):  # Reservoir_d_eau(Noeud_de_conduite)
    pass

class Wassergewinnungsanlage(Leitungsknoten):  # Installation_d_approvisionnement_en_eau(Noeud_de_conduite)
    pass

class Spezialbauwerk(SIA405_Base.SIA405_BaseClass):  # Construction_speciale(SIA405_Base_f.SIA405_BaseClass)
    pass

class Spezialbauwerk_Flaeche(None):  # Construction_speciale_Surface(None)
    pass

class Spezialbauwerk_Linie(None):  # Construction_speciale_Ligne(None)
    pass

class Spezialbauwerk_Text(SIA405_Base.SIA405_TextPos):  # Construction_speciale_Texte(SIA405_Base_f.SIA405_TextePos)
    pass

class Uebersichtsplanposition(SIA405_Base.SIA405_SymbolPos):  # Position_plan_d_ensemble(SIA405_Base_f.SIA405_SymbolePos)
    pass

