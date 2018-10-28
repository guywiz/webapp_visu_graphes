# webapp de visualisation de graphes

Le but de cette archive est d'illustrer comment on peut construire une application qui s'appuie sur une base de données graphes.

Sans aller jusqu'à utiliser une base de donnes graphes comme Neo4j, on peut très bien stocker les données sous forme d'un fichier Tulip contenant tous les éléments qui nous intéresse.

L'application elle-même repose sur un serveur Flask agissant comme contrôleur.

- L'application suit l'architecture MVC (modèle/vue/contrôleur)
- Le contrôleur fait appel au modèle chargé de manipuler les données, et calculer tous les objets qui doivent servir à produire les visualisations
- La vue se charge de traduire ces objets en objets json qui suivent le format défini dans l'application. C'est la vue qui connait les particulatiés dont il fat tenir compte dans l'interface (la page web côté client).
- Le contrôleur renvoie au client une page html contenant tout le code (javascript) sollicité pour construire l'objet SVG (à partir d'un fichier de description produit par la vue et srtocké côté serveur).


## installation et usage

Suffit d'installer l'archive depuis là où le serveur sera lancé.

L'application est sur le port 5000 (par défaut pour Flask). Typiquement, si l'application est sur localhost, on la lance en allant sur

http://127.0.0.1:5000

En rechargeant la page, on pourra observer que le calcul du dessin du graphe est fait à la volée (alors que la structure, etc. est stocké au niveau des données).

