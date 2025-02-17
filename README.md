# Résolution du problème du Postier chinois en Python

Dans le cadre de ma 1ère année de BUT informatique, nous <i>(en équipe de 3)</i> avons réalisé un projet pour résoudre le problème du postier chinois, qui consiste à trouver le plus court chemin dans un graphe connexe non orienté qui passe au moins une fois par chaque arête et revient à son point de départ (choisi par l'utilisateur), ce qui correspond au cycle eulerien du graphe selon le point de départ donné.

### Nous avons donc réalisé les étapes suivantes : 
- Création d'une classe afin de gérer les graphes valués <i>(avec des arêtes ayant des poids / valeurs)</i> en tant qu'objets
- Création de toutes les méthodes nécessaires à la gestion des graphes (gestions des sommets, arêtes, poids)
- Création des méthodes pour vérifier si un graphe est Eulerien (= passant exactement 1 fois par chaque arête et revient au départ)
  - <b>Si le graphe est Eulerien</b>, il suffit de retrouver le chemin correspondant au sommet de départ donné
  - Sinon, le graphe est <b>peut-être un graphe Semi-Eulerien</b> (= passant exactement 1 fois par chaque arête sans revenir au départ)
    - Si c'est le cas, on va le <b>tranfsormer en un graphe Eulerien</b> en créant une arête entre les 2 sommets qui l'empêche d'être Eulerien, avec comme poids la distance la plus courte possible de cette arête (calculée par l'algorithme de Dijkstra)
    - Sinon, le graphe n'est pas Eulerien et il n'y aura pas de chamin a trouver.
