# Trucs que je comprends pas

modèle SIA + modèle QWAT + business domain + interlis + ili2pg

## Interlis

### SmartInheritance 

Ca aplatit les inheritance, ça, ok, mais du coup, comment ça gère les FK, par exemple
node_from, node_to pour un tronçon ? avec ili2pg, il y a toujours la table noeud_hydraulique, alors que j'imagine que tous les noeuds devraient être des sous-classes ? ou bien c'est copié séparément dans les 2 (dénormalisé) ?  

=> j'ai l'impression que utiliser smartInheritance n'est pas une bonne idée, ça ajoute une couche de problèmes possibles

Mais sans smartinheritance, on dirait qu'il manque des tables (p. ex. hydrant ou reservoir_d_eau), qui pourtant apparaîssent avec smartinheritance... Je sais pas si c'est un bug ?

=> apparement il faut specifier --noSmartInheritance, et apparament tous les autrs paramètres foutent le bordel


### Modèle SIA

Il y a [conduite]1->N[troncon_hydraulique], comment il peut y avoir plusieurs conduite par troncon ?!

Quelle est la relation `noeud_de_conduite` / `noeud_hydraulique` ?

Il y a deux modèle par fichier ilis, p. ex. `SIA405_EAUX_2015_LV95` et `SIA405_EAUX_2015`, quel est le lien entre les 2 ?

#### Documentation

Les modèles ne sont vraiment pas documentés ?!! Ou bien c'est dans les cahiers payants (voir https://www.sia.ch/fr/services/sia-norm/geodonnees/)

### Modèle QWAT

Est-ce que la table "node" est concrète+abstraite ? (en gros, elle peut contenir des élément node non-subclassés, et des éléments node avec subclasses p. ex. installation ?)

À priori, sans discriminant de type (genre "entity_type"), je pense qu'il faudrait avoir des classes purement abstraites ou purement concrètes, sinon c'est pas facile de gérer les imports/exports.

P. ex. je trouve pas l'objet 13964