# webapp de visualisation de graphes

Le but de cette archive est d'illustrer comment on peut construire une application qui s'appuie sur une base de données graphes.

Sans aller jusqu'à utiliser une base de donnes graphes comme Neo4j, on peut très bien stocker les données sous forme d'un fichier Tulip contenant tous les éléments qui nous intéresse.

L'application elle-même repose sur un serveur Flask agissant comme contrôleur.

- L'application suit l'architecture MVC (modèle/vue/contrôleur)
- Le contrôleur fait appel au modèle chargé de manipuler les données, et calculer tous les objets qui doivent servir à produire les visualisations
- La vue se charge de traduire ces objets en objets json qui suivent le format défini dans l'application. C'est la vue qui connait les particulatiés dont il fat tenir compte dans l'interface (la page web côté client).
- Le contrôleur renvoie au client une page html contenant tout le code (javascript) sollicité pour construire l'objet SVG (à partir d'un fichier de description produit par la vue et srtocké côté serveur).